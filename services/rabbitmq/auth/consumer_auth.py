import pika
import sys
import os
from flask import Flask, jsonify, request, json, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ


app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
config_uri = 'mysql+pymysql://root:{password}@authentication_db/app_users'.format(password=environ['MYSQL_PASSWORD'])
app.config['SQLALCHEMY_DATABASE_URI'] = config_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class allUsers(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(1024))
    user_role = db.Column(db.String(10))
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


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if method.routing_key == 'store.addstore':
        try:

            data = json.loads(body)

            id = data['store_id']
            password = data['password']
            user_role = 'store'

            user = allUsers(id=id, password=password, user_role=user_role)
            db.session.add(user)
            db.session.commit()
            print("Data received through auth_consumer. Added to menu db")
        except:
            print("Problems in adding data recevied through auth_consumer")
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
