from flask_restx import fields
from ..teacher import teacher_namespace

# TEACHER COURSE SCHEMA
teacher_course_list = teacher_namespace.model(
    name="Teacher Course List",
    model={
        "name": fields.String(description="Course Name")
    }
)

# TEACHER SCHEMA
teacher_model = teacher_namespace.model(
    name="Teacher Details",
    model={
        "id": fields.Integer(description="Auto ID"),
        "title": fields.String(required=True, description="Title", enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"]),
        "first_name": fields.String(required=True, description="Teacher's First Name"),
        "last_name": fields.String(required=True, description="Teacher's Last Name"),
        "gender": fields.String(required=True, description="Gender", enum=["MALE", "FEMALE"]),
        "date_created": fields.DateTime(description="Date Created"),
        "courses": fields.Nested(teacher_course_list, description="Course List"),
    },
)


# UPDATE TEACHER SCHEMA
update_teacher_model = teacher_namespace.model(
    name="Update Teacher Details",
    model={
        "first_name": fields.String(description="Teacher's First Name"),
        "last_name": fields.String(description="Teacher's Last Name"),
        "email": fields.String(description="Teacher's Email"),
    },
)
