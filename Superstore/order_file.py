import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import date
app = Flask(__name__)


class Orders:
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

    def enter_order(self, data):
        try:
            product_code = data["code"].upper()
            self.cursor.execute("select stock from inventory where product_code = %s", (product_code,))
            fetch = self.cursor.fetchone()
            if fetch is None:
                fetch = 0
                old_stock = fetch
            else:
                old_stock = fetch[0]
            self.cursor.execute("select supplier_id from products where product_code = %s", (product_code,))
            fetch = self.cursor.fetchone()
            supplier_id = fetch[0]
            quantity = int(data['quantity'])
            new_stock = old_stock + quantity
            self.cursor.execute("update inventory set stock = %s where product_code = %s", (new_stock, product_code,))
            self.conn.commit()

            dt = date.today()
            self.cursor.execute(
                "insert into orders(supplier_id,order_date,product_code,status,Quantity) values (%s,%s,%s,%s,%s)",
                (supplier_id, dt, product_code, data['status'], data['quantity']))
            self.conn.commit()
            return {"status": "Order table updated."}, 200
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self, data):
        try:
            lista = []
            dt = data['date']
            self.cursor.execute("select * from orders where order_date = %s", (dt,))
            fetch = self.cursor.fetchall()
            for i in range(len(fetch)):
                data = fetch[i]
                values = {
                    "Supplier_id": data[1],
                    "Order_date": data[2],
                    "Product_code": data[3],
                    "Status": data[4],
                    "Quantity": data[5]
                }
                lista.append(values)
            return {"Orders_Info": lista}, 200
        except Error as e:
            return {"Error": str(e)}, 404


if __name__ == '__main__':
    app.run(debug=True)

