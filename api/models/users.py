from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime
from enum import Enum
from flask_login import UserMixin

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class Title(Enum):
    PROF = "Prof"
    ENGR = "Engr"
    DR = "Dr"
    MR = "Mr"
    MRS = "Mrs"
    MS = "Ms"

class User(db.Model, DB_Func):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Enum(Title), nullable=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(),)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    
    created_by = db.Column(db.String()) 
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    modified_by = db.Column(db.String())
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow())
    
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }    
    # documentaiton: https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    
    def __repr__(self):
        return f"<User ID: {self.id}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_department_id(cls, department_id):
        return cls.query.filter_by(department_id=department_id).all()
    
    def generate_username(self) -> None:
        self.username = f"{self.first_name.lower()}.{self.last_name.lower()}{self.id}"

    @classmethod
    def check_email_exist(cls, email) -> bool:
        """Checks if email already exist in the users table"""
        email_exist = cls.query.filter_by(email=email).first()
        return True if email_exist else False


class Student(User):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    matric_no = db.Column(db.String(12), unique=True)

    student_courses = db.relationship("StudentCourseScore", backref="student", lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    def __repr__(self):
        return f"<Student Matric No.: {self.matric_no}>"

    def generate_matric_no(self):
        year_str = str(datetime.utcnow().year)
        year_str = year_str[-3:]
        self.matric_no = f"STU-{year_str}-{self.student_id:04d}"

    @classmethod
    def get_by_student_id_or_matric(cls, student_id_or_matric):
        student_w_id = cls.query.filter(cls.student_id==student_id_or_matric).first()
        student_w_matric = cls.query.filter(cls.matric_no==student_id_or_matric).first()
        student = student_w_id if student_w_id else student_w_matric
        return student


class Teacher(User):
    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    staff_code = db.Column(db.String(12), unique=True)

    teacher_courses = db.relationship("Course", backref="teacher", lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }

    def __repr__(self):
        return f"<Staff Code.: {self.staff_code}>"

    def generate_staff_code(self):
        year_str = str(datetime.utcnow().year)
        year_str = year_str[-3:]
        self.staff_code = f"TCH-{year_str}-{self.teacher_id:04d}"
        # self.update_db()

    @classmethod
    def get_by_teacher_id_or_code(cls, teacher_id_or_code):
        teacher_w_id = cls.query.filter(cls.teacher_id==teacher_id_or_code).first()
        teacher_w_code = cls.query.filter(cls.staff_code==teacher_id_or_code).first()
        teacher = teacher_w_id if teacher_w_id else teacher_w_code
        return teacher


class Admins(User, UserMixin): # using UserMixin in Flask-Login with Flask-Admin
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_code = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def __repr__(self):
        return f"<Admin Code.: {self.admin_code}>"

    def generate_admin_code(self):
        self.admin_code = f"ADM-{self.first_name.lower()}.{self.last_name.lower()}{self.admin_id}"

    @classmethod
    def get_by_admin_id_or_code(cls, admin_id_or_code):
        admin_w_id = cls.query.filter(cls.admin_id==admin_id_or_code).first()
        admin_w_code = cls.query.filter(cls.admin_code==admin_id_or_code).first()
        admin = admin_w_id if admin_w_id else admin_w_code
        return admin
