from flask import Flask, json, jsonify, abort, request
from flask_pymongo import PyMongo
from os import environ
from sys import exit
from prometheus_flask_exporter import PrometheusMetrics
from flask_cors import CORS
from producer import publish
import jwt

app = Flask(__name__)
CORS(app)
config_URI = 'mongodb://' + \
    environ['MONGO_USERNAME'] + ':' + environ['MONGO_PASSWORD'] + '@' + \
    environ['MONGO_SERVER_HOST'] + ':' + \
    str(environ['MONGO_SERVER_PORT']) + '/store?authSource=admin'

app.config['MONGO_URI'] = config_URI
mongo = PyMongo(app)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Store API", version="1.0.0")


@app.route('/stores', methods=["GET"])
def get_store():
    try:
        stores = list(mongo.db.information.find({}, {'_id': False}))
        locations = list(mongo.db.location.find({}, {'_id': False}))
        if len(stores) == 0 or len(locations) == 0:
            return jsonify({'error': 'No Store Found'}), 404
        for store in stores:
            for location in locations:
                if store['store_id'] == location['store_id']:
                    store['location'] = location
        return jsonify(stores), 200
    except Exception as err:
        abort(500)


@app.route('/stores/add-store', methods=["POST"])
def add_store():

    try:
        if not request.data:
            return jsonify({'error': 'no data given'}), 400
        data = request.get_json(force=True)
        if 'store_id' not in data.keys():
            return jsonify({'error': 'no store_id given'}), 400
        if 'location' not in data.keys():
            return jsonify({'error': 'location information not present'}), 400
        if 'contact_emails' not in data.keys():
            return jsonify({'error': 'email information not present'}), 400
        if 'name' not in data.keys():
            return jsonify({'error': 'name information not present'}), 400
        if 'priceBucket' not in data.keys():
            return jsonify({'error': 'price bucket information not present'}), 400
        if data['priceBucket'] not in ['$', '$$', '$$$']:
            return jsonify({'error': 'incorrect price bucket symbol. Must be $, $$ or $$$.'}), 400
        if 'password' not in data.keys():
            return jsonify({'error': 'password information not present'}), 400
        store = list(mongo.db.information.find(
            {'store_id': data['store_id']}, {'_id': False}))
        if len(store) != 0:
            return jsonify({'error': 'store_id present'}), 400
        mongo.db.information.insert_one({
            'store_id': data['store_id'],
            'name': data['name'],
            "contact_emails": data['contact_emails'],
            "isOpen": True,
            "priceBucket": data['priceBucket']
        })
        mongo.db.location.insert_one(data['location'])

        publish_body = {'store_id': data['store_id'],
                        'name': data['name'],
                        "contact_emails": data['contact_emails'],
                        "isOpen": True,
                        "priceBucket": data['priceBucket']}

        publish("store", "addstore", publish_body)

        return jsonify({'message': 'Store Added Successfully'}), 201
    except:
        return jsonify({'error': 'internal server error'}), 500


@app.route('/stores/<store_id>', methods=["GET"])
def get_one_store(store_id):
    store = dict(mongo.db.information.find_one_or_404(
        {'store_id': store_id}, {'_id': False}))
    location = dict(mongo.db.location.find_one_or_404(
        {'store_id': store_id}, {'_id': False}))
    store['location'] = location
    return jsonify(store), 200


@app.route('/stores/status/<store_id>', methods=["GET"])
def get_store_status(store_id):
    store = dict(mongo.db.information.find_one_or_404(
        {'store_id': store_id}, {'_id': False}))
    if store['isOpen']:
        return jsonify({'status': 'Open'}), 200
    output = {}
    output['status'] = 'Closed'
    if 'reasonClose' in store.keys():
        output['reason'] = store['reasonClose']
    return jsonify(output), 200


<< << << < HEAD


@app.route('/stores/set_status/<store_id>', methods=["GET", "PATCH"])
== == == =


@app.route('/stores/set_status/<store_id>', methods=["PATCH"])
>>>>>> > main


def set_store_status(store_id):
    if 'x-access-token' not in request.headers:
        return jsonify({'error': 'No token given'}), 403
    token = request.headers['x-access-token']
    decoded_token = jwt.decode(
        token, environ['SECRET_KEY'], algorithms="HS256")
    if store_id != decoded_token['id']:
        return jsonify({'error': 'not authorised'}), 403
    if decoded_token['user_role'] not in ['store', 'admin']:
        return jsonify({'error': 'not authorised'}), 403
    try:
        data = request.args.to_dict()
        if 'status' not in data.keys():
            return jsonify({'error': 'no status specified.'}), 400
        if data['status'] != 'closed' and data['status'] != 'open':
            return jsonify({'error': 'status should be either closed or open'}), 400
        if 'description' in data.keys() and data['status'] == 'closed':
            store = mongo.db.information.find_one_and_update(
                {'store_id': store_id},
                {
                    '$set': {
                        'isOpen': False,
                        'reasonClosed': data['description']
                    }
                }
            )
            if store is None:
                return jsonify({'message': 'Status not updated successfully'}), 404
        if data['status'] == 'closed' and 'description' not in data.keys():
            store = mongo.db.information.find_one_and_update(
                {'store_id': store_id},
                {
                    '$set': {
                        'isOpen': False,
                        'reasonClosed': ''
                    }
                }
            )
            if store is None:
                return jsonify({'message': 'Status not updated successfully'}), 404
        if data['status'] == 'open':
            store = mongo.db.information.find_one_and_update(
                {'store_id': store_id},
                {
                    '$set': {
                        'isOpen': True,
                        'reasonClosed': ''
                    }
                }
            )
            if store is None:
                return jsonify({'message': 'Status not updated successfully'}), 404
        return jsonify({'message': 'Status updated successfully'}), 200
    except Exception as err:
        abort(500)


@app.errorhandler(404)
def wrong_url(e):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
