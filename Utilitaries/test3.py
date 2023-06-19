import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import datetime
from datetime import date
import time
import sys
import re

# Define the web browser's options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_argument("--headless")  # Hides the browser tabs
#chrome_options.add_argument("log-level=2")  # Hides the headless error messages from the console
chrome_options.add_argument(("--disable-gpu"))

# Define the function to open the item link in a new tab
def open_in_new_tab(driver, link):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

# Loads the progress bar to track the progress of 'i'
progress_file = "../Assets/Data/progress_bar_data.txt"
i = 0
cnt = 0
page = 1
duplicate = 0
with open(progress_file, "w") as f:
    f.write("0")  # Initialize the progress to 0

# Get the search parameters from the parent script
url = sys.argv[1]
pieces_a_chercher = int(sys.argv[2])
query = sys.argv[3]
session_token = sys.argv[4]
category = sys.argv[5]
category_id = sys.argv[6]

# Establish a connection to the PostgreSQL database
engine = create_engine('postgresql://postgres: @localhost/items_data_2')
Session = sessionmaker(bind=engine)
session = Session()

# Load existing item data from the PostgreSQL database to a DataFrame
existing_data = pd.read_sql_table('item', engine)


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





Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    item_title = Column(String)
    item_picture = Column(String)
    item_link = Column(String)
    item_color = Column(String)
    item_price = Column(Float)
    item_description = Column(String)
    item_size = Column(String)
    item_brand = Column(String)
    item_initial_views = Column(Integer)
    item_current_views = Column(Integer)
    item_initial_followers = Column(Integer)
    item_current_followers = Column(Integer)
    item_location = Column(String)
    item_date_added = Column(DateTime)
    date_scrapped = Column(DateTime)
    query = Column(String)
    session_token = Column(String)
    raindrop_collection = Column(String)
    raindrop_collection_id = Column(Integer)
    status = Column(String)

print("okay")

time.sleep(5)
# Defines the data list and loads every item's individual link on the Vinted search page
items = driver.find_elements(By.CLASS_NAME, 'new-item-box__overlay')
if len(items) < pieces_a_chercher:
    pieces_a_chercher = len(items)

print(len(items))

last_item_link = None

# Starts the scraping process
while i < pieces_a_chercher:
    if len(items) == 0:
        break

    first_item_link = items[0].get_attribute('href')

    if first_item_link == last_item_link :
        print("Articles déjà scannés")
        break

    # For every item's link located on the search result page...
    for item in items:
        # Break the while loop above if the number of items 'i' meets the specified number of items 'pieces_a_rechercher'
        if i >= pieces_a_chercher:
            break

        # Open said link in a new tab
        try:
            # Check if the item is a duplicate
            item_link = item.get_attribute('href')



            # Query the database to check if this item_link already exists
            already_exists = session.query(exists().where(Item.item_link == item_link)).scalar()

            if already_exists:
                print("duplicate")
                continue  # Skip this item if it's a duplicate

            open_in_new_tab(driver, item_link)  # Open the item link in a new tab
            print("not a duplicate, opening...")
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

                # Parse the string as day/month/year, 24-hour time
                item_date_added = datetime.datetime.strptime(item_date_added, "%d/%m/%Y, %H:%M:%S")

                # Format the datetime object to the standard format ("YYYY-MM-DD HH:MM:SS")
                item_date_added = item_date_added.strftime("%Y-%m-%d %H:%M:%S")

                try:
                    item_followers_format = "1 UTILISATEUR"
                    item_followers = int(re.search(r'\d+', item_followers_format).group())
                except NoSuchElementException:
                    item_followers = "0"

                print("saving...")

                try:
                    #Inside your scraping loop
                    new_item = Item(
                        item_title=item_title,
                        item_picture=str(img_links),  # Convert the list to string if you are storing it in one column
                        item_link=item_link,
                        item_color=item_color,
                        item_price=item_price,
                        item_description=item_description,
                        item_size=item_size,
                        item_brand=item_brand,
                        item_initial_views=item_views,
                        item_current_views=item_views,
                        item_initial_followers=item_followers,
                        item_current_followers=item_followers,
                        item_location=item_location,
                        item_date_added=item_date_added,
                        date_scrapped=date.today().strftime("%Y-%m-%d %H:%M:%S"),
                        query=query,
                        session_token=session_token,
                        raindrop_collection=category,
                        raindrop_collection_id=category_id,
                        status="pending",
                    )

                    session.add(new_item)
                    session.commit()

                except Exception as e:
                    print("Error inserting item data into the PostgreSQL database:", e)



                # Increment the progress counter 'i'
                i += 1


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
    if i < pieces_a_chercher:
        last_item_link = items[0].get_attribute('href')
        page += 1
        driver.get(url + f"?page={page}")
        print(f"next page {page}")
    else:
        break

    # Wait for the page to load and get the new items' links
    time.sleep(5)
    items = driver.find_elements(By.CLASS_NAME, 'new-item-box__overlay')

# Close the web browser
driver.quit()

# Close the PostgreSQL connection
session.close()

print(f"Items scrapped: {i}")
