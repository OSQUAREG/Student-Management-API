from flask_restx import fields
from ..course import course_namespace
from ..teacher.schemas import teacher_model


# CREATE COURSE SCHEMA MODEL
create_course_model = course_namespace.model(
    name="Create Course Details",
    model={
        "name": fields.String(required=True, description="First Name"),
        "teacher_id": fields.String(required=True, description="Gender", enum=["MALE", "FEMALE"]),
    },
)



# COURSE STUDENTS SCHEMA MODEL
course_students_model = course_namespace.model(
    name="Course Students List",
    model={
        "matric_no": fields.String(description="First Name"),
        "first_name": fields.String(description="First Name"),
        "last_name": fields.String(description="Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
    },
)



# COURSE SCHEMA MODEL
course_model = course_namespace.model(
    name="Course Details",
    model={
        "id": fields.Integer(description="Auto ID"),
        "name": fields.String(description="First Name"),
        "date_created": fields.String(description="Last Name"),
        "teacher": fields.Nested(model=teacher_model, description="Teacher Details"),
        "students": fields.Nested(model=course_students_model, description="Students List"),
    },
)

