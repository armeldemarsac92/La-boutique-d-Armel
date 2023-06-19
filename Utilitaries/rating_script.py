import time
import pandas as pd
import requests
import json
import datetime


# Function to load access token from file
def load_access_token_from_file(file_name="../Assets/Data/credentials.json"):
    with open(file_name, "r") as file:
        data = json.load(file)
        return data["api_key"]

# Load data from CSV file
csv_file = '../Assets/Data/item_data_scrapped_from_vinted.csv'

# Load CSV data into a pandas DataFrame
df = pd.read_csv(csv_file)

# Load API key
api_key = load_access_token_from_file()

def extract_number(value):
    # check if value is a string
    if isinstance(value, str):
        # remove non-numeric characters
        value = value.replace('€', '').replace(',00', '')

        # replace comma with dot as decimal separator
        value = value.replace(',', '.')

        # get the first part before the space (assuming the number is always the first part)
        number = value.split()[0]

        return pd.to_numeric(number, errors='coerce')

    return value


# Base rating parameters per item
view_score_weight = 0.2
like_score_weight = 0.3
trend_weight = 0.5

# Rating parameters updated with item's price, the lower the price, the better.
rating_weight = 0.4  # Adjust this value according to how much you want to weight the item rating
price_weight = 0.6  # Adjust this value according to how much you want to weight the item price

# Brand popularity parameters, Define weights for views, likes, and price (the higher the median price, the better)
views_weight = 0.2
likes_weight = 0.3
price_weight = 0.5

#final parameters
brand_final_weight = 0.5
item_final_weight = 0.5

df['days_elapsed'] = df['item_date_added'].apply(lambda x: (datetime.datetime.now() - pd.to_datetime(x)).days)
df['item_initial_followers2'] = df['item_initial_followers'].apply(extract_number)
df['item_current_followers2'] = df['item_current_followers'].apply(extract_number)
df['item_current_followers2'].fillna(df['item_initial_followers2'], inplace=True)  # Fill empty values with initial followers

df['item_current_views'].fillna(df['item_initial_views'], inplace=True)  # Fill empty values with initial views


df['item_price2'] = df['item_price'].apply(extract_number)
print(df['item_price'])
print(df['item_price2'])
print(df['item_current_followers2'])

df['gained_views'] = df['item_current_views'] - df['item_initial_views']
df['gained_likes'] = df['item_current_followers2'] - df['item_initial_followers2']
df['trend_coefficient'] = 1 + (df['gained_likes']/df['gained_views'])* trend_weight
df['trend_coefficient'].fillna(1, inplace=True)
df['view_score'] = (df['item_current_views']/df['days_elapsed'])*view_score_weight
df['like_score'] = (df['item_current_followers2']/df['days_elapsed'])*like_score_weight
df['item_rating'] = (df['view_score'] + df['like_score'])*df['trend_coefficient']
print(df['item_rating'])
# Calculate Min-Max for normalization for item_rating
max_rating = df['item_rating'].max()
min_rating = df['item_rating'].min()

# Normalize item_rating
df['item_rating_normalized'] = (df['item_rating'] - min_rating) / (max_rating - min_rating)

# Calculate Min-Max for normalization for item_price
max_price = df['item_price2'].max()
min_price = df['item_price2'].min()
print(min_price)
# Normalize item_price (1 - to get higher score for lower price)
df['item_price_normalized'] = 1 - ((df['item_price2'] - min_price) / (max_price - min_price))

# Calculate final item rating based on weights
df['item_final_rating'] = rating_weight * df['item_rating_normalized'] + price_weight * df['item_price_normalized']
print(df['item_final_rating'])

# Calculate median price for each brand
brand_low_price_index = df.groupby('item_brand')['item_price2'].quantile(0.30)

# Create a new column 'brand_median_price' in the dataframe
df['brand_low_price_index'] = df['item_brand'].map(brand_low_price_index)

# Calculate brand popularity
brand_popularity = df.groupby('item_brand').agg({
    'item_initial_views': 'mean',
    'item_initial_followers2': 'mean',
    'item_price2': 'median'
}).rename(columns={
    'item_initial_views': 'avg_views',
    'item_initial_followers2': 'avg_likes',
    'item_price2': 'median_price'
})


# Normalize the three factors in brand_popularity DataFrame
for column in brand_popularity.columns:
    brand_popularity[column] = (brand_popularity[column] - brand_popularity[column].min()) / (brand_popularity[column].max() - brand_popularity[column].min())

brand_popularity['popularity_score'] = views_weight * brand_popularity['avg_views'] + likes_weight * brand_popularity['avg_likes'] + price_weight * brand_popularity['median_price']
print(brand_popularity['popularity_score'])

# Check if the 'popularity_score' column already exists in the DataFrame
if 'popularity_score' in df.columns:
    # Map the 'popularity_score' values from brand_popularity based on 'item_brand' values
    df['popularity_score'] = df['item_brand'].map(brand_popularity['popularity_score'])
    df['brand_price'] = df['item_brand'].map(brand_popularity['median_price'])
else:
    # Merge brand_popularity DataFrame back to the original DataFrame
    df = df.merge(brand_popularity['popularity_score'], left_on='item_brand', right_index=True)

print(df['popularity_score'])

# Adjust the final item rating based on brand popularity
df['item_final_rating'] = item_final_weight * df['item_final_rating'] + brand_final_weight * df['popularity_score']

# Normalize the 'item_final_rating' column to have values between 0 and 1
df['item_final_rating'] = (df['item_final_rating'] - df['item_final_rating'].min()) / (df['item_final_rating'].max() - df['item_final_rating'].min())

# Calculate quartiles
calc1 = df['item_final_rating'].quantile(q=0.25, interpolation='linear')
calc2 = df['item_final_rating'].quantile(q=0.70, interpolation='linear')
calc3 = df['item_final_rating'].quantile(q=0.90, interpolation='linear')
print(calc1)
print(calc2)
print(calc3)

print(df.columns)
columns_to_drop = ['item_rating', 'popularity_score', 'item_rating_normalized',
       'item_price_normalized', 'item_initial_followers2',
       'item_current_followers2', 'item_price2']

# Save the updated DataFrame back to the CSV file
df.to_csv('../Assets/Data/item_data_scrapped_from_vinted.csv', index=False)
# Iterate through items with "available" status
for index, row in df.iterrows():
    if row['status'] == 'available':
        # Get raindrop item's tags
        raindrop_id = int(row['raindrop_id'])
        headers = {'Authorization': api_key}
        response = requests.get(f'https://api.raindrop.io/rest/v1/raindrop/{raindrop_id}', headers=headers)

        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['result']:
                    item_data = response_data['item']
                    tags = item_data['tags']


                    tags = [tag for tag in tags if 'Tendance :' not in tag]

                    if row['item_price2']<row['brand_low_price_index']:
                        tags.append('Tendance : bonne affaire \U0001F929')
                    if row['item_final_rating'] > calc3:
                        tags.append('Tendance : article star \u2B50')
                    if calc3 > row['item_final_rating'] > calc2:
                        tags.append('Tendance : à surveiller \U0001F440')

                    print(tags)

                    # Prepare the data for the API request
                    data_for_request = {
                        'tags': tags,
                    }

                    # Make the API request to create a new Raindrop
                    response = requests.put(f'https://api.raindrop.io/rest/v1/raindrop/{raindrop_id}', headers=headers, json=data_for_request)

                    if response.status_code == 200:
                        print(f"Tags updated for item with raindrop ID: {raindrop_id}")
                        time.sleep(1)
                    else:
                        print(f"Failed to update tags for item with raindrop ID: {raindrop_id}")
                        print(response.json())
                else:
                    print(f"Raindrop item not found with ID: {raindrop_id}")
            except json.decoder.JSONDecodeError as err:
                print(f"Error decoding JSON response: {err}")
        else:
            print(f"Failed to fetch raindrop item with ID: {raindrop_id}")
