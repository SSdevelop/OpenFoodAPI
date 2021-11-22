import pika
import sys
import os
from os import environ
from pymongo import MongoClient
from flask import Flask, json, jsonify, abort, request


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='openfood_exchange', exchange_type='topic')

    # temp queue for now
    result = channel.queue_declare('')
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
            db = client["menus"]
            return db
        else:
            # if cant connect then return error
            return jsonify(ERR_CODE_NOT_FOUND), 404
    except:
        return jsonify({'error': 'Problem with connecting to DB'}), 500


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if method.routing_key == 'store.addstore':

        try:
            # receive the data and put it to the menu_db
            db = get_db()

            data = json.loads(body)

            newstore_empty_menu = {"id": 'empty_menu_id_' + data['store_id'], "title": 'Empty Menu',
                                   "subtitle": 'Empty Meny Subtitle', "category_ids": ['item1', 'item2'], "store_id": data['store_id']}

            db.menu.insert_one(newstore_empty_menu)
            print("Data received through consumer added to menu db")
        except:
            print("Problems in adding data recevied through consumer")
            abort(500)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


@app.errorhandler(404)
def wrong_url(e):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500
