from flask_restx import fields
from ..admin import admin_namespace


# TEACHER SCHEMA
admin_create_model = admin_namespace.model(
    name="Create Admin",
    model={
        "first_name": fields.String(required=True, description="First Name"),
        "last_name": fields.String(required=True, description="Last Name"),
        "gender": fields.String(
            required=True, description="Gender", enum=["MALE", "FEMALE"]
        ),
        # "matric_no": fields.String(required=True, description="Admin No"),
        "email": fields.String(required=True, description="An Email"),
        "password": fields.String(required=True, description="A Password"),
    },
)


# TEACHER SCHEMA
admin_model = admin_namespace.model(
    name="Admin Details",
    model={
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First Name"),
        "last_name": fields.String(description="Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "matric_no": fields.String(description="Admin No"),
        "email": fields.String(description="An Email"),
        "password_hash": fields.String(description="A Password"),
        "is_admin": fields.Boolean(description="Admin Flag"),
        "date_registered": fields.DateTime(description="Date Created"),
    },
)
