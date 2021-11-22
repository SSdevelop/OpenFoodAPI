from datetime import datetime, timedelta
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


@app.route('/auth/users', methods=['GET'])
def get_users():
    if 'x-access-token' not in request.headers:
        return jsonify({'error': 'No token given'}), 403
    token = request.headers['x-access-token']
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    if 'user_role' not in data.keys():
        return jsonify({'error': 'user_role not specified in the token'}), 403
    if data['user_role'] != 'admin':
        return jsonify({'error': 'not authorised'}), 403
    users = allUsers.query.all()
    output = []
    for user in users:
        output.append({
            'id': user.id,
            'password': user.password,
            'user_role': user.user_role
        })
    return jsonify(output), 200


@app.route('/auth/signup', methods=["POST"])
def singup_users():
    if not request.data:
        return jsonify({"error": "no data given. Please give data to insert."}), 400
    data = request.get_json(force=True)
    if "id" not in data.keys():
        return jsonify({'error': 'no ID specified.'}), 400
    if 'password' not in data.keys():
        return jsonify({'error': 'no passoword specified.'}), 400
    if 'user_role' not in data.keys():
        return jsonify({'error': 'no user_role specified.'}), 400
    try:
        id = data['id']
        password = data['password']
        user_role = data['user_role']
        user = allUsers.query.filter_by(id=id).first()
        if not user:
            user = allUsers(id=id, password=password, user_role=user_role)
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': 'user added successfully'}), 201
        return jsonify({'error': 'User already present'}), 202
    except:
        return jsonify({'error': 'cannot connect to database'}), 500


@app.route('/auth/signin', methods=["POST"])
def login_user():
    if not request.data:
        return jsonify({"error": "no data given. Please give data to insert."}), 400
    data = request.get_json(force=True)
    if "id" not in data.keys():
        return jsonify({'error': 'no ID specified.'}), 400
    if 'password' not in data.keys():
        return jsonify({'error': 'no passoword specified.'}), 400
    try:
        user = allUsers.query.filter_by(id = data['id']).first()
        if not user:
            return jsonify({'error': 'No user present'}), 401
        if data['password'] != user.password:
            return jsonify({'error': 'Password does not match'}), 403
        token = jwt.encode({
            'id': user.id,
            'user_role': user.user_role,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token}), 200
    except:
        return jsonify({'error': 'Internal Server error'}), 500


@app.errorhandler(404)
def handle_404(e):
    return jsonify({'error': 'Not Found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9004, debug=False)
