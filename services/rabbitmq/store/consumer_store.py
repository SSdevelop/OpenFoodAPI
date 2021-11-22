import pika
import sys
import os
from pymongo import MongoClient
from os import environ
from flask import Flask, json, jsonify, abort, request


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='openfood_exchange', exchange_type='topic')

    # temp queue for now
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = ['store.updatestore', 'store.addstore']

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='openfood_exchange', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Started consuming')
    channel.start_consuming()


def get_db():
    try:
        client = MongoClient(host=os.environ['MONGO_SERVER_HOST'],
                             # convert the port number to make sure its an integer
                             port=int(os.environ['MONGO_SERVER_PORT']),
                             username=os.environ['MONGO_USERNAME'],
                             password=os.environ['MONGO_PASSWORD'],
                             )
        if client:
            db = client["store"]
            return db
        else:
            # if cant connect then return error
            return jsonify({'error': 'not found'}), 404
    except:
        return jsonify({'error': 'Problem with connecting to DB'}), 500


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    # store consumer handling process can be implemented here


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
