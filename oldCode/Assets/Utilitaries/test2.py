
import streamlit as st
import pandas as pd
import json
import time
import requests
import ast

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

def display_item(df, item_index):
    csv_row_number = item_index + 2  # Adjust for 0-based indexing and header row
    st.write(f"CSV row number: {csv_row_number}")
    st.write(f"Item title: {df.loc[item_index, 'item_title']}")

    # Parse the list of image URLs from the 'item_picture' column
    image_urls = json.loads(df.loc[item_index, 'item_picture'].replace("'", "\""))

    # Remove duplicate image URLs
    unique_image_urls = list(set(image_urls))

    # Display images in a grid with a maximum of 3 columns per row
    max_columns = 3
    row_count = -(-len(unique_image_urls) // max_columns)  # Ceiling division

    for row in range(row_count):
        cols = st.columns(max_columns)
        for col in range(max_columns):
            index = row * max_columns + col
            if index < len(unique_image_urls):
                cols[col].write(
                    f'<img src="{unique_image_urls[index]}" style="width: 100%; height: auto; object-fit: contain;">',
                    unsafe_allow_html=True)
    st.write(f"Item price: {df.loc[item_index, 'item_price']}")

    like_button = st.button(f"Like {df.loc[item_index, 'item_title']}")
    dislike_button = st.button(f"Dislike {df.loc[item_index, 'item_title']}")

    if like_button:

        # Prepare tags for the API request
        colors = [f"Couleur : {color.strip().lower()}" for color in df.loc[item_index,'item_color'].split(',')]

        size = "Taille " + df.loc[item_index,'item_size'].split('\n')[0]  # Format size to 'Taille X'
        brand = f"Marque : {df.loc[item_index,'item_brand'].lower()}",
        tags = [brand, size] + colors

        # Check if color, size, or brand tags exist, if not create new ones
        for tag in tags:
            if tag not in tags_list:
                tags_list.append(tag)

        # Check if the item's category is formal or casual
        if any(category in df.loc[item_index,'raindrop_collection'] for category in formal_categories):
            tags.append('Style : Formel')
        if any(category in df.loc[item_index,'raindrop_collection'] for category in casual_categories):
            tags.append('Style : Casual ✌🏻')

        # Check for keywords
        for keyword, tag in keywords_tags.items():
            if keyword in df.loc[item_index,'item_description']:
                tags.append(tag)
        # Check for keywords in title
        for keyword, tag in keywords_tags.items():
            if keyword in df.loc[item_index,'item_title']:
                tags.append(tag)

        # Check for the color tone
        if any(color in df.loc[item_index,'item_color'] for color in light_colors):
            tags.append('Teinte : Lumineux ⬜️')
        if any(color in df.loc[item_index,'item_color'] for color in dark_colors):
            tags.append('Teinte : Sombre ⬛️')
        if any(color in df.loc[item_index,'item_color'] for color in multicolor):
            tags.append('Style : Multicolore')
        if len(['item_color']) == 1:
            tags.append('Style : Uni')
        if df.loc[item_index,'item_color'] == 'Couleur : multicolore':
            tags.remove('Style : Uni')
            tags.append('Style : Motifs')
        if len(['item_color']) > 1:
            tags.append('Style : Motifs')
        if 'Style : Rayures' in tags:
            tags.append('Style : Motifs')
        if 'Carreaux' in tags:
            tags.append('Style : Motifs')
        if 'jean' in df.loc[item_index,'item_description']:
            tags.append('Style : Denim')
        if 'jean' in df.loc[item_index,'item_title']:
            tags.append('Style : Denim')

        price = extract_number(df.loc[item_index,'item_price'])
        price_tag = f'Prix : {get_price_tag(price)}'
        tags.append(price_tag)

        try:
            id_float = float(df.loc[item_index,'raindrop_collection'])
            id_int = int(id_float)
            id_str = str(id_int)
        except:
            id_float = float(df.loc[item_index,'raindrop_collection_id'])
            id_int = int(id_float)
            id_str = str(id_int)

        item_pictures = ast.literal_eval(df.loc[item_index,'item_picture'])
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
            'excerpt': df.loc[item_index,'item_description'],
            'title': df.loc[item_index,'item_title'],
            'link': df.loc[item_index,'item_link'],
            'tags': tags,
            'description': df.loc[item_index,'item_description'],
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
                df.loc[item_index, 'status'] = 'available'
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


    if dislike_button:
        df.loc[item_index, 'status'] = 'rejected'


    return False

st.title('Review Items')

# Replace 'your_file_path.csv' with the actual file path of your CSV file
file_path = '../Assets/Data/item_data_scrapped_from_vinted.csv'

# Load the existing CSV file or create a new DataFrame
df = pd.read_csv(file_path)

pending_items = df[df['status'] == 'pending']
validated_items = df[df['status'] == 'validated']
rejected_items = df[df['status'] == 'rejected']

st.write(f"Pending items: {len(pending_items)}")
st.write(f"Validated items: {len(validated_items)}")
st.write(f"Rejected items: {len(rejected_items)}")

if 'current_item_index' not in st.session_state:
    st.session_state.current_item_index = 0

pending_item_indexes = pending_items.index.tolist()

if pending_item_indexes:
    current_item_index = pending_item_indexes[st.session_state.current_item_index]
    if display_item(df, current_item_index):
        st.session_state.current_item_index += 1
        if st.session_state.current_item_index >= len(pending_item_indexes):
            st.session_state.current_item_index = 0

    # Save the DataFrame after every interaction
    df.to_csv(file_path, index=False)
