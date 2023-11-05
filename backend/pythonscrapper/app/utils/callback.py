import json
import re

def extract_item_id(url):
    match = re.search(r'/items/(\d+)-', url)
    if match:
        return match.group(1)
    else:
        return None

def process_message(ch, method, properties, body, api_connection, item_queue):

    message = json.loads(body)
    print(f"Received message: {message}")

    if message['message_type'] == 'fetch_data':
        print('fetching data')
        try : 
            item_url = message['data']['url']
            message['item_id'] = extract_item_id(item_url)

        except Exception as e:
            print(f"Failed to extract data from message parameters, have you made changes to the message keys ? : {e}")
        
        try : 
            fetch_data(api_connection, item_queue, message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Failed to fetch data, check the proxy manager logs for more informations : {e}")

    elif message['message_type'] == 'fetch_parameters':
        print('fetching parameters')
        try :
            fetch_parameters(api_connection, item_queue)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Failed to fetch parameters, check the proxy manager logs for more informations : {e}")
       
        
    #elif message['message_type'] == 'fetch_urls':
        

def loop(item, paramlist):
    # Check if the 'catalog' key has items in it
    if 'catalogs' in item and len(item['catalogs']) > 0:
        for catalog_item in item['catalogs']:
            # Recursively call loop on each item in the catalog
            loop(catalog_item, paramlist)
    else:
        # Create a dictionary for parameters
        param = {}
        param['id'] = item.get('id', None)  # Use .get() to handle cases where 'id' might not exist
        param['title'] = item.get('title', None)  # Same as above for 'title'
        param['size_group_id'] = item.get('size_group_id', None)
        param['size_group_ids'] = []
        for size_id in item.get('size_group_ids'):
            param['size_group_ids'].append(size_id)
        param['item_count'] = item.get('item_count', None)
        # Append the dictionary to the list
        paramlist.append(param)

def fetch_parameters(api_connection, item_queue):
    # Call the API and get the response data
    response_data = api_connection.call("/api/v2/catalogs")
    # Initialize an empty list to collect parameter data
    parameter_data = []
    # Call the loop function with response data and the list to fill
    loop(response_data, parameter_data)
    # Return the collected parameter data
    for parameter in parameter_data:
        item_queue.publish(parameter, message_type = 'save')




def fetch_data(api_connection, item_queue, message):

    response_data = api_connection.call(f"/api/v2/items/{message['item_id']}?localize=fr")
    item_data = {}
    item_data['item_url'] = response_data['item']['url']
    item_data['item_title'] = response_data['item']['title']
    item_data['item_description'] = response_data['item']['description']
    item_data['item_size'] = response_data['item']['size']
    item_data['item_brand'] = response_data['item']['brand']
    item_data['item_price'] = response_data['item']['total_item_price']
    item_data['item_city'] = response_data['item']['city']
    item_data['item_country'] = response_data['item']['country']
    item_data['item_color'] = response_data['item']['color1'] + " " + response_data['item']['color2']
    item_data['item_status'] = response_data['item']['status']
    item_data['item_views'] = response_data['item']['view_count']
    item_data['item_favorites'] = response_data['item']['favourite_count']
    item_data['item_publication_date'] = response_data['item']['created_at_ts']
    item_data['item_update_date'] = response_data['item']['updated_at_ts']
    item_data['item_available'] = response_data['item']['is_visible']
    item_data['item_active_bid_count'] = response_data['item']['active_bid_count']
    item_pictures = []
    for picture in response_data['item']['photos']:
        item_pictures.append(picture['url'])
    item_data['item_pictures'] = item_pictures
    item_data['user_positive_feedback_count'] = response_data['item']['user']['positive_feedback_count']
    item_data['user_negative_feedback_count'] = response_data['item']['user']['negative_feedback_count']
    

    brand_data = {}
    brand_data['brand_name'] = response_data['item']['brand_dto']['title']
    brand_data['brand_id'] = response_data['item']['brand_dto']['id']
    brand_data['brand_favorites'] = response_data['item']['brand_dto']['favourite_count']
    brand_data['item_count'] = response_data['item']['brand_dto']['item_count']
    brand_data['vinted_slug'] = response_data['item']['brand_dto']['url']

    data = {
        'item_data' : item_data,
        'brand_data' : brand_data
    }


    with open('item_data.json', 'w', encoding='utf-8') as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)

    item_queue.publish(data, message_type = 'save')
    