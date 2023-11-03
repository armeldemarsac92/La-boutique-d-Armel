from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import date
import datetime
import re


class Browser:
    def __init__(self, chrome_options=None):
        if chrome_options is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        # Rest of the class methods...

    def open_in_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(link)

    def accept_cookies(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            element.click()
        except TimeoutException:
            pass

    def get_item_links(self,url, db_handler, item_count):
        self.open_in_new_tab(url)
        self.accept_cookies()
        items_list = []
        while len(items_list)<item_count:
            items = self.driver.find_elements(By.CLASS_NAME, 'new-item-box__overlay')
            for item in items:
                item_link = item.get_attribute('href')
                if db_handler.item_exists(item_link):
                    continue
                items_list.append(item_link)
            if len(item_link)<item_count:
                self.Nextpage.advance(url)

        return items_list[:item_count]


class WebScraper:
    def __init__(self):
        self.browser = Browser()

    def extract_item_info(self, item_link, session_token, query, raindrop_collection, raindrop_collection_id):
        # Open link in a new tab
        self.browser.open_in_new_tab(item_link)
        self.browser.accept_cookies()

        # Initialize empty dictionary to store item properties
        item_properties = {}

        # Stores the arguments passed from the parent script
        item_properties['session_token'] = session_token

        item_properties['query'] = query

        item_properties['raindrop_collection'] = raindrop_collection

        item_properties['raindrop_collection_id'] = raindrop_collection_id

        item_properties['item_link'] = item_link

        item_properties['status'] = 'pending'

        try:
            item_properties['item_picture'] = []
            imgs = self.browser.driver.find_elements(By.CSS_SELECTOR,
                                        "div div div div div div [class='web_ui__Image__image web_ui__Image__cover web_ui__Image__scaled']")
            for img in imgs:
                img_link = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                item_properties['item_picture'].append(img_link)

        except :
            item_properties['item_picture'] = None
        # Extract item title
        try:
            item_properties["title"] = self.browser.driver.find_element(By.CSS_SELECTOR,
                                                                "div div div div div div div div div div[itemprop='name'] h2").text
        except :
            item_properties["title"] = None

        # Extract item brand
        try:
            item_properties["brand"] = self.browser.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div div div div div div div div[itemprop='brand'] a span"))).text
        except :
            item_properties["brand"] = None

        # Extract item color
        try:
            item_properties["color"] = self.browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,                                                                                  "div div div div div div div div[data-testid='item-attributes-color'] div[class='details-list__item-value']"))).text
        except :
            item_properties["color"] = None

        # Extract item price
        try:
            item_price = self.browser.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__heading.web_ui__Text__left"))).text
            item_price = item_price.replace(',', '.').replace(' €', '')
            item_properties["price"] = float(item_price)
        except :
            item_properties["price"] = None

        # Extract item description
        try:
            item_properties["description"] = self.browser.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div div div div div div div div div[itemprop='description']"))).text
        except :
            item_properties["description"] = None

        # Extract item size
        try:
            item_properties["size"] = self.browser.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div div div div div div div div div[itemprop='size']"))).text
            item_properties['size'].replace('\nSIZE INFORMATION','')
        except :
            item_properties["size"] = None

        # Extract item views
        try:
            item_properties["views"] = self.browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,                                                                                  "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text
        except :
            item_properties["views"] = None

        # Extract item followers
        try:
            item_followers_format = self.browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                            "div div div div div div div [data-testid='item-details-interested_count'] div[class='details-list__item-value']"))).text

            item_properties['followers'] = int(re.search(r'\d+', item_followers_format).group())
        except :
            item_properties['followers'] = '0'

        # Extract item location
        try:
            item_properties["location"] = self.browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div div div div div div div div[data-testid='item-details-location'] div[class='details-list__item-value']"))).text
        except :
            item_properties["location"] = None

        # Defines item date scrapped

        item_properties['date_scrapped'] = date.today().strftime("%Y-%m-%d %H:%M:%S")

        # Extract item date added
        try:
            item_date_added = self.browser.driver.find_element(By.CSS_SELECTOR,"div div div div div div [data-testid='item-details-uploaded_date'] div[class='details-list__item-value'] div span").get_attribute('title')
            # Parse the string as day/month/year, 24-hour time
            item_date_added = datetime.datetime.strptime(item_date_added, "%d/%m/%Y, %H:%M:%S")
            # Format the datetime object to the standard format ("YYYY-MM-DD HH:MM:SS")
            item_date_added = item_date_added.strftime("%Y-%m-%d %H:%M:%S")
            item_properties["date_added"] = item_date_added
        except :
            item_properties["date_added"] = None


        # Close the current tab and switch back to the search result page
        self.browser.driver.close()
        self.browser.driver.switch_to.window(self.browser.driver.window_handles[0])

        # Return the dictionary with item properties
        return item_properties

class ProgressTracking:
    def __init__(self):
        with open("../Assets/Data/progress_bar_data.txt", "w") as f:
            f.write("0")

    def update_progress(self, progress_value, progress_file="../Assets/Data/progress_bar_data.txt"):
        with open(progress_file, "w") as f:
            f.write(str(progress_value))

class NextPage:

    def advance(self,page, url):
        # Move to the next search result page
        page += 1
        self.driver.get(url + f"?page={page}")
        print(f"next page {page}")

