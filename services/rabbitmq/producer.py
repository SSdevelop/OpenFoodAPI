import sys
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')


def publish(publisher, method, body):

    routing_key = publisher + "." + method

    message = json.dumps(body)

    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=message)

    print(" [x] Sent %r:%r" % (routing_key, message))


publish_body = {"store_id": "1", "store_name": "adistore"}

publish("store", "addstore", publish_body)


connection.close()
