import pandas as pd
import logging
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm

# defines the web browser's options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_argument("--headless")  # hides the browser tabs
chrome_options.add_argument("log-level=2")  # hides the headless error messages from the console
chrome_options.add_argument("disable-gpu")
logging.getLogger('tensorflow').disabled = True

driver = webdriver.Chrome(options=chrome_options)

# Load existing CSV file into a DataFrame
file_path = '../Assets/Data/item_data_scrapped_from_vinted6.csv'
existing_df = pd.read_csv(file_path)
print(len(existing_df))

# Filter the DataFrame to select items with "available" status
available_items_df = existing_df[existing_df['status'] == 'available']
print("df chargé")

# Get the item links from the filtered DataFrame
items = available_items_df['item_link'].tolist()
print(f"il y a {len(items)}")

i = 0
sold_count=0
updated_count=0
added_count=0

# Starts the scraping process
for item_link in tqdm(items):

    # Find the index of the item in the DataFrame
    item_index = existing_df[existing_df['item_link'] == item_link].index[0]

    try:
        # Open the item link in a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(item_link)

        if i == 0:
            # Define the wait instance, waits for the cookie accept button to load then clicks on it
            try:
                wait = WebDriverWait(driver, 3)
                element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
                element.click()
            except:
                print("pas de cookie notice")
                pass

        try:
            wait = WebDriverWait(driver, 3)
            item_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div div div div div div div div div div[itemprop='name'] h2"))).text

            if existing_df.at[item_index, 'item_title'] == "":

                try:
                    img_links = []
                    imgs = driver.find_elements(By.CSS_SELECTOR,
                                                "div div div div div div [class='web_ui__Image__image web_ui__Image__cover web_ui__Image__scaled']")
                    for img in imgs:
                        img_link = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        img_links.append(img_link)
                except Exception as e:
                    print(f"Erreur dans la collecte des images : {e}")

                item_brand = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div div div div div div div div[itemprop='brand'] a span"))).text

                try:
                    item_color = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                            "div div div div div div div div[data-testid='item-attributes-color'] div[class='details-list__item-value']"))).text
                except:
                    item_color = "pas de couleur"

                item_price = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__heading.web_ui__Text__left"))).text

                item_description = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div div div div div div div div div[itemprop='description']"))).text

                try:
                    item_size = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div div div div div div div div div[itemprop='size']"))).text
                except:
                    item_size = "pas de taille"

                item_views = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text

                item_location = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                           "div div div div div div div div[data-testid='item-details-location'] div[class='details-list__item-value']"))).text

                item_date_added = driver.find_element(By.CSS_SELECTOR,
                                                      "div div div div div div [data-testid='item-details-uploaded_date'] div[class='details-list__item-value'] div span").get_attribute(
                    'title')

                try:
                    item_followers = driver.find_element(By.CSS_SELECTOR,
                                                         "div div div div div div div [data-testid='item-details-interested_count'] div[class='details-list__item-value']").text
                except NoSuchElementException:
                    item_followers = "0 membre intéressé"

                # Update the fields in the DataFrame with the scraped data
                existing_df.at[item_index, 'item_title'] = item_title
                existing_df.at[item_index, 'item_picture'] = str(img_links)
                existing_df.at[item_index, 'item_brand'] = item_brand
                existing_df.at[item_index, 'item_color'] = item_color
                existing_df.at[item_index, 'item_price'] = item_price
                existing_df.at[item_index, 'item_description'] = item_description
                existing_df.at[item_index, 'item_size'] = item_size
                existing_df.at[item_index, 'item_initial_views'] = str(item_views)
                existing_df.at[item_index, 'item_location'] = item_location
                existing_df.at[item_index, 'item_date_added'] = item_date_added
                existing_df.at[item_index, 'item_initial_followers'] = str(item_followers)

                state = "Données produit ajoutées"
                added_count += 1


            else:

                item_current_views = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text
                try:
                    item_current_followers = driver.find_element(By.CSS_SELECTOR,
                                                         "div div div div div div div [data-testid='item-details-interested_count'] div[class='details-list__item-value']").text
                except NoSuchElementException:
                    item_current_followers = "0 membre intéressé"

                existing_df.at[item_index, 'item_current_followers'] = str(item_current_followers)
                existing_df.at[item_index, 'item_current_views'] = str(item_current_views)

                state = "Vues et likes actualisés"
                updated_count += 1

        except TimeoutException:

            # This item is sold. adding tag "vendu" to it
            existing_df.at[item_index, 'status'] = 'sold'
            existing_df.at[item_index, 'item_date_sold'] = dt.today().strftime("%d/%m/%Y")

            state="Article vendu"
            sold_count += 1

        #saving process, closing tab

        i += 1

        if i % 20 == 0:
            # Write the updated DataFrame back to the CSV file
            existing_df.to_csv(file_path, index=False)
            print("Sauvegarde des données...")

        # Close the current tab
        driver.close()
        print(f"{state}, fermeture de la fenêtre.")

        # Switch back to the main tab
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"Le navigateur n'a pas réussi à ouvrir le lien dans un nouvel onglet, message d'erreur: {e}. Lien suivant.")
        continue

# Write the updated DataFrame back to the CSV file
existing_df.to_csv(file_path, index=False)

# Close the webdriver
driver.quit()

print(f"Mise à jour des données effectuée : {sold_count} article(s) vendu(s), {updated_count} article(s) mis à jour, {added_count} articles ajoutés.")


