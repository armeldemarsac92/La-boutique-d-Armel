from utils.queue import Queue
from utils.scrapper import WebScraper

queue = Queue()
proxyprod = "http://backend-proxymanager-1:24000"
proxy = 'http://127.0.0.1:24001'

def main():
    browser = WebScraper(proxy)
    try:
        print(browser.extract_item_info('https://www.vinted.fr/items/3695546794-parka?referrer=catalog'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
