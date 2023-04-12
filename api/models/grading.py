from sqlalchemy import func, or_
from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime
from ..models import Course


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
    def get_courses_by_student_id_or_matric(cls, student_id_or_matric):
        """Gets All Courses Offered by a Specific Student"""
        student_courses = cls.query.filter(
            or_(cls.student_id==student_id_or_matric, cls.matric_no==student_id_or_matric)
            ).all()
        return student_courses

    @classmethod
    def get_students_by_course_id_or_code(cls, course_id_or_code):
        """Gets All Students Offering a Specific Course"""
        course_students = cls.query.filter(
            or_(cls.course_id==course_id_or_code, cls.course_code==course_id_or_code)
            ).all()
        return course_students
    
    @classmethod
    def get_student_course_by_id_or_code(cls, student_id_or_matric, course_id_or_code):
        """Gets a Specific Course Offered by a Specific Student"""
        student_course = cls.query.filter(
            or_(cls.student_id==student_id_or_matric, cls.matric_no==student_id_or_matric), 
            or_(cls.course_id==course_id_or_code, cls.course_code==course_id_or_code)
            ).first()
        return student_course

    def calc_grade_scored_point(self, score):
        """Calculates and Returns the Grade, Grade Point and Scored Point for a Student Course"""
        grade_point = (
            db.session.query(
                GradeScale.grade,
                GradeScale.point,
                (StudentCourseScore.credit * GradeScale.point).label("scored_point"),
            )
            .join(StudentCourseScore, StudentCourseScore.score >= GradeScale.min)
            .filter(
                StudentCourseScore.student_id == self.student_id,
                StudentCourseScore.course_id == self.course_id,
                GradeScale.min <= score,
                GradeScale.max >= score,
            )
            .first()
        )        
        self.grade, self.grade_point, self.scored_point = grade_point.grade, grade_point.point, grade_point.scored_point

class StudentRecord(db.Model, DB_Func):
    __tablename__ = "students_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    matric_no = db.Column(db.String(12), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    
    course_count = db.Column(db.Integer, default=0)
    total_credits = db.Column(db.Integer, default=0)
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
    def get_by_student_id_or_matric(cls, student_id_or_matric):
        """Gets a Specific Student Records by Id"""
        return cls.query.filter(
            or_(cls.student_id==student_id_or_matric, cls.matric_no==student_id_or_matric)
            ).first()

    def calc_course_count_credits(self):
        """Calculates and Returns the Count of Courses Offered by Specific Students and the Total Credits of the Courses"""
        student_course = (
            db.session.query(
                (func.count(StudentCourseScore.course_id)).label("course_count"), 
                (func.sum(StudentCourseScore.credit)).label("total_credits")
            )
            .filter(StudentCourseScore.student_id == self.student_id)
            .first()
        )
        self.course_count, self.total_credits = student_course.course_count, student_course.total_credits

    def calc_points_gpa_honours(self):
        """
        Calculates and Returns the Total Points, GPA and Honours scored by Specific Student.
        Notes:
        the GPA is mutiplied by 100 when saving it to the database,
        and divided by 100 when retrieving it from the database.
        """
        records = (
            db.session.query(
                (func.sum(StudentCourseScore.scored_point)).label("total_points"),
                (((func.sum(StudentCourseScore.scored_point)) / StudentRecord.total_credits) * 100).label("gpa")
            )
            .outerjoin(StudentCourseScore, StudentCourseScore.student_id == StudentRecord.student_id)
            .filter(StudentRecord.student_id == self.student_id)
            .first()
        )

        gpa = int(records.gpa) if records.gpa is not None else None        
        total_points = records.total_points
        honours = None

        honours = ("First Class Honours" if gpa and gpa / 100 >= 3.5
            else "Second Class Honours (Upper Division)" if gpa and gpa / 100 >= 3.0 and gpa / 100 <= 3.49
            else "Second Class Honours (Lower Division)" if gpa and gpa / 100 >= 2.0 and gpa / 100 <= 2.99
            else "Third Class Honours" if gpa and gpa / 100 >= 1.0 and gpa / 100 <= 1.99
            else "No Honours/Degree") if gpa else 0

        self.total_points, self.gpa, self.honours = total_points, gpa, honours
