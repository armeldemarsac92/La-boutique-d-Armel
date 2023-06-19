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
api_key = load_access_token_from_file()

# Load data from CSV file
csv_file = '../Assets/Data/item_data_scrapped_from_vinted.csv'

# Load CSV data into a pandas DataFrame
df = pd.read_csv(csv_file)

# Iterate through items with "available" status
for index, row in df.iterrows():
    if row['status'] == 'available':
        # Get raindrop item's tags
        raindrop_id = int(row['raindrop_id'])
        headers = {'Authorization': api_key}
        response = requests.get(f'https://api.raindrop.io/rest/v1/raindrop/{raindrop_id}', headers=headers)
        time.sleep(0.5)
        if response.status_code == 200:
            print("item not deleted")
        else:
            print("duplicate")