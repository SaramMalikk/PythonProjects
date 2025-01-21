import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import date
app = Flask(__name__)


class Inventory:
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

    # def inventory_info(self, data):
    #     try:
    #         code = str(data['code'])
    #         product_code = code.upper()
    #         dt = date.today()
    #         self.cursor.execute("insert into inventory (product_code,stock,purchasing_price,date,description)"
    #                       " values(%s,%s,%s,%s,%s)", (product_code, data['stock'], data["purchase"], dt, data['des']))
    #         self.conn.commit()
    #         return {"Status": "Inventory updated."}, 200
    #     except Error as e:
    #         return {"Error": e}, 500

    def view(self, data):
        try:
            products_code = data['code']
            self.cursor.execute("select p.name,p.price,i.stock,i.purchasing_price from inventory i left join "
                                "products p on p.product_code = i.product_code where p.product_code = %s",
                                (products_code,))
            fetch = self.cursor.fetchall()
            result = fetch[0]
            val = {"Inventory_info": {
                "Name": result[0],
                "Sell_price": result[1],
                "Stock_available": result[2],
                "Purchase_price": result[3]
            }}
            return val, 200
        except Error as e:
            return {"Error": str(e)}, 404


if __name__ == '__main__':
    app.run(debug=True)

