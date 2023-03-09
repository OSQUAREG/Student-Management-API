# from enum import Enum
# from ..utils import db
# from ..utils.func import DB_Func
# from datetime import datetime


# class UserType(Enum):
#     ADMIN = "admin"
#     TEACHER = "teacher"
#     STUDENT = "student"


# class User(db.Model, DB_Func):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     password_hash = db.Column(db.String(), nullable=False)
#     is_active = db.Column(db.Boolean, default=True)
#     # type = db.Column(db.Enum(UserType), default=UserType.STUDENT)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     student = db.relationship("Student", backref="student_user", lazy=True)
    
#     teacher = db.relationship("Teacher", backref="teacher_user", lazy=True)

#     @classmethod
#     def get_user_by_code(cls, user_code):
#         return cls.query.get_or_404(user_code)


# class Student(db.Model, DB_Func):
#     __tablename__ = "students"

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), unique=False, nullable=False)
#     last_name = db.Column(db.String(50), unique=False, nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     uid = db.Column(db.String(12), unique=True)
#     date_registered = db.Column(db.DateTime, default=datetime.utcnow())

#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

#     courses = db.relationship("StudentCourse", backref="students")

#     def __repr__(self):
#         return f"<Student ID: {self.student_uid}>"

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)


# class Teacher(db.Model, DB_Func):
#     __tablename__ = "teachers"

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), unique=False, nullable=False)
#     last_name = db.Column(db.String(50), unique=False, nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     uid = db.Column(db.String(12), unique=True)
#     is_admin = db.Column(db.Boolean, default=False)
#     date_registered = db.Column(db.DateTime, default=datetime.utcnow)

#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

#     course = db.relationship("Course", backref="teacher", lazy=True)

#     def __repr__(self):
#         return f"<Teacher ID: {self.teacher_uid}>"

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)


# class Course(db.Model, DB_Func):
#     __tablename__ = "courses"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), unique=False, nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

#     students = db.relationship("StudentCourse", backref="courses")

#     def __repr__(self):
#         return f"<Course Name: {self.name}>"


# class StudentCourse(db.Model, DB_Func):
#     __tablename__ = "students_courses"

#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
#     course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
#     date_registered = db.Column(db.DateTime, default=datetime.utcnow)
