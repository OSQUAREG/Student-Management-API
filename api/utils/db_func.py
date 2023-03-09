from sqlalchemy import func
from datetime import datetime
from . import db
# from ..models import Course, StudentCourse, Teacher


# Database Functions
class DB_Func:
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

# function to generate student unique id
def generate_matric_no(new_user_id):
    year = datetime.utcnow().year
    return f"ST/{year}/{new_user_id:04d}"


# def get_courses():
#     course = (
#         db.session.query(
#             Course.id,
#             Course.name,
#             func.concat(
#                 Teacher.title.name + " " + Teacher.first_name + " " + Teacher.last_name
#             ).label("teaher_name"),
            
            
#         )
#         .outerjoin(Teacher.id == Course.teacher_id)
#         .order_by(Course.id)
#     )


# def get_student_courses(course_id):
#     course_detail = db.session.\
#                 query(Course.name, func.concat(
#                     Teacher.title.name + " " + Teacher.first_name + " " + Teacher.last_name).label("teaher_name"), StudentCourse.date_registered).\
#                     outerjoin(Teacher.id == Course.teacher_id).\
#                         outerjoin(StudentCourse.course_id == Course.id).\
#                             filter_by(Course.id == course_id).first()
#     pass


# def get_student_course_count():
#     pass


# def get_course_students():
#     pass

