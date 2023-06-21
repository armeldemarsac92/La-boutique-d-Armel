from Assets.Classes.web_scrapper import WebScraper, Browser, ProgressTracking, NextPage
from Assets.Classes.sql_handler import Item, DatabaseHandler



# Define the database model
scraper = WebScraper()
browser = Browser()
db_handler = DatabaseHandler('postgresql://postgres: @localhost/items_data_2')
tracker = ProgressTracking()
next_page = NextPage()


# Get the search parameters from the parent script
url = "https://www.vinted.fr/catalog?search_text=&catalog[]=2538&size_id[]=209" #sys.argv[1]
pieces_a_chercher = 10 #int(sys.argv[2])
query = "test"#sys.argv[3]
session_token = 4000 #sys.argv[4]
category = "test" #sys.argv[5]
category_id = 100000 #sys.argv[6]

i=0
page=1

item_links = browser.get_item_links(url, db_handler, pieces_a_chercher)

while i < pieces_a_chercher:

    for item in item_links:

        item_data={}
        item_data = scraper.extract_item_info(item,session_token,query,category,category_id)
        print(item_data)


        try:
            # Inside your scraping loop
            new_item = Item(item_data)
            db_handler.add_item(new_item)

        except Exception as e:
            print("Error inserting item data into the PostgreSQL database:", e)

        # Increment the progress counter 'i'
        i += 1

        tracker.update_progress(i)

    if i < pieces_a_chercher:
        next_page.advance(page,url)
    else:
        break







# Your scraping logic starts here, using methods of the scraper object.
# Example:
# scraper.open_in_new_tab(your_link)
# Here you would call the methods to extract information and save it in the database.

# After finishing the scraping logic, close the resources
