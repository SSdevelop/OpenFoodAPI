import pika
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='main')  # dont really need it

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # def callbackSample(ch, method, properties, body):
    #     print('Received in main')
    #     data = json.loads(body)
    #     print(data)

    #     if properties.content_type == 'product_created':
    #         product = Product(
    #             id=data['id'], title=data['title'], image=data['image'])
    #         db.session.add(product)
    #         db.session.commit()
    #         print('Product Created')

    #     elif properties.content_type == 'product_updated':
    #         product = Product.query.get(data['id'])
    #         product.title = data['title']
    #         product.image = data['image']
    #         db.session.commit()
    #         print('Product Updated')

    #     elif properties.content_type == 'product_deleted':
    #         product = Product.query.get(data)
    #         db.session.delete(product)
    #         db.session.commit()
    #         print('Product Deleted')

    # store created
    # store updated
    # menu created for a store
    # menu updated for a store
    # item created for a menu of a particular store
    # item updated for a menu of a particular store

    def callbackSample(ch, method, properties, body):
        print('Received in main')
        data = json.loads(body)
        print(data)

        if properties.content_type == 'product_created':
            product = Product(
                id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product Created')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product Updated')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product Deleted')

    channel.basic_consume(queue='main',
                          auto_ack=True,
                          on_message_callback=callback)

    print('Started consuming')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
