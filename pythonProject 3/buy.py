import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import date
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for the whole app


class PersonalInfo:
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

    def purchase(self, data):
        try:
            datee = date.today()
            # Ensure that the input data is a list of entries
            # if not isinstance(data, list):
            #     return {"Error": "Invalid input format. Expected a list of entries."}, 400
            for i in data:
                price = i.get('price')
                remaining = i.get('remaining', "")
                if remaining == "":
                    remaining = None
                self.cursor.execute("INSERT INTO buying (buy_price, buy_date, remaining) values(%s, %s, %s)",(price, datee, remaining))
            self.conn.commit()
            return {"status": "Info entered successfully"}, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view_total_purchase(self, data):
        try:
            lista = []
            total_buy_price = 0  # Variable
            total_remaining = 0
            day = data["days"]
            self.cursor.execute("SELECT id, buy_price, remaining, buy_date FROM buying WHERE buy_date BETWEEN CURDATE() - INTERVAL %s DAY AND CURDATE()",(day,))
            results = self.cursor.fetchall()
            for i in results:
                buy_price = i[1] if i[1] is not None else 0  # Handle None for buy_price
                remaining = i[2] if i[2] is not None else 0  # Handle None for remaining
                buy_date = i[3]

                vals = {
                    "id": i[0],
                    "buy_price": buy_price,
                    "remaining": remaining,
                    "buy_date": buy_date.strftime("%Y-%m-%d")
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

    def total_sell_purchase(self, data):
        try:
            day = data['days']
            self.cursor.execute("SELECT SUM(sell_price), SUM(CASE WHEN remaining IS NOT NULL THEN remaining ELSE 0 END)  FROM selling  WHERE sell_date BETWEEN CURDATE() - INTERVAL %s DAY AND CURDATE()",(day,))
            result = self.cursor.fetchone()
            total_sell = result[0]
            sell_remaining = result[1]

            self.cursor.execute("SELECT SUM(buy_price), SUM(CASE WHEN remaining IS NOT NULL THEN remaining ELSE 0 END) FROM buying  WHERE buy_date BETWEEN CURDATE() - INTERVAL %s DAY AND CURDATE()",(day,))
            result = self.cursor.fetchone()
            total_buy = result[0]
            purchase_remaining = result[1]

            profit = total_sell - total_buy
            vals = {"Information": {
                f"Total_purchase of {day} days": total_buy,
                f"Purchase_remaining ": purchase_remaining,
                f"Total_sell of {day} days": total_sell,
                f"Sell_remaining ": sell_remaining,
                f"Total_Profit of {day} days ": profit
            }}
            return vals, 200
        except Error as e:
            return {"Error": f"{e}"}, 404

#
# @app.route('/enter_purchase', methods=['POST', 'GET'])
# def enter_purchase():
#     data = request.get_json()
#     db = PersonalInfo()
#     response, status_code = db.purchase(data)
#     return jsonify(response), status_code
#
#
# @app.route('/view_purchase', methods=['POST', 'GET'])
# def view_purchase():
#     data = request.get_json()
#     db = PersonalInfo()
#     response, status_code = db.view_total_purchase(data)
#     return jsonify(response), status_code
#
#
# @app.route('/tot_sell_purchase', methods=['GET', 'POST'])
# def tot_sell_purchase():
#     data = request.get_json()
#     db = PersonalInfo()
#     response, status_code = db.total_sell_purchase(data)
#     return jsonify(response), status_code


# if __name__ == "__main__":
#     app.run(debug=True)
