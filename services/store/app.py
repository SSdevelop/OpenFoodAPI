from flask import Flask, json, jsonify, abort, request
from flask_pymongo import PyMongo
from os import environ
from sys import exit, version
# from prometheus_flask_exporter import PrometheusMetrics
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
config_URI = 'mongodb://' + \
    environ['MONGO_USERNAME'] + ':' + environ['MONGO_PASSWORD'] + '@' + \
    environ['MONGO_SERVER_HOST'] + ':' + \
    str(environ['MONGO_SERVER_PORT']) + '/store?authSource=admin'

app.config['MONGO_URI'] = config_URI
mongo = PyMongo(app)
# metrics = PrometheusMetrics(app)
# metrics.info("app_info", "Store API", version="1.0.0")

@app.route('/store', methods=["GET"])
def get_store():
    try:
        stores = list(mongo.db.information.find({}, {'_id': False}))
        if len(stores) == 0:
            return jsonify({'error': 'No Store Found'}), 404
        return jsonify(stores), 200
    except:
        abort(500)

@app.errorhandler(404)
def wrong_url(e):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
