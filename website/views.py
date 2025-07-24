from flask import Blueprint, render_template, redirect, url_for, request
from . import models
from flask_login import login_required, current_user
from datetime import date
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")


######STUDENT SECTION######

@views.route('/home')
#@login_required
def home():
    events = models.Events.get_Events()
    upe=[]
    pe=[]
    for event in events:
        if event.date<date.today():
            pe.append(event)
        else:
            upe.append(event)
    return render_template("home.html", pastevents=pe, upcommingevents=upe)

@views.route('/attendance')
#@login_required
def attendance():
    return render_template("attendance.html")

@views.route('/marks')
#@login_required
def marks():
    return render_template("marks.html")

@views.route('/fees')
#@login_required
def fees():
    return render_template("fees.html")

@views.route('/assignments')
#@login_required
def assignments():
    return render_template("assignments.html")



#####TEACHER SECTION######


@views.route('/teacher_home')
#@login_required
def teacher_home():
    return render_template("teacher_home.html")

@views.route('/teacher_timetable/id=<id>', methods=['GET', 'POST'])
def teacher_timetable(id):
    return "HELLO"



######ADMIN SECTION######


@views.route('/admin_home')
@login_required
def admin_home():
    return render_template("admin_home.html")

@views.route('/add_student', methods=['GET', 'POST'])
#@login_required
def add_student():
    if request.method == 'POST':
        roll = request.form['rollno']
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dateofbirth']
        email = request.form['email']
        phno =  request.form['phno']
        address = request.form['address']
        student = models.Student(id=roll, name=name, gender=gender, date_of_birth=dob, email=email, phone=phno, address=address, user_id=None , class_id=None)
        models.Student.create_Student(student = student)
        return redirect(url_for('views.admin_home'))
    return render_template("add_student.html")

@views.route('/view_student', methods=['GET', 'POST'])
#@login_required
def view_student():
    query = request.args.get('query')
    if query is None:
        students = models.Student.get_students()
        return render_template("view_student.html", student = students)
    student = models.Student.get_student(query)
    return render_template("view_student.html", student = student)

@views.route('/delete/id=<id>')
#@login_required
def deleteStudent(id):
    models.Student.delete(id)
    return redirect(url_for('views.view_student'))

@views.route('/edit_student/id=<id>', methods=['GET', 'POST'])
#@login_required
def edit_student(id):
    student = models.Student.query.get(id)
    if request.method == 'POST':
        roll = request.form['rollno']
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dateofbirth']
        email = request.form['email']
        phno =  request.form['phno']
        address = request.form['address']
        class_id = request.form['class_id']
        models.Student.updateStudent(roll=roll, name=name, gender=gender, dob=dob, email=email, phone=phno, address=address, class_id=class_id)
        return redirect(url_for("views.admin_home"))
    return render_template("edit_student.html",student=student)

@views.route('/add_teacher', methods=['GET', 'POST'])
#@login_required
def add_teacher():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dateofbirth']
        email = request.form['email']
        phno =  request.form['phno']
        address = request.form['address']
        experience = request.form['experience']
        doj = request.form['dateofjoining']
        teacher = models.Teacher(id=id, name=name, gender=gender, dob=dob, email=email, phone=phno, address=address, user_id=None, experience=experience, doj=doj)
        teacher.create_Teacher()   
        return redirect(url_for('views.admin_home'))
    return render_template("add_teacher.html")

@views.route('/viewteachers')
#@login_required
def viewteachers():
    teachers = models.Teacher.getTeachers()
    return render_template("view_teacher.html", teachers = teachers)
# def deleteTeacher(id):
#     models.Teacher.delete(id)
#     return redirect(url_for('views.viewteachers'))



@views.route('/deleteTeacher/id=<id>')
#@login_required
def deleteTeacher(id):
    models.Teacher.delete(id)
    return redirect(url_for('views.viewteachers'))

@views.route('/edit_teacher/id=<id>', methods=['GET', 'POST'])
#@login_required
def edit_teacher(id):
    teacher = models.Teacher.getTeacher(id)
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dateofbirth']
        email = request.form['email']
        phno =  request.form['phno']
        address = request.form['address']
        experience = request.form['experience']
        doj = request.form['dateofjoining']
        models.Teacher.updateTeacher(id=teacher[0].id, name=name, gender=gender, dob=dob, email=email, phone=phno, address=address, experience=experience, doj=doj)
        return redirect(url_for("views.admin_home"))
    return render_template("edit_teacher.html", teacher = teacher[0])

@views.route('/add_course',methods=['GET', 'POST'])
#@login_required
def add_course():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        course = models.Course(id=id, name=name)
        course.create_Course()
        return redirect(url_for('views.admin_home'))
    return render_template("add_course.html")

@views.route('/viewcourse')
#@login_required
def viewcourse():
    courses = models.Course.getCourses()
    print(courses)
    return render_template("view_Courses.html", courses = courses)

@views.route('/edit_course/id=<id>', methods=['GET', 'POST'])
#@login_required
def edit_course(id):
    course = models.Course.getCourse(id)
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        models.Course.updateCourse(id=course.id,idn=id, name=name)
        return redirect(url_for("views.admin_home"))
    return render_template("edit_course.html", course = course)

@views.route('/deleteCourse/id=<id>')
#@login_required
def deleteCourse(id):
    models.Course.delete(id)
    return redirect(url_for('views.viewcourse'))

@views.route('/add_class', methods=['GET', 'POST'])
#@login_required
def add_class():
    teachers = models.Teacher.getTeachers()
    if request.method == 'POST':
        b_name = request.form['branchname']
        section = request.form['section']
        year = request.form['year']
        mentor = request.form['mentor']
        class_ = models.Class(branch_name=b_name, section=section, year=year, mentor=mentor)
        class_.create_Class()
        return redirect(url_for('views.admin_home'))
    return render_template("add_class.html",teachers=teachers)

@views.route('/viewclass')
#@login_required
def viewclass():
    classes = models.Class.getClasses()
    return render_template("viewclass.html", classes = classes)

@views.route('/edit_class/id=<id>', methods=['GET', 'POST'])
#@login_required
def edit_class(id):
    class_ = models.Class.getClass(id)
    teachers = models.Teacher.getTeachers()
    if request.method == 'POST':
        b_name = request.form['branchname']
        section = request.form['section']
        year = request.form['year']
        mentor = request.form['mentor']
        models.Class.updateClass(id=id, branch_name=b_name, section=section, year=year, mentor=mentor)
        return redirect(url_for("views.admin_home"))
    return render_template("edit_class.html", class_ = class_, teachers = teachers)

@views.route('/add_Stu_Clas/id=<id>', methods=['GET', 'POST'])
#@login_required
def add_Stu_Clas(id):
    students = models.Student.get_students()
    if request.method == 'POST':
        students = request.form.getlist('students')
        for student in students:
            models.Student.assignClass(id=student, class_id=id)
            return redirect(url_for('views.admin_home'))
    return render_template("add_Stu_Clas.html", students = students)

@views.route('/deleteClass/id=<id>')
#@login_required
def deleteClass(id):
    models.Class.delete(id)
    return redirect(url_for('views.viewclass'))

@views.route('/add_timetable')
def add_timetable():
    classes = models.Class.getClasses()
    courses = models.Course.getCourses()
    teachers = models.Teacher.getTeachers()
    return render_template("add_timetable.html",classes=classes, courses=courses, teachers=teachers)

@views.route('/add_events', methods=['GET', 'POST'])
#@login_required
def add_events():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        link = request.form['link']
        event = models.Events(name=name, date=date, description=description, link=link)
        event.create_Event()
        return redirect(url_for('views.admin_home'))
    return render_template("add_event.html")

@views.route('/viewevents')
#@login_required
def viewevents():
    events = models.Events.get_Events()
    return render_template("viewevents.html", events = events)

@views.route('/edit_event/id=<id>', methods=['GET', 'POST'])
#@login_required
def edit_event(id):
    event = models.Events.get_Event(id)
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        link = request.form['link']
        models.Events.updateEvent(id=id, name=name, date=date, description=description, link=link)
        return redirect(url_for("views.admin_home"))
    return render_template("edit_event.html", event = event)

@views.route('/deleteEvent/id=<id>')
#@login_required
def deleteEvent(id):
    models.Events.delete(id)
    return redirect(url_for('views.viewevents'))

@views.route('/createUser')
#@login_required
def createUser():
    students = models.Student.UnReg_stud()
    teachers = models.Teacher.UnReg_teach()

    return render_template("createUser.html", students = students, teachers = teachers)

@views.route('/addUser/id=<id>/role=<role>')
#@login_required
def addUser(id,role):
    user = models.User(id.lower(),id,role.upper())
    user.create_user()
    return redirect(url_for('views.createUser'))

@views.route('/viewUsers')
def viewUsers():
    users = models.User.getUsers()
    return render_template("viewUsers.html", users = users)

@views.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dateofbirth']
        email = request.form['email']
        phno =  request.form['phno']
        address = request.form['address']
        admin = models.Admin(id=id, name=name, gender=gender, dob=dob, email=email, phone=phno, address=address)
        admin.create_Admin()
        user = models.User(id.lower(), id, "ADMIN")
        user.create_user()
        return redirect(url_for('views.admin_home'))
    return render_template("add_admin.html")


@views.route('/admin_profile')
#@login_required
def admin_profile():
    user = models.Admin.get_Admin(current_user.id)
    print(user)
    return render_template("admin_profile.html",user=user)