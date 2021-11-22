import sys
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='openfood_exchange', exchange_type='topic')


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='openfood_exchange', routing_key=method,
                          body=json.dumps(body), properties=properties)
