from flask_restx import fields
from ..course import course_namespace
from ..teacher.schemas import teacher_model


# CREATE COURSE SCHEMA MODEL
new_course_model = course_namespace.model(
    name="New Course Details",
    model={
        "code": fields.String(required=True, description="Course Code"),
        "name": fields.String(required=True, description="Course Name"),
        "credit": fields.Integer(required=True, description="Course Credit"),
        "department_id": fields.Integer(required=True, description="Department ID"),
        "teacher_id": fields.String(required=True, description="Teacher ID"),
    },
)


# COURSE SCHEMA MODEL
course_model = course_namespace.model(
    name="Course Details",
    model={
        "id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "course_credit": fields.String(description="Course Credit"),
        "department_name": fields.String(description="Department ID"),
        "gender": fields.String(description="Gender"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "teacher_id": fields.Integer(description="Teaacher ID"),
        "teacher": fields.String(description="Teacher Full Name"),
    },
)


# COURSE STUDENTS SCHEMA MODEL
course_students_model = course_namespace.model(
    name="Course Students",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(description="Matric No."),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "registered_on": fields.DateTime(description="Created Date"),
        "registered_by": fields.String(description="Creator's Username"),
    },
)
