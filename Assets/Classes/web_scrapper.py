from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Browser:


class WebScraper:
    def __init__(self, chrome_options=None):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

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

    def get_item_links(self, item_count):
        items = self.driver.find_elements(By.CLASS_NAME, 'new-item-box__overlay')
        return [item.get_attribute('href') for item in items[:item_count]]

    def extract_item_info(self, item_link):
        # Open link in a new tab
        self.open_in_new_tab(item_link)

        # Initialize empty dictionary to store item properties
        item_properties = {}

        # Extract item title
        try:
            item_properties["title"] = self.driver.find_element(By.CSS_SELECTOR,
                                                                "div div div div div div div div div div[itemprop='name'] h2").text
        except NoSuchElementException:
            item_properties["title"] = None

        # Extract item brand
        try:
            item_properties["brand"] = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div div div div div div div div[itemprop='brand'] a span"))).text
        except NoSuchElementException:
            item_properties["brand"] = None

        # Extract item color
        try:
            item_properties["color"] = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "div div div div div div div div[data-testid='item-attributes-color'] div[class='details-list__item-value']"))).text
        except NoSuchElementException:
            item_properties["color"] = None

        # Extract item price
        try:
            item_price = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__heading.web_ui__Text__left"))).text
            item_price = item_price.replace(',', '').replace(' €', '')
            item_properties["price"] = float(item_price)
        except NoSuchElementException:
            item_properties["price"] = None

        # Extract item description
        try:
            item_properties["description"] = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div div div div div div div div div[itemprop='description']"))).text
        except NoSuchElementException:
            item_properties["description"] = None

        # Extract item size
        try:
            item_properties["size"] = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div div div div div div div div div[itemprop='size']"))).text
        except NoSuchElementException:
            item_properties["size"] = None

        # Extract item views
        try:
            item_properties["views"] = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text
        except NoSuchElementException:
            item_properties["views"] = None

        # Extract item location
        try:
            item_properties["location"] = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                          "div div div div div div div div[data-testid='item-details-location'] div[class='details-list__item-value']"))).text
        except NoSuchElementException:
            item_properties["location"] = None

        # Extract item date added
        try:
            item_date_added = self.driver.find_element(By.CSS_SELECTOR,
                                                       "div div div div div div [data-testid='item-details-uploaded_date'] div[class='details-list__item-value'] div span").get_attribute(
                'title')
            item_date_added = datetime.datetime.strptime(item_date_added, "%Y-%m-%dT%H:%M:%S.%fZ")
            item_properties["date_added"] = item_date_added
        except NoSuchElementException:
            item_properties["date_added"] = None

        # Close the current tab and switch back to the search result page
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Return the dictionary with item properties
        return item_properties
