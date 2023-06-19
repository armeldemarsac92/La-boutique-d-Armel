import datetime
import pandas as pd
import re
import sys
import time
from Assets.Classes.web_scrapper import WebScraper
from Assets.Classes.sql_handler import Item, DatabaseHandler
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, exists
from sqlalchemy.orm import sessionmaker, declarative_base


# Define the database model
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

# Define the web browser's options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Establish a connection to the PostgreSQL database
engine = create_engine('postgresql://postgres: @localhost/items_data_2')
Session = sessionmaker(bind=engine)
db_session = Session()

# Open the web browser and search
driver = webdriver.Chrome(options=chrome_options)
scraper = WebScraper(driver)

# Get the search parameters from the parent script
url = sys.argv[1]
pieces_a_chercher = int(sys.argv[2])
query = sys.argv[3]
session_token = sys.argv[4]
category = sys.argv[5]
category_id = sys.argv[6]

item_links = scraper.get_item_links(pieces_a_chercher)

items = scraper.extract_item_info(item_links)

for item in items:




# Your scraping logic starts here, using methods of the scraper object.
# Example:
# scraper.open_in_new_tab(your_link)
# Here you would call the methods to extract information and save it in the database.

# After finishing the scraping logic, close the resources
driver.quit()
db_session.close()
