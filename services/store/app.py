from flask import Flask, requests, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET"])
def get_server():
    return jsonify({'message': 'Hello World!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)