import mysql.connector
from mysql.connector import Error
from flask import Flask
app = Flask(__name__)


class Branches:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'CarRental'  # Replace with your MySQL database name
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

    def create(self, data):
        try:
            name = data['name'].upper()
            self.cursor.execute("insert into branches(name) values(%s)", (name,))
            self.conn.commit()
            branch_id = self.cursor.lastrowid

            return {"Status": "Branch created.", "ID": branch_id}, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self):
        try:
            lista = []
            self.cursor.execute("select * from branches")
            fetch = self.cursor.fetchall()
            for branches in fetch:
                vals = {
                    "ID": branches[0],
                    "Name": branches[1]
                }
                lista.append(vals)
            return lista, 200
        except Error as e:
            return {"Error": str(e)}, 500
