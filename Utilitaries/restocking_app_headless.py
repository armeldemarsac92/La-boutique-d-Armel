
import json
import random
import ast
import subprocess
import pandas as pd
import math
import sys
import os

with open("../Assets/Catalogs/size_catalog.json", "r") as size_catalog:
    size_dict = json.load(size_catalog)
# Load the brand_catalog.json file
with open("../Assets/Catalogs/brand_catalog.json", "r") as brand_catalog_file:
    brand_dict = json.load(brand_catalog_file)
# Reverse the dictionary to map from brand_id to brand_name
reversed_brand_dict = {v: k for k, v in brand_dict.items()}
def brand_catalog(brand_id):
    # Get the brand name from the reversed dictionary
    return reversed_brand_dict.get(brand_id, "Unknown Brand")

def count_tailles_inferieures(cloth_data, query_urls, size_quotas):
    print(cloth_data.keys())
    tailles_inferieures = 0
    for size, quantity in cloth_data[category].items():
        expected_quantity = int(parameters['desired_number_of_items'] * size_quotas[
            list(cloth_data[category].keys()).index(size)])
        if quantity < expected_quantity:
            tailles_inferieures += 1

    return tailles_inferieures

df = pd.read_csv('../Assets/Data/item_data_scrapped_from_vinted.csv')
df = df[df['status'] != 'pending']
# Assume you've loaded your dataframe into the variable `df`
# Replace 'status' and 'item_brand' with the appropriate column names in your CSV
df['status'] = df['status'].apply(lambda x: x.lower())  # Normalize status values
grouped = df.groupby('item_brand')['status'].value_counts().unstack().fillna(0)
# Calculate the ratio
grouped['ratio'] = grouped['available'] / (grouped['available'] + grouped['rejected'])

# Read and parse the three files
with open('../Assets/Data/size_quotas.json', 'r') as f3:
    size_quotas = json.load(f3)
# Define the sizes you're interested in
tags_of_interest = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../Assets/Data/item_quantities_per_tags_and_collections.csv', encoding='utf-8')
# filter DataFrame to exclude rows where 'desired_number_of_items' is empty
df = df[df['desired_number_of_items'].notna()]

# Initialize an empty dictionary to store the item quantities
cloth_data = {}

# Loop through each row in the DataFrame
for _, row in df.iterrows():
    # Extract the title
    title = row["Title"]

    # Initialize a new dictionary to store the quantities of the tags of interest
    quantities = {}

    # Loop through the tags of interest
    for tag in tags_of_interest:
        # If the tag is in the row, add its quantity to the new dictionary
        if tag in row:
            quantities[tag] = int(row[tag])

    # Add the new dictionary to the item quantities dictionary
    cloth_data[title] = quantities

# Read the existing query URLs and parameters from the DataFrame
query_urls = {}

if 'query' in df.columns:
    print('query is in the df')
    for _, row in df.iterrows():
        collection = row['Title']
        parameters = {
            'query': row['query'],
            'brand_ids': row['brand_ids'],
            'category_ids': row['category_ids'],
            'color_ids': row['color_ids'],
            'desired_number_of_items': row['desired_number_of_items'],
            'url': row['url'],
            'ID': row['ID'],
            'Title': row['Title']
        }
        query_urls[collection] = parameters

# Initialize a dictionary to store the results
results = {}
ecart = {}

session_token = random.randint(0, 10000)


# Loop through each category in the query URLs and parameters
for category, parameters in query_urls.items():
    # Initialize a dictionary to store the category results
    category_results = {}
    ecart[category] = {}


    # initiate i to track the progress of the collection fetching
    i = 0


    # defines the number of sizes to iterate through, used for the progress bar


    tailles_inferieures = count_tailles_inferieures(cloth_data, query_urls, size_quotas)

    print('a')

    # Loop through each size in the cloth data for this category
    for size, quantity in cloth_data[category].items():

        ecart[category][size] = 0

        # Convert brand_ids from string to list
        brand_ids = ast.literal_eval(parameters['brand_ids'])
        for brand_id in brand_ids:

            brand_upper = brand_catalog(brand_id).upper()
            print(brand_upper)
            if brand_upper in grouped.index:
                ratio = grouped.loc[brand_upper, 'ratio']
                print(ratio)
            else:
                ratio = 0.7

            print(f"current dict : {ecart[category][size]}")


            # Multiply the desired number of items by the size quota to get the expected quantity
            expected_quantity = int(parameters['desired_number_of_items'] * size_quotas[list(cloth_data[category].keys()).index(size)])

            # Compare the effective quantity with the expected quantity
            if quantity < expected_quantity:
                category_results[size] = f'UNDERSTOCK ({quantity} < {expected_quantity})'

                # Launch the scraping script with the difference as the number of items to fetch
                pieces_a_chercher = math.ceil((((expected_quantity - quantity)/len(brand_ids))/ratio)+ecart[category][size])


                query = parameters['query']
                brand_ids_str = f"&brand_id[]={brand_id}"
                site = parameters['url'] + "&size_id[]=" + str(size_dict[size]) + "&brand_id[]=" + str(brand_id)

                # Path to the Python interpreter within the virtual environment
                virtual_env_python = r'C:\Users\Armel\PycharmProjects\boutique_sql\venv\Scripts\python.exe'

                # Defines the parameters to pass to the scraping script
                cmd = [
                    virtual_env_python,
                    '../Utilitaries/test.py',
                    site,
                    str(pieces_a_chercher),
                    str(query),
                    str(session_token),
                    str(parameters['Title']),
                    str(parameters['ID']),
                ]

                print("Launching scraping process...")
                print(parameters['ID'])
                print(parameters['Title'])

                process = subprocess.Popen(cmd, env=dict(os.environ, PYTHONPATH=sys.executable), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # displays an informational message
                print(f"Lancement de la recherche de {pieces_a_chercher} {category} de la marque {brand_catalog(brand_id)} en {size}...")

                stdout, stderr = process.communicate()
                stdout_str = stdout.decode('utf-8')

                print(f"stdout: {stdout}")
                print(f"stderr: {stderr}")

                # Find the index of the phrase in the stdout
                index = stdout_str.find('Items scrapped:')

                # Find the index of the phrase in the stdout
                index = stdout_str.find('Items scrapped:')

                # If the phrase was found
                if index != -1:
                    # Get the part of the stdout after the phrase
                    after_phrase = stdout_str[index + len('Items scrapped:'):]

                    # Split this part into words
                    words = after_phrase.split()

                    # The first word should be the number of items scrapped
                    if words:
                        collected_pieces_count = int(words[0])
                    else:
                        print('No number found after the phrase')
                else:
                    print('Phrase not found in stdout')

                if 0 < collected_pieces_count < pieces_a_chercher:
                    # The script_b.py execution has completed
                    print(
                        f"La recherche de {category} pour la marque {brand_catalog(brand_id)} en {size} est incomplète : {collected_pieces_count}/{pieces_a_chercher} pièces.")
                    # Adjust expected_quantity
                    ecart[category][size] = (pieces_a_chercher - collected_pieces_count)
                    # Update cloth_data with the new expected quantity
                if collected_pieces_count == 0 :
                    print(
                        f"La recherche de {pieces_a_chercher} {category} pour la marque {brand_catalog(brand_id)} en {size} n'a pas abouti. Aucun article disponible sur Vinted.")
                    # Adjust expected_quantity
                    ecart[category][size] = (pieces_a_chercher - collected_pieces_count)
                else :
                    # The script_b.py execution has completed
                    print(
                        f"La recherche des {pieces_a_chercher} {category} de la marque {brand_catalog(brand_id)} en {size} est terminée")
                    ecart[category][size] = (pieces_a_chercher - collected_pieces_count)

                # updates the progress of the collection fetching
                i += 1

                print(f"Avancement du restockage pour {category} : {i}/{tailles_inferieures*len(brand_ids)} tailles.")


            elif quantity == expected_quantity:
                category_results[size] = 'OK'
                print(category_results[size])
            else:
                category_results[size] = f'OVERSTOCK ({quantity} > {expected_quantity})'
                print(category_results[size])

        # Add the category results to the overall results dictionary
        results[category] = category_results

    # The script_b.py execution has completed
    print('script completed')


