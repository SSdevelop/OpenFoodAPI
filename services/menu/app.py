# importing required modules
from os import environ
from flask import Flask, jsonify, abort, request, json
from prometheus_flask_exporter import PrometheusMetrics
from flask_cors import CORS
from flask_pymongo import PyMongo
from sys import exit, version


# # init our app
# app = Flask(__name__)
# metrics = PrometheusMetrics(app)
# metrics.info("app_info", "Menu API", version="1.0.0")

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


# def get_db():
#     try:
#         client = MongoClient(host=os.environ['MONGO_SERVER_HOST'],
#                              # convert the port number to make sure its an integer
#                              port=int(os.environ['MONGO_SERVER_PORT']),
#                              username=os.environ['MONGO_USERNAME'],
#                              password=os.environ['MONGO_PASSWORD'], connect=False
#                              )
#         if client:
#             db = client["menu"]
#             return db
#         else:
#             # if cant connect then return error
#             return jsonify(ERR_CODE_NOT_FOUND), 404
#     except:
#         return jsonify({'error': 'Problem with connecting to DB'}), 500


app = Flask(__name__)
CORS(app)
config_URI = 'mongodb://' + \
    environ['MONGO_USERNAME'] + ':' + environ['MONGO_PASSWORD'] + '@' + \
    environ['MONGO_SERVER_HOST'] + ':' + \
    str(environ['MONGO_SERVER_PORT']) + '/menu?authSource=admin'

app.config['MONGO_URI'] = config_URI
mongo = PyMongo(app)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Menu API", version="1.0.0")


@app.route('/menus/<store_id>', methods=['GET'])
def getMenu(store_id):

    # call the stores
    # db = get_db()

    try:
        menus = mongo.db.menu.find_one(
            {'store_id': store_id})
        return jsonify(menus), 200
    except Exception as err:
        abort(500)


# PUT upload Menu


@app.route('/menus/<store_id>', methods=['PUT'])
def uploadMenu(store_id):
    # db = get_db()

    id = request.get_json().get('id')
    title = request.get_json().get('title')
    subtitle = request.get_json().get('subtitle')
    category_ids = request.get_json().get('category_ids')

    menu = mongo.db.menu.find_one({'store_id': store_id, 'id': id})

    if menu:
        result = [{"id": id, "title": title,
                   "subtitle": subtitle, "category_ids": category_ids, "store_id": store_id}]
        try:
            mongo.db.menu.update_one(result[0])
        except Exception as err:
            abort(500)

        return jsonify("Menu is updated"), 409
    # if the stud does not exist then add him
    else:
        result = [{"id": id, "title": title,
                   "subtitle": subtitle, "category_ids": category_ids, "store_id": store_id}]

        try:
            mongo.db.menu.insert_one(result[0])
        except Exception as err:
            abort(500)
    return jsonify("Success!"), 200

# POST update Item


@app.route('/menus/set-item', methods=['POST'])
def setItemById():

    try:
        # db = get_db()
        data = request.args.to_dict()

        if 'store_id' not in data.keys():
            return jsonify({'error': 'no store_id specified.'}), 400
        if 'item_id' not in data.keys():
            return jsonify({'error': 'no item_id specified.'}), 400
        if 'description' in data.keys() and 'title' in data.keys() and 'price' in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'description': data['description'],
                        'title': data['title'],
                        'price': data['price']
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404
        if 'description' in data.keys() and 'title' not in data.keys() and 'price' not in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'description': data['description'],
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404

        if 'description' in data.keys() and 'title' in data.keys() and 'price' not in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'description': data['description'],
                        'title': data['title'],
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404

        if 'description' in data.keys() and 'title' not in data.keys() and 'price' in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'description': data['description'],
                        'price': data['price'],
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404

        if 'description' not in data.keys() and 'title' in data.keys() and 'price' in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'title': data['title'],
                        'price': data['price'],
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404

        if 'description' not in data.keys() and 'title' in data.keys() and 'price' not in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'title': data['title'],
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404

        if 'description' not in data.keys() and 'title' not in data.keys() and 'price' in data.keys():
            item = mongo.db.item.find_one_and_update(
                {'store_id': data['store_id'], 'item_id': data['item_id']},
                {
                    '$set': {
                        'price': data['price'],
                    }
                }
            )
            if item is None:
                return jsonify({'message': 'Item not updated successfully'}), 404

        return jsonify(SUCCESS_CODE), 200
    except Exception as err:
        abort(500)


@app.errorhandler(404)
def wrong_url(e):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001)
