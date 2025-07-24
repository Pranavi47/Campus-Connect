from . import db
from flask_login import UserMixin

# PGPASSWORD=OoyFmIHJodYr5N08T80GHEbmd3P4yYX7 psql -h dpg-con7hvsf7o1s73ff246g-a.singapore-postgres.render.com -U campus_connect_user campus_connect

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    user_role = db.Column(db.String(20))

    def __init__(self, username, password, user_role):
        self.username = username
        self.password = password
        self.user_role = user_role

    def create_user(self):
        db.session.add(self)
        if self.user_role == 'STUDENT':
            student = Student.query.get(self.username.upper())
            print(student)
            student.user_id = self.id
        elif self.user_role == 'TEACHER':
            teacher = Teacher.query.get(self.username.upper())
            teacher.user_id = self.id
        elif self.user_role == 'ADMIN':
            admin = Admin.query.get(self.username.upper())
            admin.user_id = self.id
        db.session.commit()

    def getUsers():
        users = User.query.all()
        return users

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(50), unique = True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, id, name, gender, dob, email, phone, address):
        self.id = id
        self.name = name.title()
        self.gender = gender
        self.date_of_birth = dob
        self.email = email
        self.phone = phone
        self.address = address

    def create_Admin(self):
        db.session.add(self)
        db.session.commit()

    def get_Admin(id):
        admin = Admin.query.filter(Admin.user_id==id).first()
        return admin

class Student(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(50), unique = True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, id, name, gender, date_of_birth, email, phone, address, class_id, user_id):
        self.id = id
        self.name = name.title()
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone = phone
        self.address = address
        self.class_id = class_id
        self.user_id = user_id

    def create_Student(student):
        db.session.add(student)
        db.session.commit()

    def get_student(id):
        student = Student.query.filter(Student.id.like(f'%{id}%')).all()
        return student

    def get_students():
        students = Student.query.order_by(Student.id).all()
        return students
    
    def UnReg_stud():
        students = Student.query.with_entities(Student.id,Student.name,Student.gender,Student.date_of_birth).order_by(Student.id).filter(Student.user_id == None).all()
        return students

    def updateStudent(roll,name,gender, dob, phone, email, class_id, address):
        student = Student.query.get(roll)
        student.name = name
        student.gender = gender
        student.date_of_birth = dob
        student.phone = phone
        student.email = email
        student.address = address
        if class_id == None:
            student.class_id = "Null"
        db.session.commit()

    def assignClass(id, class_id):
        student = Student.query.get(id)
        student.class_id = class_id
        db.session.commit()

    def delete(id):
        student = db.session.query(Student).filter(Student.id==id).first()
        db.session.delete(student)
        db.session.commit()

class Teacher(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(50), unique = True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    experience = db.Column(db.Integer)
    date_of_joining = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,id,name,gender,dob,email,phone,address,doj,experience,user_id):
        self.id = id
        self.name = name.title()
        self.gender = gender
        self.date_of_birth = dob
        self.email = email
        self.phone = phone
        self.address = address
        self.experience = experience
        self.date_of_joining = doj
        self.user_id = user_id

    def create_Teacher(self):
        db.session.add(self)
        db.session.commit()

    def getTeacher(id):
        teachers = Teacher.query.filter(Teacher.id.like(f'%{id}%')).all()
        return teachers

    def getTeachers():
        teachers = Teacher.query.order_by(Teacher.id).all() 
        return teachers

    def updateTeacher(id, name, gender, dob, phone, email, address, experience, doj):
        teacher = Teacher.query.get(id)
        teacher.name = name
        teacher.gender = gender
        teacher.date_of_birth = dob
        teacher.phone = phone
        teacher.email = email
        teacher.address = address
        teacher.experience = experience
        teacher.date_of_joining = doj
        db.session.commit()

    def UnReg_teach():
        teachers = Teacher.query.with_entities(Teacher.id, Teacher.name, Teacher.gender, Teacher.date_of_birth).order_by(Teacher.id).filter(Teacher.user_id == None).all()
        return teachers
    
    def delete(id):
        teacher = db.session.query(Teacher).filter(Teacher.id==id).first()
        db.session.delete(teacher)
        db.session.commit()


class Course(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def create_Course(self):
        db.session.add(self)
        db.session.commit()

    def getCourses():
        courses = Course.query.order_by(Course.id).all()
        return courses
    
    def getCourse(id):
        course = Course.query.filter(Course.id.like(f'%{id}%')).first()
        return course

    def updateCourse(id, idn, name):
        course = Course.query.get(id)
        course.id = idn
        course.name = name
        db.session.commit()
    
    def delete(id):
        course = db.session.query(Course).filter(Course.id==id).first()
        db.session.delete(course)
        db.session.commit()

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Branch_name = db.Column(db.String(50))
    section = db.Column(db.String(5))
    mentor = db.Column(db.String(15), db.ForeignKey('teacher.id'))
    year = db.Column(db.String(10))

    def __init__(self, branch_name, section, mentor, year):
        self.Branch_name = branch_name
        self.section = section
        self.mentor = mentor
        self.year = year

    def create_Class(self):
        db.session.add(self)
        db.session.commit()

    def getClasses():
        classes = Class.query.order_by(Class.id).all()
        return classes
    
    def getClass(id):
        class_ = Class.query.get(id)
        return class_
    
    def updateClass(id, branch_name, section, mentor, year):
        class_ = Class.query.get(id)
        class_.Branch_name = branch_name
        class_.section = section
        class_.mentor = mentor
        class_.year = year
        db.session.commit()
    
    def delete(id):
        class_ = db.session.query(Class).filter(Class.id==id).first()
        db.session.delete(class_)
        db.session.commit()

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(15), db.ForeignKey('student.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    course_id = db.Column(db.String(20), db.ForeignKey('course.id'))
    date = db.Column(db.Date)
    status = db.Column(db.String(20))

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(15), db.ForeignKey('student.id'))
    course_id = db.Column(db.String(20), db.ForeignKey('course.id'))
    marks = db.Column(db.Integer)
    exam_type = db.Column(db.String(20))
    date = db.Column(db.Date)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(15), db.ForeignKey('teacher.id'))
    course_id = db.Column(db.String(20), db.ForeignKey('course.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    Assignment_name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    due_date = db.Column(db.Date)

class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(15), db.ForeignKey('student.id'))
    amount = db.Column(db.Integer)
    fee_type = db.Column(db.String(20))
    date = db.Column(db.Date)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    date = db.Column(db.Date)
    description = db.Column(db.String(200))
    link = db.Column(db.String(200))

    def __init__(self, name, date, description, link):
        self.name = name
        self.date = date
        self.description = description
        self.link = link
    
    def create_Event(self):
        db.session.add(self)
        db.session.commit()

    def get_Events():
        events = Events.query.order_by(Events.id).all()
        return events
    
    def get_Event(id):
        event = Events.query.order_by(Events.id).first()
        return event
    
    def updateEvent(id, name, date, description, link):
        event = Events.query.get(id)
        event.name = name
        event.date = date
        event.description = description
        event.link = link

    def delete(id):
        event = db.session.query(Events).filter(Events.id==id).first()
        db.session.delete(event)
        db.session.commit()

class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    day = db.Column(db.String(10))
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    subject_id = db.Column(db.String(20), db.ForeignKey('course.id'))
    teacher_id = db.Column(db.String(15), db.ForeignKey('teacher.id'))