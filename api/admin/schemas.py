from flask_restx import fields
from ..admin import admin_namespace


# ADMIN SCHEMA
new_admin_model = admin_namespace.model(
    name="New Admin",
    model={
        "first_name": fields.String(required=True, description="First Name"),
        "last_name": fields.String(required=True, description="Last Name"),
        "gender": fields.String(
            required=True, description="Gender", enum=["MALE", "FEMALE"]
        ),
        "email": fields.String(required=True, description="An Email"),
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
        "username": fields.String(description="Admin Username"),
        "email": fields.String(description="An Email"),
        "admin_code": fields.String(description="Admin Code"),
        "is_admin": fields.Boolean(description="Admin Flag"),
        "is_staff": fields.Boolean(description="Staff Flag"),
        "created_by": fields.String(description="Created By"),
        "created_on": fields.DateTime(description="Date Created"),
    },
)

admin_response_model = admin_namespace.model(
    name="Admin Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(admin_model, description="Response Data")
    }
)

