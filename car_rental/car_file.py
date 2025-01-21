import mysql.connector
from mysql.connector import Error
from flask import Flask
app = Flask(__name__)


class Cars:
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
            self.cursor.execute("INSERT INTO cars(name,number_plate,year) values(%s,%s,%s)",
                                (data['name'], data['number'], data['year']))
            self.conn.commit()
            # Retrieve the ID of the newly created car
            car_id = self.cursor.lastrowid

            val = {
                "Status": "Car created.",
                "Car_ID": car_id
            }
            return val, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def view(self, data):
        try:
            branch = data['city'].upper()
            self.cursor.execute("SELECT id FROM branches WHERE name = %s ", (branch,))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "Invalid input or Branch name."}, 404
            branch_id = fetch[0]
            self.cursor.execute("select c.id, c.name , c.number_plate, c.year , r.daily_city_rent, r.outcity_rent,"
                                "r.fuel_tolls , b.name from cars c left join rent_prices r on c.id = r.car_id "
                                "left join branches b on b.id = r.branch_city_id where c.id = %s "
                                "and r.branch_city_id = %s", (data['car_id'], branch_id))
            cars = self.cursor.fetchone()
            if not cars:
                return {"Error": "Invalid car_id. Check if the ID exists."}, 404
            val = {"Cars_Info": {
                    "Name": cars[0],
                    "Number": cars[1],
                    "Model_Year": cars[2],
                    "DailyCity_Rent": cars[3],
                    "OutCity_Rent_": cars[4],
                    "FuelAndTolls": cars[5]
                }}
            return val, 200
        except Error as e:
            return {"Error": str(e)}, 500

    def view_all(self):
        try:
            lista = []
            self.cursor.execute("select c.id, c.name , c.number_plate, c.year , r.daily_city_rent, r.outcity_rent,"
                                "r.fuel_tolls , b.name from cars c left join rent_prices r on c.id = r.car_id "
                                "left join branches b on b.id = r.branch_city_id")
            fetch = self.cursor.fetchall()

            for cars in fetch:
                val = {"Cars_Info": {
                    "Car_ID": cars[0],
                    "Name": cars[1],
                    "Number": cars[2],
                    "Model_Year": cars[3],
                    "DailyCity_Rent": cars[4],
                    "OutCity_Rent_": cars[5],
                    "FuelAndTolls": cars[6],
                    "Branch_Name": cars[7]
                }}

                lista.append(val)

            return lista, 200
        except Error as e:
            return {"Error": str(e)}, 500

    def remove(self, data):
        try:
            self.cursor.execute("DELETE from cars WHERE id = %s", (data['id'],))
            self.conn.commit()

            if self.cursor.rowcount == 0:
                return {"Error": "No row effect. Checked if the ID exists."}, 404

            return {"Status": "Car Deleted."}, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def edit(self, data):
        try:
            self.cursor.execute("UPDATE cars set name = %s, number_plate = %s , year = %s"
                                " WHERE id = %s", (data['name'], data['number'], data['year'], data['id']))
            self.conn.commit()

            if self.cursor.rowcount == 0:
                return {"Status": "No rows updated. Check if the ID exists."}, 404

            return {"Status": "Car updated."}, 201
        except Error as e:
            return {"Error": str(e)}, 500

    def create_rent(self, data):
        try:
            branch = data['branch_city'].upper()
            self.cursor.execute("SELECT id FROM branches WHERE name = %s ", (branch,))
            fetch = self.cursor.fetchone()
            if not fetch:
                return {"Error": "No branch found. Check if exists."}, 404
            city_id = fetch[0]

            self.cursor.execute("INSERT INTO rent_prices (car_id,branch_city_id,daily_city_rent,outcity_rent,"
                                "fuel_tolls)values (%s,%s,%s,%s,%s)",
                                (data['car_id'], city_id, data['city_rent'], data['outcity_rent'], "Not_Included"))
            self.conn.commit()
            return {"Status": "Rent created successfully. "}, 201
        except Error as e:
            return {"Error": str(e)}, 500
