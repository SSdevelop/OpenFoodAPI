# importing required modules
from os import environ
from flask import Flask, jsonify, abort, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics
from flask_cors import CORS

# init our app
#app = Flask(__name__)
#CORS(app)
#metrics = PrometheusMetrics(app)
#metrics.info("app_info", "Menu API", version="1.0.0")

# the status codes

ERR_CODE_NOT_FOUND = {
    "error": "not found"
}

ERR_CODE_CONFLICT = {
    "error": "conflict"
}

SUCCESS_CODE = {
    "success"
}


def get_db():
    try:
        config_URI = 'mongodb://' + \
            environ['MONGO_USERNAME'] + ':' + environ['MONGO_PASSWORD'] + '@' + \
            environ['MONGO_SERVER_HOST'] + ':' + \
            str(environ['MONGO_SERVER_PORT']) + '/menus?authSource=admin'
        app.config['MONGO_URI'] = config_URI
        mongo = PyMongo(app)
        if mongo.db:
            return mongo.db
        else:
            # if cant connect then return error
            return jsonify({'error': 'cannot connect to DB'}), 500
    except:
        return jsonify({'error': 'Problem with connecting to DB'}), 500

# GET order


@app.route('/order/<order_id>', methods=['GET'])
def getOrder(store_id):

    # call the orders
    db = get_db()

    orders = db.order.find_one_or_404({'order_id': order_id},{'_id':False})
    return jsonify(orders), 200

# POST accept order

@app.route('order/{order_id}/accept_order', methods=['POST'])
def acceptorder(order_id):
    db = get_db()

    order = db.order.find_one({'order_id': order_id})

    if order:
        accepted_order = {}

        if request.get_json().get('reason'):
            reason = request.get_json().get('reason')
            accepted_order.reason = reason
        if request.get_json().get('pickup_time'):
            pickup_time = request.get_json().get('pickup_time')
            accepted_order.pickup_time = pickup_time
        if request.get_json().get('external_reference_id'):
             external_reference_id = request.get_json().get('external_reference_id')
             accepted_order.external_reference_id = external_reference_id
        
        try:
            db.item.accept_one(accept_order)
        
        except:       
             return jsonify(result), 200
    else:
        return jsonify(ERR_CODE), 404
    
    # POST deny order

@app.route('order/{order_id}/deny_order', methods=['POST'])
def denyorder(order_id):
    db = get_db()

    order = db.items.find_one({'order_id': order_id})

    if item:
        denied_order = {}

        if request.get_json().get('reason'):
            reason = request.get_json().get('reason')
            denied_order.reason = reason
        if request.get_json().get('out_of_stock_items'):
            denied_order = request.get_json().get('out_of_stock_items')
            updated_item.out_of_stock_items = out_of_stock_items
        if request.get_json().get('invalid_items'):
            invalid_items = request.get_json().get('invalid_items')
            denied_order.invalid_items = invalid_items
       
        try:
            db.item.deny_one(deny_order)
        except:
                  return jsonify(result), 200
    else:
        return jsonify(ERR_CODE), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001, debug=False)