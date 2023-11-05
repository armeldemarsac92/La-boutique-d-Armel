from utils.queue import Queue

queue = Queue(queue_name='parameters_queue')



item = {}

item['url'] = 'https://www.vinted.fr/items/3625552434-womens-olive-green-barbour-lightweight-acorn-8-slim-wax-jacket-veste-ciree-cintree'

queue.publish(item, 'fetch_parameters')

#https://www.vinted.fr/api/v2/catalog/items?page=1&per_page=96&search_text=barbour&catalog_ids=1206&price_from=40&price_to=70&currency=EUR&color_ids=16&brand_ids=46805&size_ids=208&material_ids=&video_game_rating_ids=&status_ids=2

