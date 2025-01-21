from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql  # we use this to solve no module mysql error
pymysql.install_as_MySQLdb()  # we use this to solve no module mysql error
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:saramali9@localhost/flask_mig'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    code = db.Column(db.String(80))


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    batch_no = db.Column(db.String(80), nullable=True)
    telephone = db.Column(db.Integer, nullable=False)
    shift = db.Column(db.String(80), nullable=True)
    roll_no = db.Column(db.String(80), nullable=True)
    birthdate = db.Column(db.DATE, nullable=True)
    numeric_id = db.Column(db.Integer, nullable=True)   # Integer's I should be capital
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete='CASCADE'), nullable=False)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)    # Integer's I should be capital
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    tcode = db.Column(db.String(80), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    numeric_id = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(50), nullable=False)


class Attend(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)    # Integer's I should be capital
    sid = db.Column(db.Integer, db.ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    tid = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete='CASCADE'), nullable=False)
    subid = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DATE, nullable=False)
    Ispresent = db.Column(db.Boolean, default=True)
# to run  migration file  we first use 'export FLASK_APP=[YOUR_APP_FILE].py' then 'flask db init' commands
# to create migration 'flask db migrate' command and to give some msg 'flask db migrate -m "msg" '
# to create or to do changes in tables in database  ' flask db upgrade' command


if __name__ == "__main__":
    app.run(debug=True)
