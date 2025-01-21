from Students import *
from classes import *
from attendance import *
from teachers import *
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from flask_cors import CORS  # Import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes



@app.route('/viewstudents', methods=['POST'])
@jwt_required()
def viewstudents():
    data = request.get_json()
    roll = data.get('roll')
    db = Students()
    response = db.view_students(roll)
    return jsonify(response)


@app.route('/viewstudentbyclass', methods=['POST'])
@jwt_required()
def viewstudentbyclass():
    data = request.get_json()
    classcode = data.get('classcode')
    db = Students()
    response = db.view_students_byclass(classcode)
    return jsonify(response)


@app.route('/createstudent', methods=['POST'])
@jwt_required()
def createstudent():
    data = request.get_json()
    db = Students()
    response = db.create_students(data)
    return jsonify(response)


@app.route('/createclass', methods=['POST'])
@jwt_required()
def createclass():
    data = request.get_json()
    db = Classes()
    response = db.create_classes(data)
    return jsonify(response)


@app.route('/checkclass', methods=['POST'])
@jwt_required()
def checkclass():
    data = request.get_json()
    code = data.get("code")
    db = Classes()
    response = db.view_classes(code)
    return jsonify(response)


@app.route('/viewclasses', methods=['POST'])
@jwt_required()
def viewclasses():
    db = Classes()
    response = db.view_all_classes()
    return jsonify(response)


@app.route('/check_attend', methods=['POST'])
@jwt_required()
def check_attend():
    db = Att()
    response = db.show_attendance()
    return jsonify(response)


@app.route('/attend_data', methods=['POST'])
@jwt_required()
def attend_data():
    data = request.get_json()
    db = Att()
    response = db.show_attend_info(data)
    return jsonify(response)


@app.route('/mark_attend', methods=['POST'])
# @jwt_required()
def mark_attend():
    data = request.get_json()
    db = Att()
    response_message, status_code = db.mark_attendance(data)
    return jsonify({'message': response_message}), status_code


@app.route('/addtcode', methods=['POST'])
@jwt_required()
def addtcode():
    data = request.get_json()
    teachercode = data.get('teachercode')
    db = Teachers()
    response = db.view_teachers(teachercode)
    return jsonify(response)


@app.route('/enterteacher', methods=['POST'])
# @jwt_required()
def enterteacher():
    data = request.get_json()
    db = Teachers()
    response = db.create_teacher(data)
    return jsonify(response)


@app.route('/viewteachers', methods=['POST'])
@jwt_required()
def viewteachers():
    db = Teachers()
    response = db.view_all_teachers()
    return jsonify(response)


@app.route('/login_to_data', methods=['POST'])
def login_to_data():
    data = request.get_json()
    db = Teachers()
    response = db.login(data)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
