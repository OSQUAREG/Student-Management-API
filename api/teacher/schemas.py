from flask_restx import fields
from ..teacher import teacher_namespace


# TEACHER SCHEMA
teacher_model = teacher_namespace.model(
    name="Teacher Details",
    model={
        "teacher_id": fields.Integer(description="Teacher ID"),
        "user_id": fields.Integer(description="User ID"),
        "title": fields.String(description="Title", enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"]),
        "first_name": fields.String(description="Teacher's First Name"),
        "last_name": fields.String(description="Teacher's Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "username": fields.String(description="Username"),
        "email": fields.String(description="An Email"),
        "staff_code": fields.String(description="Teacher's Staff Code"),
        "is_staff": fields.String(description="Is Staff Flag"),
        "type": fields.String(description="User Type"),
        "department_id": fields.String(description="Department ID"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    },
)
