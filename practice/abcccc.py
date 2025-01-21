import mysql.connector
from datetime import datetime
import re
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saramali9",
    database="practice"
)
mycursor = mydb.cursor(buffered=True)
date_regex = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')   # only take values in 'yyyy-mm-dd' format
name_regex = re.compile(r'(^[a-zA-Z]+$)')    # only alphabets
address_regex = re.compile(r"[A-Za-z0-9'\.\-\s\,]")  # symbols which are not used in the address ( &(%#$^).
telephone_regex = re.compile(r"^((\+92)?(0092)?(92)?(0)?)(3)([0-9]{9})$")    # contains pakistani telephone format only
shift_regex = re.compile(r"(^[a-zA-Z0-9]+$)")    # alphabet and integers
batch_regex = re.compile(r"(^[0-9]+$)")     # only integers


def stu_enter_data():
    lista = []
    try:
        firstname = input("enter firstname ")
        lista.append(firstname)
    except TypeError:
        print('letters only please ')
    try:
        lastname = input('enter lastname ')
        lista.append(lastname)
    except TypeError:
        print('letters only please ')
    try:
        batch_no = input('enter batch_no ')
        lista.append(batch_no)
    except TypeError:
        print('integers only please')
    try:
        address = input('enter address ')
        lista.append(address)
    except TypeError:
        print('Does not support special symbols ')
    try:
        telephone = input('enter telephone ')
        lista.append(telephone)
    except TypeError:
        print('telephone format is wrong ')
    cls_code = input('Enter class code ')
    lista.append(cls_code)
    try:
        shift = input('enter shift ')
        lista.append(shift)
    except TypeError:
        print('letters and integers')
    try:
        birthdate = str(input('enter birthdate '))
        lista.append(birthdate)
    except TypeError:
        print('Put birthdate in yyyy-mm-dd format')
    return lista


def validate_stu_data():
    lista = stu_enter_data()
    firstname = lista[0]
    if not name_regex.match(firstname):
        print("Firstname should be in alphabets only  ")
        v_firstname = False
    else:
        v_firstname = True
    lastname = lista[1]
    if not name_regex.match(lastname):
        print("Firstname should be in alphabets only  ")
        v_lastname = False
    else:
        v_lastname = True
    batch_no = lista[2]
    if not batch_regex.match(batch_no):
        print("Batch_no only contains alphabets and integers  ")
        v_batch_no = False
    else:
        v_batch_no = True
    address = lista[3]
    if not address_regex.match(address):
        print("Address format does not support special symbols  ")
        v_address = False
    else:
        v_address = True
    telephone = lista[4]
    if not telephone_regex.match(telephone):
        print("invalid phone format ")
        v_telephone = False
    else:
        v_telephone = True
    cls_code = lista[5]
    shift = lista[6]
    if not shift_regex.match(shift):
        print("Shift format only contains alphabets and integers  ")
        v_shift = False
    else:
        v_shift = True
    birthdate = lista[7]
    if not date_regex.match(birthdate):
        print("birthdate format only take values in 'yyyy-mm-dd' format ")
        v_birthdate = False
    else:
        v_birthdate = True

    if v_firstname and v_lastname and v_batch_no and v_address and v_telephone and v_shift and v_birthdate == True:
        return lista
    else:
        return []


def create_students():
    lista = validate_stu_data()
    if len(lista) == 0:
        print('Student is not inserted ')
    elif len(lista) > 0:
        mycursor.execute("select id from classes where code = %s ",(lista[5],))
        result = list(mycursor.fetchone())
        classid = result[0]

        mycursor.execute('select numericno from students order by numericno desc ')
        result = list(mycursor.fetchone())
        numeric_id = result[0]

        batch = lista[2][-2:]
        last_roll = str((numeric_id) +1)
        new_roll = lista[5].upper()+batch+last_roll
        print(new_roll)
        mycursor.execute("insert into students (firstname,lastname,batchno,address,telephone,classid,shift,roll,numericno,birthdate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(lista[0],lista[1],lista[2],lista[3],lista[4],classid,lista[6],new_roll,last_roll,lista[7]))
        mydb.commit()
        print('Student created successfully')


def view_students():
    roll = input("Enter student's roll no ")
    mycursor.execute("select * from students where  roll = %s",(roll,))
    result = mycursor.fetchone()
    dic = {'id': result[0], 'firstname': result[1], 'lastname': result[2], 'betachno': result[3],'address': result[4],'telephone': result[5], 'class id': result[6], 'shift': result[7], 'roll no': result[8], 'nid': result[9], 'birth date': result[10]}
    print(dic)


def view_students_byclass():
    cls_code = input('Enter code of class ')
    mycursor.execute("select id from classes where code = %s ",(cls_code,))
    result = mycursor.fetchone()
    cls_id = result[0]
    mycursor.execute("select * from students where  classid = %s",(cls_id,))
    result=mycursor.fetchall()
    for i in result:
        print(i)


def create_teacher():
    firstname = input('Enter firstname ')
    lastname = input('Enter lastname ')
    password = input('Enter password ')

    mycursor.execute('select numericno from students order by numericno desc ')
    result = list(mycursor.fetchone())
    numeric_id = str((result[0])+1)
    new_code = 'T'+numeric_id
    mycursor.execute("insert into teachers(firstname,lastname,tcode,nid,password) values(%s,%s,%s,%s,%s)",(firstname, lastname, new_code, numeric_id,password))
    mydb.commit()


def view_teachers():
    teacher_code = input("Enter teacher code ")
    mycursor.execute("select * from teachers  where tcode = %s", (teacher_code,))
    result = mycursor.fetchone()
    print(result)


def view_all_teachers():
    mycursor.execute("select * from teachers  ")
    result = mycursor.fetchall()
    for i in result:
        print(i)


def login_teacher():
    code = input('Enter code ')
    password = input('Enter password ')
    mycursor.execute("select * from teachers  where tcode = %s and password =%s", (code,password))
    result = mycursor.fetchall()
    global teachercode
    if len(result) == 0:
        print('invalid code or password')
    elif len(result) == 1:
        print('Welcome', result[0][1])
        teachercode = code
        call_functions()
        

def create_classes():
    cls_name = input('Enter  name ')
    cls_code = input('Enter code ')
    mycursor.execute("insert into classes(name,code) values(%s,%s)", (cls_name,cls_code))
    mydb.commit()


def view_classes():
    name = input('Enter class code ')
    mycursor.execute("select * from classes  where code = %s", (name,))
    result = mycursor.fetchone()
    print(result)


def view_all_classes():
    mycursor.execute("select * from classes")
    result = mycursor.fetchall()
    for i in result:
        print(i)


def mark_attendance():
    cls_code = input('enter class code ')
    mycursor.execute("select id from classes where code = %s ", (cls_code,))
    result = list(mycursor.fetchone())
    cls_id = result[0]

    mycursor.execute("select * from students where classid =%s", (cls_id,))
    studentlist = list(mycursor.fetchall())

    mycursor.execute("select id from teachers where tcode=%s", (teachercode,))
    result = list(mycursor.fetchone())
    teacher_id = result[0]

    subject = input('Enter subject name ')
    mycursor.execute("select id from subjects where names=%s",(subject,))
    result = list(mycursor.fetchone())
    subject_id = result[0]

    x = datetime.now()
    date_time = x.strftime("%m/%d/%Y, %H:%M:%S")

    for i in range(len(studentlist)):
        attendance = input(f"{studentlist[i][1]} is Present or Absent? ")
        if attendance.upper() == 'P':
            attendance = True
        elif attendance.upper() == 'A':
            attendance = False
        mycursor.execute("insert into attendance(sid,tid,subid,dtime,Ispresent,classid) values(%s,%s,%s,%s,%s,%s)",(studentlist[i][0],teacher_id,subject_id,date_time,attendance,cls_id))
        mydb.commit()


def show_attendance():
    mycursor.execute("Select s.firstname as Student,c.name as Class,su.names as Subject,t.firstname as Teacher,att.dtime as datetime , Case when att.Ispresent = 1 then 'Present' when att.Ispresent= 0 then 'Absent' End As 'Attendance' from attendance att left join students s on att.sid = s.id left join classes c on att.classid = c.id left join teachers t on t.id = att.tid left join subjects su on att.subid = su.id")
    result = mycursor.fetchall()
    for i in result:
         print(i)
    # print(result)


def call_functions():
    name = input('Enter function name ')
    if name == 'create_students':
        create_students()
    elif name == 'view_students':
        view_students()
    elif name == 'view_students_byclass':
        view_students_byclass()
    elif name == 'create_teacher':
        create_teacher()
    elif name == 'view_teachers':
        view_teachers()
    elif name == 'view_all_teachers':
        view_all_teachers()
    elif name == 'create_classes':
        create_classes()
    elif name == 'view_classes':
        view_classes()
    elif name == ' view_all_classes':
        view_all_classes()
    elif name == 'mark_attendance':
        mark_attendance()
    elif name == 'show_attendance':
        show_attendance()
    else:
        print('Invalid function ')


show_attendance()

