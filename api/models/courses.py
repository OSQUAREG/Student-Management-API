from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime


class Department(db.Model, DB_Func):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    
    created_by = db.Column(db.String()) 
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    modified_by = db.Column(db.String())
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow())
    
    courses = db.relationship("Course", backref="co_department", lazy=True)
    users = db.relationship("User", backref="user_department", lazy=True)

    def __repr__(self):
        return f"<{self.name}>"

    @classmethod
    def get_by_department_id_or_code(cls, department_id_or_code):
        department_w_id = cls.query.filter(cls.id==department_id_or_code).first()
        department_w_code = cls.query.filter(cls.code==department_id_or_code).first()
        department = department_w_id if department_w_id else department_w_code
        return department

    @classmethod
    def check_department_code_exist(code) -> bool:
        """"Checks if code already exist in departments table"""
        code_exist = Department.query.filter_by(code=code).first()
        return True if code_exist else False


class Course(db.Model, DB_Func):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id"))

    created_by = db.Column(db.String()) 
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    modified_by = db.Column(db.String())
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow())
    
    course_students = db.relationship("StudentCourseScore", backref="course", lazy=True)

    def __repr__(self):
        return f"<Course Name: {self.name}>"

    @classmethod
    def get_by_course_id_or_code(cls, course_id_or_code):
        course_w_id = cls.query.filter(cls.id==course_id_or_code).first()
        course_w_code = cls.query.filter(cls.code==course_id_or_code).first()
        course = course_w_id if course_w_id else course_w_code
        return course

    @classmethod
    def get_by_department_id(cls, department_id):
        return cls.query.filter_by(department_id=department_id).all()

    @classmethod
    def get_one_by_teacher_id(cls, teacher_id):
        return cls.query.filter_by(teacher_id=teacher_id).first()

    @classmethod
    def get_all_by_teacher_id(cls, teacher_id):
        return cls.query.filter_by(teacher_id=teacher_id).all()

    @classmethod
    def check_course_code_exist(code) -> bool:
        """Checks if code already exist in courses table"""
        code_exist = Course.query.filter_by(code=code).first()
        return True if code_exist else False