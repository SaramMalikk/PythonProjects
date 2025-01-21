import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import date
from flask_cors import CORS  # Import CORS
app = Flask(__name__)

CORS(app)


class Products:
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

    def products_data(self, data):
        try:
            dt = date.today()
            self.cursor.execute("SELECT product_id FROM products ORDER BY product_id DESC")
            result = self.cursor.fetchone()
            if result is None:
                product_id = 1
            else:
                product_id = result[0] + 1

            product_code = 'BCN' + str(product_id)  # bar code number BNC
            self.cursor.execute("select id from suppliers where email=%s", (data['supplier'],))
            fetch = self.cursor.fetchone()
            supplier_id = fetch[0]
            self.cursor.execute("INSERT INTO products (name, product_code, product_id,price, category_id, supplier_id) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (data['name'].upper(), product_code, product_id, data['sellPrice'], data['category'], supplier_id))
            self.conn.commit()
            des = data['description'].upper()
            stock = 0
            self.cursor.execute("insert into inventory (product_code,stock,purchasing_price,date,description) "
                                "values (%s,%s,%s,%s,%s)", (product_code, stock, data['purchasePrice'], dt, des))
            self.conn.commit()
            return {"Status": "Data entered successfully"}, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self, data):
        try:
            product_code = data['code']

            self.cursor.execute("select p.name,p.price,p.category_id,p.supplier_id,i.stock from products p left join"
                                " inventory i on p.product_code = i.product_code where p.product_code = %s", (product_code,))
            fetched_result = list(self.cursor.fetchall())
            values = fetched_result[0]

            val = {"Product_Info": {
                "Name": values[0],
                "price": values[1],
                "category_id": values[2],
                "supplier_id": values[3],
                "Available_stock": values[4]
            }}
            return val, 200
        except Error as e:
            return {"Error": str(e)}, 404

    def view_all(self):
        try:
            lista = []
            self.cursor.execute("select p.*,i.purchasing_price from products p left join inventory i "
                                "on p.product_code = i.product_code")
            fetch_data = self.cursor.fetchall()
            for i in fetch_data:
                val = {
                    "Name": i[1],
                    "Code": i[2],
                    "Selling_price": i[4],
                    "Purchasing_price": i[7]
                }
                lista.append(val)
            return lista, 200
        except Error as e:
            return {"Error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
    