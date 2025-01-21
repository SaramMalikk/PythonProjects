import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify, make_response
import datetime
from datetime import timedelta, timezone

from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!


class Teachers:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'practice'  # Replace with your MySQL database name
        self.conn = None
        self.cursor = None

        # Create the database connection and cursor directly in the constructor
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                print("Successfully connected to the database.")
                self.cursor = self.conn.cursor(buffered=True)
                print("Cursor created successfully.")
        except Error as e:
            print(f"Error: {e}")
            self.conn = None
            self.cursor = None

    def create_teacher(self, data):
        self.cursor.execute('select nid from teachers order by nid desc ')
        result = self.cursor.fetchone()
        if result[0] == 0:
            result[0] = 1
            numeric_id = str((result[0]) + 1)
            new_code = 'T' + numeric_id
            self.cursor.execute("insert into teachers(firstname,lastname,tcode,nid,password) values(%s,%s,%s,%s,%s)",
                                (data['firstname'], data['lastname'], new_code, numeric_id, data['password']))
            self.conn.commit()
            return 'Teacher created successfully'
        else:
            result = list(self.cursor.fetchone())
            numeric_id = str((result[0]) + 1)
            new_code = 'T' + numeric_id
            self.cursor.execute("insert into teachers(firstname,lastname,tcode,nid,password) values(%s,%s,%s,%s,%s)", (data['firstname'], data['lastname'], new_code, numeric_id, data['password']))
            self.conn.commit()
            return 'Teacher created successfully'

    def view_teachers(self, teachercode):
        try:
            self.cursor.execute("select * from teachers  where tcode = %s", (teachercode,))
            result = self.cursor.fetchone()
            dic = [{'id': result[0], 'firstname': result[1], 'lastname': result[2], 'tcode': result[3], 'nid': result[4], 'password': result[5]}]
        except TypeError:
            return "Teacher code does not exist"
        return dic

    def view_all_teachers(self):
        lista = []
        self.cursor.execute("select * from teachers  ")
        result = self.cursor.fetchall()
        for i in range(len(result)):
            abc = result[i]
            dic = [{'id': abc[0], 'firstname': abc[1], 'lastname': abc[2], 'tcode': abc[3], 'nid': abc[4], 'password': abc[5]}]
            lista.append(dic)
        return lista

    def login(self, data: dict):
        self.cursor.execute("select id from teachers  where  tcode = %s and password =%s", (data["code"], data['password']))
        result = self.cursor.fetchone()
        if len(result) == 0:
            return 'invalid code or password'
        elif len(result) == 1:
            access_token = create_access_token({'user': result[0]}, expires_delta=datetime.timedelta(minutes=2))
            return {'access token': access_token}


# @app.route('/addcode', methods=['POST'])
# def addcode():
#     data = request.get_json()
#     teachercode = data.get('teachercode')
#     db = Teachers()
#     response = db.view_teachers(teachercode)
#     return jsonify(response)

#
# @app.route('/enterteacher', methods=['POST'])
# def enterteacher():
#     data = request.get_json()
#     db = Teachers()
#     response = db.create_teacher(data)
#     return jsonify(response)

#
# @app.route('/viewteachers', methods=['POST'])
# def viewteachers():
#     db = Teachers()
#     response = db.view_all_teachers()
#     return jsonify(response)

#
# @app.route('/loginteacher', methods=['POST'])
# def loginteacher():
#     data = request.get_json()
#     db = Teachers()
#     response = db.login_teacher(data)
#     return jsonify(response)
#
# if __name__ == "__main__":
#     app.run(debug=True)
