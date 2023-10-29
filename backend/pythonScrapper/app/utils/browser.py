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
