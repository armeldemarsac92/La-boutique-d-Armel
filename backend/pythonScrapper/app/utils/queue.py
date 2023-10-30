import pika

class Queue:

    def __init__(self, host='localhost', port=5672, username='guest', password='guest', queue_name='my_queue'):
        self.queue_name = queue_name
        
        # Define RabbitMQ server connection parameters
        credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

        # Ensure the queue exists (it's idempotent, so it won't recreate if it already exists with the same properties)
        self.channel.queue_declare(queue=self.queue_name)

    def publish(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        print(f"Sent '{message}' to {self.queue_name}")

    def close(self):
        self.connection.close()
