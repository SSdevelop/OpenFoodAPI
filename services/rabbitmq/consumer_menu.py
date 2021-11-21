import pika
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # temp queue for now
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = ['store.updatestore', 'store.addstore']

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Started consuming')
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    # receive the data and put it to the menu_db


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
