from sqlalchemy import func
from ..utils import db
from ..utils.db_func import DB_Func
# from ..utils.calc_func import Record_Func
from datetime import datetime


class GradeScale(db.Model, DB_Func):
    __tablename__ = "gradescale"

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String, nullable=False)
    point = db.Column(db.Integer, default=0.00)
    min = db.Column(db.Integer, nullable=False)
    max = db.Column(db.Integer, nullable=False)

    created_by = db.Column(db.String()) 
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    modified_by = db.Column(db.String())
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return f"<Grade: {self.grade}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class StudentCourseScore(db.Model, DB_Func):
    __tablename__ = "student_courses_scores"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    matric_no = db.Column(db.String(12), unique=False, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    course_code = db.Column(db.String(6), unique=False, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    
    credit = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, default=0)
    grade = db.Column(db.String, nullable=True)
    grade_point = db.Column(db.Integer, default=0)
    scored_point = db.Column(db.Integer, default=0)

    registered_by = db.Column(db.String()) 
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())
    modified_by = db.Column(db.String())
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return f"<Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def get_student_course_id(self, student_id, course_id):
        student_course = self.query.filter(self.student_id==student_id, self.course_id==course_id).first()
        return student_course


class StudentRecord(db.Model, DB_Func):
    __tablename__ = "students_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    matric_no = db.Column(db.String(12), unique=False, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    
    course_count = db.Column(db.Integer, default=0)
    total_credits = db.Column(db.Integer, nullable=False, default=0)
    total_points = db.Column(db.Integer, default=0)
    gpa = db.Column(db.Integer, default=0)
    honours = db.Column(db.String, nullable=True)

    created_by = db.Column(db.String()) 
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    modified_by = db.Column(db.String())
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return f"<Student ID: {self.student_id}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
