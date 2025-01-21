import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify

app = Flask(__name__)


class Classes:
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

    def create_classes(self, data):
        self.cursor.execute("insert into classes(name,code) values(%s,%s)", (data['classname'],data['classcode']))
        self.conn.commit()
        return 'Class created successfully'

    def view_classes(self, code):
        try:
            self.cursor.execute("select * from classes  where code = %s", (code,))
            result = self.cursor.fetchone()
            dic = [{'id': result[0], 'Name': result[1], 'Code':result[2]}]
        except TypeError:
            return "Code does not exist"
        return dic

    def view_all_classes(self):
        lista = []
        self.cursor.execute("select * from classes")
        result = self.cursor.fetchall()
        for i in range(len(result)):
            abc = result[i]
            dic = [{'id': abc[0], 'Name': abc[1], 'Code': abc[2]}]
            lista.append(dic)
        return lista


# @app.route('/createclass', methods=['POST'])
# def createclass():
#     data = request.get_json()
#     db = Teachers()
#     response = db.create_classes(data)
#     return jsonify(response)


# @app.route('/classcode', methods=['POST'])
# def classcode():
#     data = request.get_json()
#     code = data.get("code")
#     db = Teachers()
#     response = db.view_classes(code)
#     return jsonify(response)

#
# @app.route('/viewclasses', methods=['POST'])
# def viewclasses():
#     db = Teachers()
#     response = db.view_all_classes()
#     return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

