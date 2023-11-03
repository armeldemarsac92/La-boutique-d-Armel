import requests as request
import json
from utils.queue import Queue
from utils.api import Api

url_queue = Queue(queue_name='item_urls')
item_queue = Queue(queue_name='item_data')

api_connection = Api('https://www.vinted.fr','http://proxymanager:24000')

item_queue.publish("hello", "test")
url_queue.listen(api_connection=api_connection, item_queue=item_queue)



