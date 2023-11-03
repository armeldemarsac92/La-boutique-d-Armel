import pandas as pd
import json
import time
import requests
import ast
import pandas as pd

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


# Load API key
with open("../Assets/Data/credentials.json") as f:
    data = json.load(f)
api_key = data['api_key']
API_URL='https://api.raindrop.io/rest/v1/raindrop'

headers = {
    'Authorization': f'{api_key}',
    'Content-Type': 'application/json'
}

# Read the collections file into a DataFrame
collections_df = pd.read_csv('../Assets/Data/item_quantities_per_tags_and_collections.csv')

# Create a dictionary from the DataFrame
collection_dict = collections_df.set_index('Title')['ID'].to_dict()

def clean_data(price_str):
    """Remove currency symbol and convert comma to dot."""
    cleaned_data = price_str.replace('€', '').replace(',', '.').strip()
    return cleaned_data

def get_price_tag(price):
    """Categorize price into a range and return the corresponding tag."""
    if price <= 15:
        return 'moins de 15€ 😍'
    elif 16 <= price <= 49:
        return 'de 16 à 49€ 😏'
    elif 50 <= price <= 99:
        return 'de 50 à 99€ 🫣'
    elif 100 <= price <= 150:
        return 'de 100 à 150€ 😳'
    elif price > 150:
        return 'plus de 150€ 🥵'
    else:
        return ''

# Predefined tags list
tags_list = ['Taille 44 🇮🇹', 'Gris', 'Lumineux ⬜️', 'Style : Militaire 🪖', 'de 16 à 49€ 😏', 'Style : Texturé', 'Uni', 'Taille S',
             'Taille M', 'Taille XS', 'Bleu', 'Sombre ⬛️', 'Formel', 'Casual ✌🏻', 'carreaux', 'Style : Motifs', 'Beige',
             'de 50 à 99€ 🫣', 'Vert', 'plus de 150€ 🥵', 'Croisé', 'Taille XL', 'Taille 36 🇬🇧', 'Taille 50 🇮🇹',
             'Taille 40 🇬🇧', 'Lot', 'Taille 48 🇮🇹', 'de 100 à 150€ 😳', 'Taille 44 🇬🇧', 'Taille 54 🇮🇹', 'Taille L',
             'Marron', 'Velour', 'Style : Mat', 'Style : Rayures', 'Taille 38 🇬🇧', 'Taille 52 🇮🇹', 'Taille 42 🇬🇧', 'Camel',
             'Taille 46 🇮🇹', 'Taille XXXL', 'King size', 'moins de 15€ 😍', 'Taille 47 🇮🇹', 'Taille 37 🇬🇧', 'Rouge',
             'Blanc', 'Denim', 'Taille 40 🇮🇹', 'Taille 56 🇮🇹', 'Taille XXL', 'Taille 58 🇮🇹', 'Noir', 'Brillant',
             'Pointure 42 🇫🇷', 'Pointure 44 🇫🇷', 'Pointure 41 🇫🇷', 'Pointure 38 🇫🇷', 'Pointure 40 🇫🇷',
             'Pointure 45 🇫🇷', 'Pointure 39 🇫🇷', 'Pointure 43 🇫🇷', 'Multicolore', 'uni', 'Orange', 'Jaune', 'Rose',
             'Pointure 49 🇫🇷', 'W32 🇺🇸', 'L34 🇺🇸', 'W31 🇺🇸', 'L30 🇺🇸', 'W29 🇺🇸', 'W34 🇺🇸', 'L32 🇺🇸', 'W30 🇺🇸','W33 🇺🇸', 'W36 🇺🇸', 'W40 🇺🇸', 'L29 🇺🇸', 'W35 🇺🇸', 'Taille 42 🇫🇷', 'Texte', 'Violet']

formal_categories = ['Vestes, blazers et costumes', 'Chemises','Mocassins', 'Derbies et Richelieu', 'Chaussures à boucles', 'Bottines et boots', 'Velours côtelé', 'Pantalons taille haute', 'Chinos',
                     'Foulards, cravates et écharpes', 'Bretelles']

casual_categories = ['Veste de travail', 'Sur-chemises et vareuses',
                     'Manteaux, pardessus & vestes', 'Gilets & doudounes ss manches', 'Blousons', 'Manteaux & vestes',
                     'Tee shirts et marinières', 'Sweat shirts', 'Pulls', 'Polos', 'Chemises', 'Sneakers',
                     'Chaussures bateau','Bottines et boots',
                     'Chaussures', 'Velours côtelé', 'Pantalons taille haute', 'Jeans', 'Chinos', 'Ceintures & maroquinerie']

keywords_tags = {
    # French keywords
    'militaire': 'Style : Militaire 🪖',
    'camouflage': 'Style : Militaire 🪖',
    'armée': 'Style : Militaire 🪖',
    'kaki': 'Style : Militaire 🪖',
    'treillis': 'Style : Militaire 🪖',
    'uniforme': 'Style : Militaire 🪖',
    'para': 'Style : Militaire 🪖',
    'commando': 'Style : Militaire 🪖',
    'béret': 'Style : Militaire 🪖',
    # Italian keywords
    'militare': 'Style : Militaire 🪖',
    'camuffamento': 'Style : Militaire 🪖',
    'esercito': 'Style : Militaire 🪖',
    'kaki': 'Style : Militaire 🪖',
    'tuta': 'Style : Militaire 🪖',
    'uniforme': 'Style : Militaire 🪖',
    'paracadutista': 'Style : Militaire 🪖',
    'commando': 'Style : Militaire 🪖',
    'berretto': 'Style : Militaire 🪖',
    # English keywords
    'military': 'Style : Militaire 🪖',
    'camouflage': 'Style : Militaire 🪖',
    'army': 'Style : Militaire 🪖',
    'khaki': 'Style : Militaire 🪖',
    'uniform': 'Style : Militaire 🪖',
    'paratrooper': 'Style : Militaire 🪖',
    'commando': 'Style : Militaire 🪖',
    'beret': 'Style : Militaire 🪖',
    #other keywords
    'rayé': 'Style : Rayures',
    'texturé': 'Style : Texturé',
    'velour': 'Style : Mat',
    'daim': 'Style : Mat',
    'vellusto': 'Style : Mat',
    'cotelé':'Style : Mat',
    'cotelé':'Style : Texturé',
    'a coste':'Style : Texturé',
    'a coste':'Style : Texturé',
    'righe':'Style : Rayé',
    'rayures': 'Style : Rayures',
    'carreaux': 'Carreaux'
}


light_colors = ["BLANC", "CRÈME", "BEIGE", "ABRICOT", "ORANGE", "CORAIL", "ROSE", "ROSE FUSHIA", "LILA", "BLEU CLAIR", "TURQUOISE", "MENTHE", "MOUTARDE", "JAUNE", "ARGENT"]
dark_colors = ["NOIR", "GRIS", "ROUGE", "BORDEAUX", "VIOLET", "BLEU", "MARINE", "VERT", "VERT FONCÉ", "KAKI", "MARRON", "DORÉ"]
multicolor = ["MULTICOLORE"]




# Prepare an empty dictionary to store the new data
data = {
    'item_link': [],
    'raindrop_id': [],
    'raindrop_last_update': [],
    'raindrop_collection_id': []
}


# Read the item data file into a DataFrame
item_data_df = pd.read_csv('../Assets/Data/item_data_scrapped_from_vinted.csv')


for index, row in item_data_df.iterrows():

    # Only process rows with status 'validated'
    if row['status'] == 'validated':
        # Prepare tags for the API request
        colors = [f"Couleur : {color.strip().lower()}" for color in row['item_color'].split(',')]
        size = "Taille " + row['item_size'].split('\n')[0]  # Format size to 'Taille X'
        brand = f"Marque : {row['item_brand'].lower()}",
        tags = [brand, size] + colors

        # Check if color, size, or brand tags exist, if not create new ones
        for tag in tags:
            if tag not in tags_list:
                tags_list.append(tag)


        # Check if the item's category is formal or casual
        if any(category in row['raindrop_collection'] for category in formal_categories):
            tags.append('Style : Formel')
        if any(category in row['raindrop_collection'] for category in casual_categories):
            tags.append('Style : Casual ✌🏻')

        # Check for keywords
        for keyword, tag in keywords_tags.items():
            if keyword in row['item_description']:
                tags.append(tag)
        # Check for keywords in title
        for keyword, tag in keywords_tags.items():
            if keyword in row['item_title']:
                tags.append(tag)

        #Check for the color tone
        if any(color in row['item_color'] for color in light_colors):
            tags.append('Teinte : Lumineux ⬜️')
        if any(color in row['item_color'] for color in dark_colors):
            tags.append('Teinte : Sombre ⬛️')
        if any(color in row['item_color'] for color in multicolor):
            tags.append('Style : Multicolore')
        if len(['item_color']) == 1 :
            tags.append('Style : Uni')
        if row['item_color'] == 'Couleur : multicolore':
            tags.remove('Style : Uni')
            tags.append('Style : Motifs')
        if len(['item_color'])>1:
            tags.append('Style : Motifs')
        if 'Style : Rayures' in tags :
            tags.append('Style : Motifs')
        if 'Carreaux' in tags :
            tags.append('Style : Motifs')
        if 'jean' in row['item_description']:
            tags.append('Style : Denim')
        if 'jean' in row['item_title']:
            tags.append('Style : Denim')




        price = extract_number(row['item_price'])
        price_tag = f'Prix : {get_price_tag(price)}'
        tags.append(price_tag)

        try:
            id_float = float(row['raindrop_collection'])
            id_int = int(id_float)
            id_str = str(id_int)
        except:
            id_float = float(row['raindrop_collection_id'])
            id_int = int(id_float)
            id_str = str(id_int)


        item_pictures = ast.literal_eval(row['item_picture'])
        new_item_pictures = []

        for item_picture in item_pictures:
            item_dict = {"link": item_picture}
            new_item_pictures.append(item_dict)

        item_pictures = new_item_pictures

        # Prepare the data for the API request
        data_for_request = {
            'collection': {
                '$id': id_str,
                'access': True
            },
            'excerpt': row['item_description'],
            'title': row['item_title'],
            'link': row['item_link'],
            'tags': tags,
            'description': row['item_description'],
            'media': item_pictures
        }

        # Make the API request to create a new Raindrop
        response = requests.post(API_URL, headers=headers, json=data_for_request)

        if response.status_code == 200:
            try:
                response_json = response.json()

                # Save the new Raindrop ID and other data
                raindrop_id = response_json['item']['_id']
                raindrop_last_update = response_json['item']['lastUpdate']
                status = 'available'

                # Update the row in the DataFrame
                item_data_df.loc[index, ['raindrop_id', 'raindrop_last_update',
                                         'status']] = raindrop_id, raindrop_last_update, status
                time.sleep(0.5)

            except ValueError:
                print("JSON decoding failed. Raw response content:")
                print(response.content)

        else:
            print(f"Request failed with status code {response.status_code}. Raw response content:")
            print(response.content)
print(len(item_data_df))
# Write the DataFrame back out to the file
item_data_df.to_csv('../Assets/Data/item_data_scrapped_from_vinted.csv', index=False)