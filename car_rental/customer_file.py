import mysql.connector
from mysql.connector import Error
from flask import Flask
app = Flask(__name__)


class Customers:
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
            self.cursor.execute("INSERT INTO customers (firstname,lastname,email,phone,license_number,license_expiry)"
                                "values(%s,%s,%s,%s,%s,%s)", (data['firstname'], data['lastname'], data['email'],
                                                              data['phone'], data['license'], data['expiry']))
            self.conn.commit()

            # Retrieve the ID of the newly created customer
            customer_id = self.cursor.lastrowid

            val = {
                "Status": "Customer created",
                "ID": customer_id

            }
            return val, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self, data):
        try:
            self.cursor.execute("SELECT * FROM customers WHERE phone = %s", (data['phone'],))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "Invalid phone number"}, 404

            vals = {
                "id": fetch[0],
                "Firstname": fetch[1],
                "lastname": fetch[2],
                "Email": fetch[3],
                "Phone": fetch[4],
                "license_number": fetch[5],
                "license_expiry": fetch[6]
            }
            return vals, 200
        except Error as e:
            return {"Error": str(e)}

    def remove(self, data):
        try:
            self.cursor.execute("DELETE from customers WHERE id =%s", (data['id'],))
            self.conn.commit()

            if self.cursor.rowcount == 1:
                return {"Error": "No row effected. Check if the ID exists."}, 404

            return {"Status": "Customer Deleted."}, 200
        except Error as e:
            return {"Error": str(e)}, 500

    def edit(self, data):
        try:
            self.cursor.execute("UPDATE customers set firstname = %s , lastname = %s, email = %s , phone = %s, "
                                "license_number = %s, license_expiry = %s WHERE id = %s",
                                (data['firstname'], data['lastname'], data['email'], data['phone'], data['license'],
                                 data['expiry'], data['id']))
            self.conn.commit()

            if self.cursor.rowcount == 0:
                return {"Error": "No row effected. Check if the ID exists."}, 404

            return {"Status": "Customer updated."}, 201
        except Error as e:
            return {"Error": str(e)}, 500
