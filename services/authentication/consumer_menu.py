import pika
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
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
        # config_uri = 'mysql+pymysql://root:{password}@authentication_db/app_users'.format(
        #     password=environ['MYSQL_PASSWORD'])
        # app.config['SQLALCHEMY_DATABASE_URI'] = config_uri
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        # db = SQLAlchemy(app)
    except:
        return jsonify({'error': 'Problem with connecting to DB'}), 500


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if method.routing_key == "store.addstore":
        db.menu.insert_one(newstore_empty_menu)
        try:
            # receive the data and put it to the menu_db
            db = get_db()

            data = json.loads(body)

            id = data['id']
            password = data['password']
            user_role = data['user_role']

            user = allUsers(id=id, password=password, user_role=user_role)
            db.session.add(user)
            db.session.commit()

        except:
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
