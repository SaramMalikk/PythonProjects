import mysql.connector
from mysql.connector import Error
from flask import Flask
from datetime import datetime, timedelta, date


app = Flask(__name__)


class Rentals:
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

    def booking(self, data):
        try:
            self.cursor.execute("SELECT name FROM cars WHERE id = %s", (data['car_id'],))
            fetch_car_info = self.cursor.fetchone()
            if fetch_car_info is None:  # this query is just to find the car_id correct
                return {"Error": "Invalid Rental id. Check if the ID exists"}, 404

            self.cursor.execute("SELECT start_date,end_date FROM rentals WHERE car_id = %s AND start_date >= CURDATE()"
                                , (data['car_id'],))
            fetch_car_info = self.cursor.fetchall()
            if fetch_car_info is None:
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
                duration_days = data['duration']
                end_date = start_date + timedelta(days=duration_days)
                city = data['city'].upper()

                self.cursor.execute('select id from branches where name =%s', (city,))
                fetch = self.cursor.fetchone()
                if not fetch:
                    return {"Error": "No branch found. Check if the branch exists"}, 404
                branch_id = fetch[0]

                city_detail = data['city_detail']
                if city_detail:
                    self.cursor.execute("select r.outcity_rent from rent_prices r where car_id = %s "
                                        "and r.branch_city_id = %s", (data['car_id'], branch_id))
                    fetch = self.cursor.fetchone()

                if not city_detail:
                    self.cursor.execute("select r.daily_city_rent from rent_prices r where car_id = %s "
                                        "and r.branch_city_id = %s", (data['car_id'], branch_id))
                    fetch = self.cursor.fetchone()

                rent_price = fetch[0]
                cost = duration_days * rent_price

                self.cursor.execute("INSERT INTO rentals(customer_id,car_id,start_date,end_date,total_cost,city) "
                                    "values(%s,%s,%s,%s,%s,%s)",
                                    (data['cus_id'], data['car_id'], start_date, end_date, cost, branch_id))
                self.conn.commit()
                # ID of the newly created booking
                booking_id = self.cursor.lastrowid
                val = {
                    'Status': "Booking created successfully. Please clear the payment.",
                    "Total_Cost": cost,
                    "Booking_ID": booking_id
                }
                return val, 201

            # Convert string start_date to a datetime.date
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()

            for booked_date in fetch_car_info:
                start_booked_date = booked_date[0]
                end_booked_date = booked_date[1]
                if start_booked_date == start_date or start_date <= end_booked_date:
                    return {"Status": "Car is not Available for the provided Starting date. Please check the Free Dates"}, 200

            duration_days = data['duration']
            end_date = start_date + timedelta(days=duration_days)

            city = data['city'].upper()
            self.cursor.execute('select id from branches where name =%s', (city,))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "No branch found. Check if the branch exists"}, 404
            branch_id = fetch[0]
            city_detail = data['city_detail']
            if city_detail:
                self.cursor.execute("select r.outcity_rent from rent_prices r where car_id = %s "
                                    "and r.branch_city_id = %s", (data['car_id'], branch_id))
                fetch = self.cursor.fetchone()
            if not city_detail:
                self.cursor.execute("select r.daily_city_rent from rent_prices r where car_id = %s "
                                    "and r.branch_city_id = %s", (data['car_id'], branch_id))
                fetch = self.cursor.fetchone()

            rent_price = fetch[0]
            cost = duration_days * rent_price
            self.cursor.execute("INSERT INTO rentals(customer_id,car_id,start_date,end_date,total_cost,city) "
                                "values(%s,%s,%s,%s,%s,%s)", (data['cus_id'], data['car_id'], start_date, end_date, cost, branch_id))
            self.conn.commit()
            # ID of the newly created booking
            booking_id = self.cursor.lastrowid

            val = {
                'Status': "Booking created successfully. Please clear the payment.",
                "Total_Cost": cost,
                "Booking_ID": booking_id
            }
            return val, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def edit(self, data):
        try:
            city = data['city'].upper()
            self.cursor.execute('select id from branches where name =%s', (city,))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "No branch found. Check if the branch exists"}, 404
            branch_id = fetch[0]
            city_detail = data['city_detail']
            if city_detail:
                self.cursor.execute("select r.outcity_rent from rent_prices r where car_id = %s "
                                    "and r.branch_city_id = %s", (data['car_id'], branch_id))
                fetch = self.cursor.fetchone()
            if not city_detail:
                self.cursor.execute("select r.daily_city_rent from rent_prices r where car_id = %s "
                                    "and r.branch_city_id = %s", (data['car_id'], branch_id))
                fetch = self.cursor.fetchone()

            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            duration_days = data['duration']
            end_date = start_date + timedelta(days=duration_days)

            rent_price = fetch[0]
            cost = duration_days * rent_price

            self.cursor.execute("SELECT total_cost FROM rentals WHERE id = %s", (data['rental_id'],))
            fetch = self.cursor.fetchone()
            if fetch is None:
                return {"Error": "Invalid rental_id. Check if ID exists."}
            previous_cost = int(fetch[0])

            self.cursor.execute(
                "UPDATE rentals SET car_id = %s, start_date = %s, end_date = %s, total_cost = %s, city = %s"
                " WHERE id = %s", (data['car_id'], start_date, end_date, cost, branch_id, data['rental_id']))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"Error": "No row updated. Check for the data double entry"}, 404

            if cost < previous_cost:
                return {"Your Return Money": previous_cost - cost, "Status": "Booking updated.",
                        "Previous Paid Money": previous_cost}, 201
            elif cost > previous_cost:
                return {"Your Remaining Money To Pay": cost - previous_cost, "Status": "Booking updated",
                        "Previous Paid Money": previous_cost}, 201
            else:
                return {"Status": "Booking updated. No cost adjustment needed."}, 200

        except Error as e:
            return {"Error": str(e)}, 500

    def cancel(self, data):
        try:
            self.cursor.execute("DELETE from rentals WHERE id = %s", (data['rental_id'],))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"Error": "No Booking found. Invalid rental ID"}, 404

            return {"Status": "Booking cancelled."}, 200
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self, data):
        try:
            self.cursor.execute("SELECT r.end_date, r.start_date , r.payment_status ,r.city, c.phone, c.firstname,"
                                " c.lastname, cars.name from rentals r left join customers c on r.customer_id = c.id "
                                "left join cars on r.car_id = cars.id WHERE r.id = %s ", (data['rental_id'],))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "Invalid rental_id .ID does not exists "}, 404
            if fetch[2] is None:
                return {"Error": "Sorry, Payment is not cleared."}, 404

            val = {"Booking_Info": {
                'Ending_Date': fetch[0],
                "Starting_Date": fetch[1],
                "Payment_Status": fetch[2],
                "Destination": fetch[3],
                "Customer_Phone": fetch[4],
                "FirstName": fetch[5],
                "LastName": fetch[6],
                "Car": fetch[7]
            }}
            return val, 200
        except Error as e:
            return {"Error": str(e)}, 500

    def availability(self, data):
        try:
            car = data['car']
            self.cursor.execute("SELECT name FROM cars WHERE id = %s", (car,))
            car_name = self.cursor.fetchall()
            if not car_name:
                return {"Error": "Invalid car ID. Check if exists"}, 404

            self.cursor.execute("SELECT start_date, end_date FROM rentals WHERE car_id = %s AND start_date >= CURDATE()", (car,))
            bookings = self.cursor.fetchall()
            if not bookings:
                return {"Status": "Car is Available. Rent your Car now Thanks!"}, 200

            unavailable_dates = []
            for i in bookings:
                start_date = i[0]
                end_date = i[1]
                unavailable_dates.append(f"Booked from {start_date} to {end_date}")

            return {"Booked Dates": unavailable_dates}, 200

        except Error as e:
            return {"Error": str(e)}, 500
