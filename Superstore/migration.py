from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql  # we use this to solve no module mysql error
pymysql.install_as_MySQLdb()  # we use this to solve no module mysql error
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:saramali9@localhost/superstore'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    product_code = db.Column(db.String(120), nullable=False, unique=True)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(80), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)



class Suppliers(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(80), db.ForeignKey('products.product_code', ondelete='CASCADE'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    purchasing_price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(80), nullable=True)


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    product_code = db.Column(db.String(80), db.ForeignKey('products.product_code', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(80), nullable=True)
    Quantity = db.Column(db.Integer, nullable=False)


class Sell(db.Model):
    __tablename__ = 'sell'
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(80), db.ForeignKey('products.product_code', ondelete='CASCADE'), nullable=False)
    method = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    profit = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=True)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    hired_date = db.Column(db.Date, nullable=False)


# to run  migration file  we first use 'export FLASK_APP=[YOUR_APP_FILE].py ' then 'flask db init' commands
# to create migration 'flask db migrate' command and to give some msg 'flask db migrate -m "msg" '
# to create or to do changes in tables in database  ' flask db upgrade' command


if __name__ == "__main__":
    app.run(debug=True)
