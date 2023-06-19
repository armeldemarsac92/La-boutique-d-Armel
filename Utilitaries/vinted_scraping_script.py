import psycopg2 as psy
from psycopg2 import Error
import pandas as pd
import time
import datetime
from datetime import date
import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Define the web browser's options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_argument("--headless")  # Hides the browser tabs
chrome_options.add_argument("log-level=2")  # Hides the headless error messages from the console
chrome_options.add_argument(("--disable-gpu"))
logging.getLogger('tensorflow').disabled = True

# Define the function to open the item link in a new tab
def open_in_new_tab(link):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

# Loads the progress bar to track the progress of 'i'
progress_file = "../Assets/Data/progress_bar_data.txt"
i = 0
page = 1
with open(progress_file, "w") as f:
    f.write("0")  # Initialize the progress to 0

# Get the search parameters from the parent script
url = sys.argv[1]
pieces_a_chercher = int(sys.argv[2])
query = sys.argv[3]
session_token = sys.argv[4]
category = sys.argv[5]
category_id = sys.argv[6]

# Open the web browser and search
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
try:
    # Define the wait instance, wait for the cookie accept button to load, then click on it
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
except TimeoutException:
    # print("Pas de cookie notice")
    pass

# Halt for the page to load
time.sleep(5)

# Establish a connection to the PostgreSQL database
try:
    connection = psy.connect(
        host="localhost",
        database="items_data",
        user="postgres",
        password=" "
    )
except Error as e:
    print("Error connecting to PostgreSQL database:", e)
    sys.exit(1)

# Create a cursor object
cursor = connection.cursor()

# Load existing item data from the PostgreSQL database to a DataFrame
existing_data_query = "SELECT * FROM items"
existing_data = pd.read_sql_query(existing_data_query, connection)

# Defines the data list and loads every item's individual link on the Vinted search page
data = []
items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')
if len(items) < pieces_a_chercher:
    pieces_a_chercher = len(items)

# Starts the scraping process
while i < pieces_a_chercher:
    if len(items) == 0:
        break

    # For every item's link located on the search result page...
    for item in items:
        # Break the while loop above if the number of items 'i' meets the specified number of items 'pieces_a_rechercher'
        if i >= pieces_a_chercher:
            break

        # Open said link in a new tab
        try:
            # Check if the item is a duplicate
            item_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if item_link in existing_data['item_link'].values:
                continue  # Skip this item if it's a duplicate
            open_in_new_tab(item_link)  # Open the item link in a new tab

            try:
                # Define the images links to fetch and store them in the img_links list
                try:
                    img_links = []
                    imgs = driver.find_elements(By.CSS_SELECTOR, "div div div div div div [class='web_ui__Image__image web_ui__Image__cover web_ui__Image__scaled']")
                    for img in imgs:
                        img_link = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        img_links.append(img_link)
                except Exception as e:
                    print(f"Erreur dans la collecte des images : {e}")

                item_title = driver.find_element(By.CSS_SELECTOR, "div div div div div div div div div div[itemprop='name'] h2").text

                item_brand = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[itemprop='brand'] a span"))).text

                try:
                    item_color = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-attributes-color'] div[class='details-list__item-value']"))).text
                except:
                    item_color = "pas de couleur"

                item_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__heading.web_ui__Text__left"))).text
                # Assuming you have a variable named "price" containing the value "10,00 €"
                # Remove the comma and euro symbol from the price value
                item_price = item_price.replace(',', '').replace(' €', '')

                # Convert the price value to a float
                item_price = float(item_price)


                item_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div[itemprop='description']"))).text

                try:
                    item_size = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div[itemprop='size']"))).text
                except:
                    item_size = "pas de taille"

                item_views = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text

                item_location = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-details-location'] div[class='details-list__item-value']"))).text

                item_date_added = driver.find_element(By.CSS_SELECTOR, "div div div div div div [data-testid='item-details-uploaded_date'] div[class='details-list__item-value'] div span").get_attribute('title')

                # Assuming you have a variable named "timestamp" containing the value "5/20/2023, 5:18:52 PM"
                # Convert the timestamp value to a datetime object
                item_date_added = datetime.datetime.strptime(item_date_added, "%m/%d/%Y, %I:%M:%S %p")

                # Format the datetime object to the desired format ("YYYY-MM-DD HH:MI:SS")
                item_date_added = item_date_added.strftime("%Y-%m-%d %H:%M:%S")

                date_scrapped = date.today().strftime("%Y-%m-%d %H:%M:%S")


                try:
                    item_followers = driver.find_element(By.CSS_SELECTOR, "div div div div div div div [data-testid='item-details-interested_count'] div[class='details-list__item-value']").text
                    item_followers = item_followers.replace(" UTILISATEURS","")
                except NoSuchElementException:
                    item_followers = "0"

                # Appends the list "data" defined before the while loop with the item's data
                data.append({
                    'item_title': item_title,
                    'item_picture': img_links,
                    'item_link': item_link,
                    'item_brand': item_brand,
                    'item_color': item_color,
                    'item_price': item_price,
                    'item_description': item_description,
                    'item_size': item_size,
                    'item_initial_views': str(item_views),
                    'item_current_views': str(item_views),
                    'item_location': item_location,
                    'item_date_added': item_date_added,
                    'date_scrapped' : date_scrapped,
                    'status' : "pending",
                    'item_initial_followers': str(item_followers),
                    'item_current_followers': str(item_followers),
                    'query': query,
                    'session_token': session_token,
                    'category': category,
                    'category_id': category_id
                })

                # Insert the item data into the PostgreSQL database
                try:
                    cursor.execute("""
                        INSERT INTO items (
                            item_title,
                            item_picture,
                            item_link,
                            item_brand,
                            item_color,
                            item_price,
                            item_description,
                            item_size,
                            item_initial_views,
                            item_current_views,
                            item_location,
                            item_date_added,
                            date_scrapped,
                            status,
                            item_initial_followers,
                            item_current_followers,
                            query,
                            session_token,
                            raindrop_collection,
                            raindrop_collection_id
                        ) VALUES (
                            %(item_title)s,
                            %(item_picture)s,
                            %(item_link)s,
                            %(item_brand)s,
                            %(item_color)s,
                            %(item_price)s,
                            %(item_description)s,
                            %(item_size)s,
                            %(item_initial_views)s,
                            %(item_current_views)s,
                            %(item_location)s,
                            %(item_date_added)s,
                            %(date_scrapped)s,
                            %(status)s,
                            %(item_initial_followers)s,
                            %(item_current_followers)s,
                            %(query)s,
                            %(session_token)s,
                            %(category)s,
                            %(category_id)s
                        )
                    """, data[-1])
                    connection.commit()
                except Error as e:
                    print("Error inserting item data into the PostgreSQL database:", e)

                # Increment the progress counter 'i'
                i += 1
                print(f"Items scrapped: {i}/{pieces_a_chercher}")

                # Update the progress file with the current progress 'i'
                with open(progress_file, "w") as f:
                    f.write(str(i))
            except Exception as e:
                print(f"Erreur de la collecte d'un item : {e}")

        except Exception as e:
            print(
                f"Le navigateur n'a pas réussi à ouvrir le lien dans un nouvel onglet, message d'erreur: {e}. Lien suivant.")
            continue

        # Close the current tab and switch back to the search result page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # Move to the next search result page
    page += 1
    driver.get(url + f"?page={page}")

    # Wait for the page to load and get the new items' links
    time.sleep(5)
    items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')

# Close the web browser
driver.quit()

# Close the PostgreSQL connection
cursor.close()
connection.close()

