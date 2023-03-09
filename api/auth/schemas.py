from flask_restx import fields
from ..auth import auth_namespace


# SIGN-UP SCHEMA MODEL
register_model = auth_namespace.model(
    name="Register Student/Teacher",
    model={
        "first_name": fields.String(required=True, description="First Name"),
        "last_name": fields.String(required=True, description="Last Name"),
        "gender": fields.String(required=True, description="Gender", enum=["MALE", "FEMALE"]),
        "email": fields.String(required=True, description="An Email"),
        # "password": fields.String(required=True, description="A Password"),
    },
)


# LOGIN SCHEMA MODEL
login_model = auth_namespace.model(
    name="Login User",
    model={
        "email": fields.String(required=True, description="An Email"),
        "password": fields.String(required=True, description="A Password"),
    },
)


# USER SCHEMA MODEL
user_model = auth_namespace.model(
    name="User Details",
    model={
        "id": fields.Integer(description="User ID"),
        "first_name": fields.String(description="First Name"),
        "last_name": fields.String(description="Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "matric_no": fields.String(description="Student Matric No."),
        "gpa": fields.Float(description="Student GPA"),
        "email": fields.String(description="Email"),
        "is_active": fields.Boolean(description="Is Active Flag"),
        "date_registered": fields.DateTime(description="Date Registered")
    },
)


# CHANGE PASSWORD SCHEMA
change_password_model = auth_namespace.model(
    name="Change Password",
    model={
        "old_password": fields.String(required=True, description="Old Password"),
        "new_password": fields.String(required=True, description="New Password"),
        "confirm_password": fields.String(required=True, description="Confirm New Password"),
    }
)
