import requests
import pandas as pd
import json
import time

df = pd.read_csv("../Assets/Data/item_quantities_per_tags_and_collections.csv")

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
            'count': collection['count'],
            'is_child': True if parent_id else False
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

# Fetch the raindrops for a given collection
def get_raindrops(collection_id, api_key):
    url = f"https://api.raindrop.io/rest/v1/raindrops/{collection_id}"
    headers = {"Authorization": f"{api_key}"}
    raindrops = []
    page = 0
    per_page = 50

    while True:
        params = {"page": page, "perpage": per_page}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            if not data["items"]:
                break

            raindrops.extend(data["items"])
            page += 1
        else:
            print(f"Error: {data.get('error', 'Unknown error')}")
            return []

    return raindrops

# Calculate tag counts for each collection
# Calculate tag counts for each collection
def get_tag_counts(collections, api_key):
    tag_counts = {}

    for collection in collections:
        raindrops = get_raindrops(collection["_id"], api_key)

        for raindrop in raindrops:
            if "tags" in raindrop:  # Ensure that the raindrop has tags
                for tag in raindrop["tags"]:
                    if tag not in tag_counts:
                        tag_counts[tag] = {}
                    if (collection["_id"], collection["title"]) not in tag_counts[tag]:
                        tag_counts[tag][(collection["_id"], collection["title"])] = 0
                    tag_counts[tag][(collection["_id"], collection["title"])] += 1



    return tag_counts


# Convert the collections list and tag counts into a pandas DataFrame
def collections_to_dataframe(collections, tag_counts):
    data = {
        'ID': [],
        'Title': [],
        'Parent_ID': [],
        'Count': [],
        "query": "",
        "brand_ids": "",
        "category_ids": "",
        "color_ids": "",
        "desired_number_of_items": "",
        "url": ""
    }

    # Add columns for each tag
    for tag in tag_counts.keys():
        data[tag] = []

    for collection in collections:
        data['ID'].append(collection['_id'])
        data['Title'].append(collection['title'])
        data['Parent_ID'].append(collection['parent'] if collection['parent'] else '')
        data['Count'].append(collection['count'])

        # Add tag counts for each tag
        for tag in tag_counts.keys():
            data[tag].append(tag_counts[tag].get((collection["_id"], collection["title"]), 0))

    return pd.DataFrame(data)


# Load the access token
api_key = load_access_token_from_file()

# Fetch the collections again (you might want to update your collections and tags)
collections = get_collections(api_key)

if collections:
    # Get the new tag counts for each collection
    tag_counts = get_tag_counts(collections, api_key)

    # Update the DataFrame with new tag counts
    for tag, counts in tag_counts.items():
        if tag not in df.columns:
            df[tag] = 0
        for collection_id, title in counts.keys():
            df.loc[df['ID'] == collection_id, tag] = counts[(collection_id, title)]

    # Save the updated DataFrame back to the CSV file
    df.to_csv('../Assets/Data/item_quantities_per_tags_and_collections.csv', index=False)

    print("Collections updated and saved to 'item_quantities_per_tags_and_collections.csv'")

else:
    print("Error fetching collections")
