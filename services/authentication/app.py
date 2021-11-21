from flask import Flask, jsonify, request
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from os import environ

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Authentication API", version="1.0.0")
app.config['SECRET_KEY'] = environ['SECRET_KEY']
config_uri = 'mysql+pymysql://root:{password}@authentication_db/app_users'.format(
    password=environ['MYSQL_PASSWORD'])
app.config['SQLALCHEMY_DATABASE_URI'] = config_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class allUsers(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(1024))
    user_role = db.Column(db.String(10))

@app.route('/users', methods=['GET'])
def get_users():
    users = allUsers.query.all()
    output = []
    for user in users:
        output.append({
            'id': user.id,
            'password': user.password,
            'user_role': user.user_role
        })
    return jsonify(output), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9004, debug=False)
