import requests
import pandas as pd
import json
from tqdm import tqdm
import time

# Load access token from a file
def load_access_token_from_file(file_name="../Assets/Data/credentials.json"):
    with open(file_name, "r") as file:
        data = json.load(file)
        return data["api_key"]

# Recursive function to extract collections (including child collections)
def extract_collections(collections_data, parent_id=None):
    collections = []

    for collection in collections_data:
        collections.append({
            '_id': collection['_id'],
            'title': collection['title'],
            'parent': parent_id,
            'count': collection['count']
        })

        if "children" in collection:
            collections.extend(extract_collections(collection["children"], collection['_id']))

    return collections

# Fetch collections (including child collections) from Raindrop API
def get_collections(api_key):
    url = "https://api.raindrop.io/rest/v1/collections/childrens"
    headers = {"Authorization": f"{api_key}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        collections = extract_collections(data["items"])
        return collections
    else:
        print(f"Error: {data['error']}")
        return None

def get_raindrops(collection_id, api_key):
    url = f"https://api.raindrop.io/rest/v1/raindrops/{collection_id}"
    headers = {"Authorization": f"{api_key}"}
    raindrops = []
    page = 0
    per_page = 50

    while True:
        params = {"page": page, "perpage": per_page}
        response = requests.get(url, headers=headers, params=params)
        time.sleep(0.5)

        try:
            data = response.json()

            if response.status_code == 200:
                if not data["items"]:
                    return raindrops

                raindrops.extend(data["items"])
                time.sleep(0.5)
                page += 1
            else:
                print(f"Error: {data.get('error', 'Unknown error')}")
                return []

        except json.JSONDecodeError:
            print("Error decoding JSON response")
            print(response.content)
            return []


# Convert the raindrops list into a pandas DataFrame
def raindrops_to_dataframe(raindrops):
    data = {
        'item_link': [],
        'raindrop_id': [],
        'raindrop_last_update': [],
        'raindrop_collection_id': []
    }

    for raindrop in raindrops:
        if "vinted" in raindrop['link']:
            data['item_link'].append(raindrop['link'])
            data['raindrop_id'].append(raindrop['_id'])
            data['raindrop_last_update'].append(raindrop['lastUpdate'])
            data['raindrop_collection_id'].append(raindrop['collectionId'])
    return pd.DataFrame(data)

# Load the access token
api_key = load_access_token_from_file()

# Fetch the collections
collections = get_collections(api_key)

all_raindrops = []

if collections:
    for collection in tqdm(collections, desc="Fetching raindrops"):
        raindrops = get_raindrops(collection["_id"], api_key)
        all_raindrops.extend(raindrops)
        time.sleep(1)
else:
    print("Error fetching collections")


# Convert raindrops to a DataFrame
df = raindrops_to_dataframe(all_raindrops)

# Load existing CSV file
file_path = '../Assets/Data/item_data_scrapped_from_vinted5.csv'
existing_df = pd.read_csv(file_path)

# Create a new DataFrame with the same columns as the existing one
new_df = pd.DataFrame(columns=existing_df.columns)

# Add the raindrops data to the new DataFrame, matching the column names
for index, row in df.iterrows():
    new_row = {
        'item_link': row['item_link'],
        'raindrop_id': row['raindrop_id'],
        'raindrop_last_update': row['raindrop_last_update'],
        'raindrop_collection_id': row['raindrop_collection_id']
    }
    new_df.loc[len(new_df)] = new_row

# Merge the existing DataFrame with the new raindrops DataFrame
merged_df = pd.concat([existing_df, new_df], axis=0, ignore_index=True)

# Update the raindrop_id for rows where status is 'available' and raindrop_id is -1
link_to_id = {rd['link']: rd['_id'] for rd in all_raindrops if "vinted" in rd['link']}
mask = (merged_df['status'] == 'available')
for index in merged_df[mask].index:
    item_link = merged_df.loc[index, 'item_link']
    if item_link in link_to_id:
        merged_df.loc[index, 'raindrop_id'] = link_to_id[item_link]

# Write the updated DataFrame back to the CSV file
merged_df.to_csv(file_path, index=False)
new_df.to_csv('../Assets/Data/item_data_scrapped_from_vinted6.csv')
