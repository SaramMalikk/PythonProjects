import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import date
app = Flask(__name__)


class SellInfo:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'shop_bills'  # Replace with your MySQL database name
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

    def sell(self, data):
        try:
            datee = date.today()
            remaining = data['remaining']
            if remaining == "":
                remaining = None
            self.cursor.execute("INSERT INTO selling (sell_price, sell_date, remaining, goat_id) values(%s,%s,%s,%s)", (data['price'], datee, remaining, data['g_id']))
            self.conn.commit()
            return {"status": "Info entered successfully"}, 201
        except Error as e:
            return {"Error": f"{e}"}, 404

    def view_total_sell(self, data):
        try:
            lista = []
            total_buy_price = 0  # Variable
            total_remaining = 0
            day = data["days"]
            self.cursor.execute("SELECT goat_id, sell_price, remaining, sell_date FROM selling WHERE sell_date BETWEEN CURDATE() - INTERVAL %s DAY AND CURDATE()",(day,))
            results = self.cursor.fetchall()
            for i in results:
                buy_price = i[1] if i[1] is not None else 0  # Handle None for buy_price
                remaining = i[2] if i[2] is not None else 0  # Handle None for remaining
                sell_date = i[3]
                vals = {
                    "Goat_id": i[0],
                    "buy_price": buy_price,
                    "remaining": remaining,
                    "sell_date": sell_date.strftime("%Y-%m-%d")

                }
                lista.append(vals)
                total_buy_price += float(buy_price)  # Check it's treated as a float
                total_remaining += float(remaining)
            values = {
                f"Total_sell of {day} days": total_buy_price,
                "Remaining": total_remaining,
                "Purchase": lista
            }
            return values, 200
        except Error as e:
            return {"Error": f"{e}"}, 404
#
# @app.route('/enter_sell', methods=['POST'])
# def enter_sells():
#     data = request.get_json()
#     db = SellInfo()
#     response, status_code = db.sell(data)
#     return jsonify(response), status_code
#
#
# @app.route('/view_sell', methods=['POST'])
# def view_sell():
#     data = request.get_json()
#     db = SellInfo()
#     response, status_code = db.view_sell_data(data)
#     return jsonify(response), status_code
#
#
# if __name__ == "__main__":
#     app.run(debug=True)