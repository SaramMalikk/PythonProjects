import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import date
app = Flask(__name__)


class Sell:
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

    def view(self, data):
        try:
            days = data['days']
            self.cursor.execute("SELECT SUM(profit) FROM sell WHERE date BETWEEN CURDATE() - INTERVAL %s DAY "
                                "AND CURDATE()", (days,))
            fetch = self.cursor.fetchone()
            profit = fetch[0]
            self.cursor.execute("SELECT SUM(amount) FROM sell WHERE date BETWEEN CURDATE() - INTERVAL %s DAY"
                                " AND CURDATE()", (days,))
            fetch = self.cursor.fetchone()
            result = fetch[0]
            if days == 1:
                value = {"Sell_info": {
                    f"total_sell of {days} day ": result,
                    "Total Profit": profit

                }}
            else:
                value = {"Sell_info": {
                    f"total_sell of {days} days ": result,
                    "Total Profit": profit
                }}
            return value, 200
        except Error as e:
            return {"Error": str(e)}, 404

    def view_by_date(self, data):
        try:
            error = []
            self.cursor.execute('select sum(profit) from sell where date = %s', (data['date'],))
            fetch = list(self.cursor.fetchone())
            if fetch[0] is None:
                error.append({"Error": "No profit on this date"})
            profit = fetch[0]

            self.cursor.execute('select sum(amount) from sell where date = %s', (data['date'],))
            fetch = self.cursor.fetchone()
            if fetch[0] is None:
                error.append({"Error": "No sell on this date"})
            sell = fetch[0]
            val = {
                "Total_sell": sell,
                "Total_profit": profit
            }
            if error:
                return {"Errors": error}, 400

            return val, 200

        except Error as e:
            return {"Error": str(e)}, 500

    def sell_data(self, data):
        try:
            dt = date.today()
            bill = []
            bill_amount = 0
            error = []
            method = data['method'].upper()
            products = data['products']

            for product in products:
                product_code = product['code'].upper()
                quantity = product['quantity']

                self.cursor.execute("SELECT price,name FROM products WHERE product_code = %s", (product_code,))
                result = self.cursor.fetchone()
                if result is None:
                    error.append({"Error": "Product_code is not valid"}), 404
                    continue

                sell_price = result[0]
                product_name = result[1]

                self.cursor.execute("SELECT purchasing_price FROM inventory WHERE product_code = %s", (product_code,))
                result = self.cursor.fetchone()
                purchasing_price = result[0]

                self.cursor.execute("SELECT stock FROM inventory WHERE product_code = %s", (product_code,))
                result = self.cursor.fetchone()
                stock = result[0]
                if stock < quantity:
                    error.append({"Error": f"Insufficient stock for {product_name}. Only {stock} units available."}), 400
                    continue
                new_stock = stock - quantity
                self.cursor.execute("UPDATE inventory SET stock = %s WHERE product_code = %s", (new_stock, product_code))
                self.conn.commit()

                total_amount = sell_price * quantity
                cost_price = purchasing_price * quantity
                profit = total_amount - cost_price

                self.cursor.execute("INSERT INTO sell(product_code, method, quantity, date, amount, profit) "
                                    "VALUES (%s, %s, %s, %s, %s, %s)", (product_code, method, quantity, dt, total_amount, profit))
                self.conn.commit()
                vals = {
                    "Quantity": quantity,
                    "Name": product_name,
                    "Total_Price": total_amount,

                }
                bill.append(vals)
                bill_amount += total_amount
            return {"Receipt": bill, "Total_Amount": bill_amount, "Error": error}, 200
        except Exception as e:
            return {"Error": str(e)}, 500
