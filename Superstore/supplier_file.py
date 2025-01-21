import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify

app = Flask(__name__)


class Supplier:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'superstore'  # Replace with your MySQL database name
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

    def suppliers_data(self, data):
        try:
            self.cursor.execute("insert into suppliers(first_name,last_name,email,phone) values(%s,%s,%s,%s)",
                                (data['firstname'], data['lastname'], data['email'], data['phone']))
            self.conn.commit()
            return {"Status": "Supplier Entered successfully"}, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self):
        try:
            lista = []
            self.cursor.execute("Select * from suppliers")
            fetch = self.cursor.fetchall()
            for i in range(len(fetch)):
                data = fetch[i]
                val = {
                    "Id": data[0],
                    "Firstname": data[1],
                    "Lastname": data[2],
                    "Email": data[3],
                    "Phone": data[4]
                }
                lista.append(val)
            return {"Suppliers_Info": lista}, 200
        except Error as e:
            return {"Error": str(e)}, 404

    def remove(self, data):
        try:
            self.cursor.execute("Delete from suppliers where id = %s", (data['id'],))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                # No rows were affected, meaning the ID does not exist
                return {"Error": "No employee found with the provided ID."}, 404
            return {"Status": "Supplier removed."}, 200
        except Error as e:
            return {"Error": str(e)}, 500
