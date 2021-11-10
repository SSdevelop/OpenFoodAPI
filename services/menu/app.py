# importing required modules
import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
# from prometheus_flask_exporter import PrometheusMetrics


# init our app
app = Flask(__name__)


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
    client = MongoClient(host=os.environ['MONGO_SERVER_HOST'],
                         # convert the port number to make sure its an integer
                         port=int(os.environ['MONGO_SERVER_PORT']),
                         username=os.environ['MONGO_USERNAME'],
                         password=os.environ['MONGO_PASSWORD'],
                         )
    if client:
        db = client["university"]
        return db
    else:
        return ERR_CODE, 404   # if cant connect then return error


@app.route('/')
def hello():
    return "Hello bro!"

# GET /students/<student_id> endpoint - returns the info about an indicated student


@app.route('/stores/<store_id>/menus', methods=['GET'])
def getMenu(store_id):

    # call the stores
    db = get_db()

    menus = db.menu.find(
        {'store_id': store_id})

    if menus:
        result = menus
    else:
        return jsonify(ERR_CODE), 404
    return jsonify(result), 200


@app.route('/stores/<store_id>/menus', methods=['PUT'])
def uploadMenu(store_id):
    db = get_db()
    # check if the student already exists
    student_id = request.get_json().get('student_id')
    student = db.student.find_one({'student_id': student_id})
    if student:
        return jsonify("Student already exists"), 409
    # if the stud does not exist then add him
    else:
        dept_name = request.get_json().get("dept_name")
        gpa = request.get_json().get("gpa")
        name = request.get_json().get("name")
        student_id = request.get_json().get("student_id")

        result = [{"dept_name": dept_name, "gpa": gpa,
                  "name": name, "student_id": student_id}]

        db.student.insert_one(result[0])

    return jsonify("Success!"), 200


@app.route('/takes/<student_id>', methods=['GET'])
def getStudentsCoursesById(student_id):
    db = get_db()
    student = db.student.find_one({'student_id': student_id})
    if student:
        _courses = db.takes.find(
            {'student_id': student["student_id"]}).sort('course_id', 1)
        courses = [{"course_id": course["course_id"],
                    "credits":course["credits"]} for course in _courses]
        result = [{"dept_name": student["dept_name"], "gpa": student["gpa"],
                   "name": student["name"], "student_id": student["student_id"], "student_takes": courses}]
        return jsonify(result), 200
    else:
        return jsonify(ERR_CODE), 404
