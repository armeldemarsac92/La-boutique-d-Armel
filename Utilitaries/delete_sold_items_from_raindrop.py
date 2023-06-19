import pandas as pd
import requests
import json
import time

def load_access_token_from_file(file_name="../Assets/Data/credentials.json"):
    with open(file_name, "r") as file:
        data = json.load(file)
        return data["api_key"]

file_path = '../Assets/Data/item_data_scrapped_from_vinted.csv'
df = pd.read_csv(file_path)

# Fill missing values in the 'raindrop_id' column and convert it to integers
df['raindrop_id'] = df['raindrop_id'].fillna(-1).astype(int)

api_url = "https://api.raindrop.io/rest/v1/raindrop"
access_token = load_access_token_from_file()
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

def delete_raindrop(raindrop_id):
    response = requests.delete(f"{api_url}/{raindrop_id}", headers=headers)
    if response.status_code == 200:
        print(f"Deleted raindrop {raindrop_id}")
        return True
    else:
        print(f"Error deleting raindrop {raindrop_id}: {response.text}")
        return False

for index, row in df.iterrows():
    if row['status'] == 'sold':
        raindrop_id = row['raindrop_id']
        if raindrop_id != -1:  # Skip invalid raindrop_ids
            success = delete_raindrop(raindrop_id)
            if success:
                df.at[index, 'status'] = 'sold - deleted'
        time.sleep(1)

df.to_csv(file_path, index=False)
