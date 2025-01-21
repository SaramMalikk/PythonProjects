import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
import datetime
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import bcrypt

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!


class UserInfo:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'shop_bills'  # Replace with your MySQL database name
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

    def users(self, data):
        try:
            password = data['password']
            token = bcrypt.gensalt()
            hash_pass = bcrypt.hashpw(password.encode('utf-8'), token)
            self.cursor.execute("INSERT INTO users (firstname, lastname, telephone, password) values(%s,%s,%s,%s)",
                                (data['firstname'], data['lastname'], data['telephone'], hash_pass))
            self.conn.commit()
            return {"status": "User created successfully"}, 201
        except Error as e:
            return {"Error": f"{e}"}, 404

    def login(self, data):
        password = data['password'].encode('utf-8')
        self.cursor.execute("SELECT password FROM users ")
        result = self.cursor.fetchone()

        stored_hashed_password = result[0]  # We got string"to convert a plain text(string)into code means encoding"
        if isinstance(stored_hashed_password, str):  # Encode the stored hashed password to bytes
            stored_hashed_password = stored_hashed_password.encode('utf-8')
        if bcrypt.checkpw(password, stored_hashed_password):
            return {"Status": "login successfully"}, 200
        else:
            return {"Status": "Invalid code or password"}, 401

#
# @app.route('/create_user', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     db = PersonalInfo()
#     response, status_code = db.users(data)
#     return jsonify(response), status_code
#
#
# @app.route('/login_user', methods=['POST'])
# def login_user():
#     data = request.get_json()
#     db = PersonalInfo()
#     response, status_code = db.login(data)
#     return jsonify(response), status_code

#
# if __name__ == "__main__":
#     app.run(debug=True)
