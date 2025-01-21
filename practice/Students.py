import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import re


app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

date_regex = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')  # only take values in 'yyyy-mm-dd' format
name_regex = re.compile(r'(^[a-zA-Z]+$)')  # only alphabets
address_regex = re.compile(r"[A-Za-z0-9'\.\-\s\,]")  # symbols which are not used in the address ( &(%#$^).
telephone_regex = re.compile(r"^((\+92)?(0092)?(92)?(0)?)(3)([0-9]{9})$")  # contains pakistani telephone format only
shift_regex = re.compile(r"(^[a-zA-Z0-9]+$)")  # alphabet and integers
batch_regex = re.compile(r"(^[0-9]+$)")


class Students:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'       # Replace with your MySQL username
        self.password = 'saramali9'   # Replace with your MySQL password
        self.database = 'practice'   # Replace with your MySQL database name
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

    def view_students(self, roll):

        try:
            self.cursor.execute("select * from students where  roll = %s", (roll,))
            result = self.cursor.fetchone()
            dic = {'id': result[0], 'firstname': result[1], 'lastname': result[2], 'betachno': result[3],
                   'address': result[4], 'telephone': result[5], 'class id': result[6], 'shift': result[7],
                   'roll no': result[8], 'nid': result[9], 'birth date': result[10]}
        except TypeError:
            return "No student under this roll no"
        return dic

    def view_students_byclass(self, classcode):
        lista = []
        try:
            self.cursor.execute("select id from classes where code = %s ", (classcode,))
            result = self.cursor.fetchone()
            classid = result[0]
            self.cursor.execute("select * from students where  classid = %s", (classid,))
            result = self.cursor.fetchall()
            for i in range(len(result)):
                abc = result[i]
                dic = {'id': abc[0], 'firstname': abc[1], 'lastname': abc[2], 'betachno': abc[3],'address': abc[4], 'telephone': abc[5], 'class id': abc[6], 'shift': abc[7],'roll no': abc[8], 'nid': abc[9], 'birth date': abc[10]}
                lista.append(dic)
            return lista
        except TypeError:
            return 'Class does not exist '

    def validate_stu_data(self, data):
        firstname = data["firstname"]
        if not name_regex.match(firstname):
            return "Firstname should be in alphabets only", 0
        lastname = data['lastname']
        if not name_regex.match(lastname):
            return "lastname should be in alphabets only", 0
        batch_no = data['batchno']
        if not batch_regex.match(batch_no):
            return " Batch_no only contains alphabets and integers ", 0
        address = data['address']
        if not address_regex.match(address):
            return "Address format does not support special symbols  ", 0
        telephone = data['telephone']
        if not telephone_regex.match(telephone):
            return "invalid phone format ", 0
        cls_code = data['classcode']
        shift = data['shift']
        if not shift_regex.match(shift):
            return "Shift format only contains alphabets and integers  ", 0
        birthdate = data['birthdate']
        if not date_regex.match(birthdate):
            return "birthdate format only take values in 'yyyy-mm-dd' format ", 0
        return data, 1

    def create_students(self, data):
        v = Students()
        tuple = v.validate_stu_data(data)
        if tuple[1] == 0:
            return 'Student is not inserted', tuple[0]
        elif tuple[1] == 1:
            self.cursor.execute("select id from classes where code = %s ", (data['classcode'],))
            result = list(self.cursor.fetchone())
            classid = result[0]

            self.cursor.execute('select numericno from students order by numericno desc ')
            result = list(self.cursor.fetchone())
            numeric_id = result[0]

            batch = data['batchno'][-2:]
            last_roll = str((numeric_id) +1)
            new_roll = data['classcode'].upper()+batch+last_roll
            print(new_roll)
            self.cursor.execute("insert into students (firstname,lastname,batchno,address,telephone,classid,shift,roll,"
                                "numericno,birthdate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (data['firstname'], data['lastname'], data['batchno'],data['address'],data['telephone']
                                 ,classid,data['shift'],new_roll,last_roll,data['birthdate']))
            self.conn.commit()
            print('Student created successfully')
            return "Student created successfully!"


#
# @app.route('/addroll', methods=['POST'])
# @jwt_required()
# def addroll():
#     data = request.get_json()
#     roll = data.get('roll')
#     db = Students()
#     response = db.view_students(roll)
#     return jsonify(response)

#
# @app.route('/classcode', methods=['POST'])
# @jwt_required()
# def classcode():
#     data = request.get_json()
#     clscode = data.get('clscode')
#     db = Students()
#     response = db.view_students_byclass(clscode)
#     return jsonify(response)


# @app.route('/createstudent', methods=['POST'])
# def createstudent():
#     data = request.get_json()
#     db = Students()
#     response = db.create_students(data)
#     return jsonify(response)

#
# if __name__ == "__main__":
#     app.run(debug=True)
