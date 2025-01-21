import mysql.connector
from mysql.connector import Error
from flask import Flask
from datetime import date
app = Flask(__name__)


class Payments:
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

    def payments(self, data):
        try:
            dt = date.today()
            self.cursor.execute("SELECT payment_status from rentals WHERE id = %s", (data['rent_id'],))
            fetch = self.cursor.fetchone()
            if fetch is None:
                return {"Error": "Invalid rental_id. Check if the ID exists."}, 404

            payment_status = fetch[0]
            if payment_status == 'Cleared':
                return {"Error": "Avoid double payment. Please Check the payment Status of provided ID."}, 400

            self.cursor.execute("INSERT INTO payments(rental_id,date,amount,method) values(%s,%s,%s,%s)",
                                (data['rent_id'], dt, data['amount'], data['method']))
            self.conn.commit()
            # Retrieve the ID of the newly created payment
            payment_id = self.cursor.lastrowid

            self.cursor.execute("UPDATE rentals SET payment_status = %s WHERE id = %s", ('Cleared', data['rent_id']))
            self.conn.commit()

            val = {
                "Status": "Payment Cleared",
                "Payment_ID": payment_id
            }
            return val, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self, data):
        try:
            self.cursor.execute("select p.date , p.amount, p.method , r.payment_status, c.email from payments p "
                                "left join rentals r on p.rental_id = r.id left join customers c on r.customer_id = "
                                "c.id where r.id = %s", (data['rental_id'],))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "No Payment found with this ID. Check if the ID exists"}, 404

            val = {"Payment_Info": {
                "Payment_Date": fetch[0],
                "Amount_Paid": fetch[1],
                "Payment_Method": fetch[2],
                "Payment_Status": fetch[3],
                "Email": fetch[4]
            }}
            return val, 200
        except Error as e:
            return {"Error": str(e)}, 500
