from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql  # we use this to solve no module mysql error
pymysql.install_as_MySQLdb()  # we use this to solve no module mysql error
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:saramali9@localhost/CarRental'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    license_number = db.Column(db.String(50), nullable=False, unique=True)
    license_expiry = db.Column(db.String(50), nullable=False)


class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number_plate = db.Column(db.String(50), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)


class Rentals(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id', ondelete="CASCADE"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(40), nullable=True)
    city = db.Column(db.String(40), nullable=True)


class Payments(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    rental_id = db.Column(db.Integer, db.ForeignKey('rentals.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String(50), nullable=False)


class Branches(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)


class CarRents(db.Model):
    __tablename__ = 'rents_prices'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id', ondelete='CASCADE'), nullable=True)
    branch_city_id = db.Column(db.Integer, db.ForeignKey('branches.id', ondelete='CASCADE'), nullable=True)
    daily_city_rent = db.Column(db.Integer, nullable=True)
    outcity_rent = db.Column(db.Integer, nullable=True)
    fuel_tolls = db.Column(db.String(50), nullable=True)


if __name__ == "__main__":
    app.run(debug=True)
