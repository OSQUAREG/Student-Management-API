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
    users = db.relationship("User", backref="ur_department", lazy=True)
    students = db.relationship("Student", backref="st_department", lazy=True)
    teachers = db.relationship("Teacher", backref="sf_department", lazy=True)

    def __repr__(self):
        return f"<Department Name: {self.name}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


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
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
