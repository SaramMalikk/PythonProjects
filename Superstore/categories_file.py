import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify

app = Flask(__name__)


class Categories:
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

    def category_info(self, data):
        try:
            name = data['name'].upper()
            des = data['des'].upper()
            parent_id = data.get('parentCategory')  # .get to handle none value from input
            self.cursor.execute("insert into categories (name,description,parent_id) values (%s,%s,%s)",
                                (name, des, parent_id))
            self.conn.commit()
            return {"status": "Category entered successfully"}, 201

        except Error as e:
            return {"Error": str(e)}, 500

    def view(self):
        try:
            lista = []
            self.cursor.execute("select * from categories")
            fetch = self.cursor.fetchall()
            for i in range(len(fetch)):
                data = fetch[i]
                values = {
                    "Category_id": data[0],
                    "Category": data[1],
                    "Detail": data[2],
                    "Parent_id": data[3]
                }
                lista.append(values)
            return {"Category_info": lista}, 200
        except Error as e:
            return {"Error": str(e)}, 404


if __name__ == '__main__':
    app.run(debug=True)
