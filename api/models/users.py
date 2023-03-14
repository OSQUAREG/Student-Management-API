from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime
from enum import Enum

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

    def generate_username(self, id, first_name, last_name) -> None:
        self.username  = f"{first_name.lower()}.{last_name.lower()}{id}"
        self.update_db()


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

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.query.filter(cls.student_id==student_id).first()

    def generate_matric_no(self, student_id):
        year_str = str(datetime.utcnow().year)
        year_str = year_str[-3:]
        self.matric_no = f"STU/{year_str}/{student_id:04d}"
        self.update_db()


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

    @classmethod
    def get_by_teacher_id(cls, teacher_id):
        return cls.query.filter(cls.teacher_id==teacher_id).first()

    def generate_staff_code(self, teacher_id):
        year_str = str(datetime.utcnow().year)
        year_str = year_str[-3:]
        self.staff_code = f"TCH/{year_str}/{teacher_id:04d}"
        self.update_db()
