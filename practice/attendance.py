import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from datetime import datetime


class Att:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'practice'  # Replace with your MySQL database name
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

    def show_attendance(self):
        self.cursor.execute("Select s.firstname as Student,c.name as Class,su.names as Subject,t.firstname as Teacher,att.dtime as datetime , Case when att.Ispresent = 1 then 'Present' when att.Ispresent= 0 then 'Absent' End As 'Attendance' from attendance att left join students s on att.sid = s.id left join classes c on att.classid = c.id left join teachers t on t.id = att.tid left join subjects su on att.subid = su.id")
        result = self.cursor.fetchall()
        return result

    def show_attend_info(self, data):
        lista = []
        try:
            self.cursor.execute("select id,name from classes where code =%s", (data['ccode'],))
            class_id = self.cursor.fetchone()
            # class_id = res[0]
        except TypeError:
            return "Class code does not exist"
        try:
            self.cursor.execute("select id from subjects where names =%s", (data['subname'],))
            res = self.cursor.fetchone()
            sub_info = res[0]
        except TypeError:
            return "subject name does not exist"
        try:
            self.cursor.execute("select id,firstname from teachers  where tcode =%s", (data['teachcode'],))
            teacher_info = self.cursor.fetchone()
            # teacher_info = res[0]
        except TypeError:
            return "No teacher with this code"
        self.cursor.execute("select * from students  where classid =%s", (class_id[0],))
        students_info = list(self.cursor.fetchall())
        for i in range(len(students_info)):
            abc = students_info[i]
            dic = [{'student_id': abc[0], 'student_name': abc[1], 'class_id': class_id[0], 'class_name': class_id[1], 'sub_id': sub_info, 'teacher_id': teacher_info[0], 'teacher_name': teacher_info[1]}]
            lista.append(dic)
        return lista

    def mark_attendance(self, data):
        self.cursor.execute("SELECT id FROM classes WHERE code = %s", (data['classcode'],))
        result = self.cursor.fetchone()

        if not result:
            return 'Class not found', 404

        cls_id = result[0]

        # Fetch the teacher ID
        self.cursor.execute("SELECT id FROM teachers WHERE tcode = %s", (data['teachercode'],))
        result = self.cursor.fetchone()

        if not result:
            return 'Teacher not found', 404

        teacher_id = result[0]

        # Fetch the subject ID
        self.cursor.execute("SELECT id FROM subjects WHERE names = %s", (data['subject'],))
        result = self.cursor.fetchone()

        if not result:
            return 'Subject not found', 404

        subject_id = result[0]

        # Current timestamp
        x = datetime.now()
        date_time = x.strftime("%m/%d/%Y, %H:%M:%S")

        # Convert attendance status
        data['attendance'] = True if data['attendance'].upper() == 'P' else False

        # Insert attendance record
        self.cursor.execute(
            "INSERT INTO attendance(sid, tid, subid, dtime, Ispresent, classid) VALUES(%s, %s, %s, %s, %s, %s)",
            (data['studentid'], teacher_id, subject_id, date_time, data['attendance'], cls_id))
        self.conn.commit()

        return "Attendance marked successfully!", 200

# @app.route('/markedattend', methods=['POST'])
# def markedattend():
#     db = ATT()
#     response = db.show_attendance()
# #     return jsonify(response)

# @app.route('/showattendinfo', methods=['POST'])
# def showattendinfo():
#     data = request.get_json()
#     db = Att()
#     response = db.show_info(data)
#     return jsonify(response)


# @app.route('/markattend', methods=['POST'])
# def markattend():
#     data = request.get_json()
#     db = Teachers()
#     response = db.mark_attendance(data)
#     return jsonify(response)
#
# #
# if __name__ == "__main__":
#     app.run(debug=True)

