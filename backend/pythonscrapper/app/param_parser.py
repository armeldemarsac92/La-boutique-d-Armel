import requests as request
from utils.queue import Queue
from utils.api import Api

data_queue = Queue(queue_name='item_data')
parameters_queue = Queue(queue_name='parameters_queue')

api_connection = Api('https://www.vinted.fr','http://127.0.0.1:24001')

parameters_queue.listen(api_connection=api_connection, item_queue=data_queue)