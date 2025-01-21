from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql  # we use this to solve no module mysql error
pymysql.install_as_MySQLdb()  # we use this to solve no module mysql error
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:saramali9@localhost/shop_bills'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(170), nullable=False)


class Goat(db.Model):
    __tablename__ = 'buying'
    goat_id = db.Column(db.Integer, primary_key=True)
    buy_price = db.Column(db.Integer, nullable=False)
    buy_date = db.Column(db.Date, nullable=False)
    remaining = db.Column(db.String(80), nullable=True)


class Selling(db.Model):
    __tablename__ = 'selling'
    id = db.Column(db.Integer, primary_key=True)
    goat_id = db.Column(db.Integer, db.ForeignKey('buying.goat_id', ondelete='CASCADE'), nullable=False)
    sell_price = db.Column(db.Integer, nullable=False)
    sell_date = db.Column(db.Date, nullable=False)
    remaining = db.Column(db.String(80), nullable=True)


# to run  migration file  we first use 'export FLASK_APP=[YOUR_APP_FILE].py' then 'flask db init' commands
# to create migration 'flask db migrate' command and to give some msg 'flask db migrate -m "msg" '
# to create or to do changes in tables in database  ' flask db upgrade' command


if __name__ == "__main__":
    app.run(debug=True)
