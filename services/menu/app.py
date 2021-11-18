# importing required modules
import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics


# init our app
app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Menu API", version="1.0.0")

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
        client = MongoClient(host=os.environ['MONGO_SERVER_HOST'],
                            # convert the port number to make sure its an integer
                            port=int(os.environ['MONGO_SERVER_PORT']),
                            username=os.environ['MONGO_USERNAME'],
                            password=os.environ['MONGO_PASSWORD'],
                            )
        if client:
            db = client["menu"]
            return db
        else:
            return jsonify(ERR_CODE_NOT_FOUND), 404   # if cant connect then return error
    except:
        return jsonify({'error': 'Problem with connecting to DB'}), 500


@app.route('/menus/<store_id>', methods=['GET'])
def getMenu(store_id):

    # call the stores
    db = get_db()

    menus = db.menu.find(
        {'store_id': store_id})

    if menus:
        result = menus
    else:
        return jsonify(ERR_CODE_NOT_FOUND), 404
    return jsonify(result), 200

# PUT upload Menu


@app.route('/menus/<store_id>', methods=['PUT'])
def uploadMenu(store_id):
    db = get_db()

    id = request.get_json().get('id')
    title = request.get_json().get('title')
    subtitle = request.get_json().get('subtitle')
    category_ids = request.get_json().get('category_ids')

    menu = db.menu.find_one({'store_id': store_id, 'id': id})

    if menu:
        result = [{"id": id, "title": title,
                   "subtitle": subtitle, "category_ids": category_ids, "store_id": store_id}]
        try:
            db.menu.update_one(result[0])
        except:
            print("DB Error")

        return jsonify("Menu is updated"), 409
    # if the stud does not exist then add him
    else:
        result = [{"id": id, "title": title,
                   "subtitle": subtitle, "category_ids": category_ids, "store_id": store_id}]

        try:
            db.menu.insert_one(result[0])
        except:
            print("DB Error")
    return jsonify("Success!"), 200

# POST update Item

# give the data in form of request body and not parameters.
# use the correct syntax for updating.
@app.route('/menus/set-item', methods=['POST'])
def setItemById(store_id, item_id):
    db = get_db()

    item = db.items.find_one({'item_id': item_id, 'store_id': store_id})

    if item:
        updated_item = {}

        if request.get_json().get('id'):
            id = request.get_json().get('id')
            updated_item.id = id
        if request.get_json().get('description'):
            description = request.get_json().get('description')
            updated_item.description = description
        if request.get_json().get('title'):
            title = request.get_json().get('title')
            updated_item.title = title
        if request.get_json().get('price'):
            price = request.get_json().get('price')
            updated_item.price = price

        try:
            db.item.update_one(updated_item)
        except:
            print("DB Error")

        return jsonify(SUCCESS_CODE), 200
    else:
        return jsonify(ERR_CODE_NOT_FOUND), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001, debug=False)
