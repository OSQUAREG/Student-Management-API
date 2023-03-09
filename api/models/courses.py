from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime


class Course(db.Model, DB_Func):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    students = db.relationship("StudentCourse", backref="courses", lazy=True)

    def __repr__(self):
        return f"<Course Name: {self.name}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class StudentCourse(db.Model, DB_Func):
    __tablename__ = "student_courses"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    score = db.Column(db.Float(precision=2, asdecimal=True), default=0.00)
    grade = db.Column(db.Float(precision=1, asdecimal=True), default=0.0)    
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Student ID: {self.student_id}, Course ID: {self.course_id}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
