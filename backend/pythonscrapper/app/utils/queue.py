import pika
import json
from functools import partial
from utils.callback import process_message

class Queue:

    def __init__(self, host='127.0.0.1', port=5672, username='user', password='password', queue_name='my_queue'):
        self.queue_name = queue_name
        
        # Define RabbitMQ server connection parameters
        credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(host=host, port=port, credentials=credentials)

        self.connection = None
        self.channel = None

        try:
            # Attempt to establish a connection and create a channel
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            
            # Ensure the queue exists
            self.channel.queue_declare(queue=self.queue_name, durable=True)
        except Exception as e:
            print(f"Error connecting to the queue: {e}")
            print("Please ensure the RabbitMQ server is configured and running.")
            print("If running in a Docker network, make sure to use the service name as the host.")

    def publish(self, data, message_type):
        if not self.channel:
            print("Cannot publish, no channel established.")
            return

        message = {
            'message_type': message_type,
            'data': data
        }
        payload = json.dumps(message)
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=payload)
        print(f"Sent '{message}' to {self.queue_name}")

    def close(self):
        if self.connection:
            self.connection.close()

    def listen(self, api_connection, item_queue):
        if not self.channel:
            print("Cannot start consuming, no channel established.")
            return

        callback_with_params = partial(process_message, api_connection=api_connection, item_queue=item_queue)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback_with_params, auto_ack=False)
        self.channel.start_consuming()
