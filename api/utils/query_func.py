from sqlalchemy import func, text
from . import db
from ..models import Course, StudentCourse, Teacher


def get_courses():
    # query = text("SELECT * FROM courses")
    # courses = db.Query.from_statement(query)
    
    courses = (
        db.session.query(
            Course.id,
            Course.name,
            db.func.concat(
                Teacher.title, " ", Teacher.first_name, " ", Teacher.last_name
            ).label("teaher_name"),
            Course.date_created,
        )
        .outerjoin(Teacher, Teacher.id == Course.teacher_id)
        .order_by(Course.id)
        .all()
    )
    return courses


def get_student_courses(course_id):
    course_detail = (
        db.session.query(
            Course.name,
            func.concat(
                Teacher.title.name + " " + Teacher.first_name + " " + Teacher.last_name
            ).label("teaher_name"),
            StudentCourse.date_registered,
        )
        .outerjoin(Teacher.id == Course.teacher_id)
        .outerjoin(StudentCourse.course_id == Course.id)
        .filter_by(Course.id == course_id)
        .first()
    )
    pass


def get_student_course_count():
    pass


def get_course_students():
    pass
