import requests as request
import json
from utils.queue import Queue

queue = Queue()

proxies = {
    "https": "http://127.0.0.1:24001",
}

response = request.get('https://vinted.fr', proxies=proxies, verify=False)

# Convert cookies to a dictionary
cookies_dict = request.utils.dict_from_cookiejar(response.cookies)

# Convert dictionary to JSON
cookies_json = json.dumps(cookies_dict)

item = request.get('https://www.vinted.fr/api/v2/items/3695546794?localize=fr', proxies=proxies, verify=False, cookies=cookies_dict)

item_json = item.json()

message = {}

message['message_type'] = 'save'

item_data = {}

item_data['item_title'] = item_json['item']['title']
item_data['item_price'] = item_json['item']['total_item_price']

message['items_data'] = item_data

item_data_serialized = json.dumps(message)

queue.publish(item_data_serialized)

#print("item price:", item_json["item"]["price_numeric"])


