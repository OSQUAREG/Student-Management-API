from flask_restx import fields
from ..auth import auth_namespace


# SIGN-UP SCHEMA MODEL
register_model = auth_namespace.model(
    name="Create Admin",
    model={
        "user_type": fields.String(required=True, description="User Type"),
        "title": fields.String(
            required=True, 
            description="Title",
            enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"],
        ),
        "first_name": fields.String(required=True, description="First Name"),
        "last_name": fields.String(required=True, description="Last Name"),
        "gender": fields.String(
            required=True, description="Gender", enum=["MALE", "FEMALE"]
        ),
        "email": fields.String(required=True, description="An Email"),
        "department_id": fields.String(required=True, description="Department ID"),
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


# STUDENT/TEACHER SCHEMA
user_model = auth_namespace.model(
    name="Student/Teacher Details",
    model={
        "user_id": fields.Integer(description="User ID"),
        "title": fields.String(
            description="Title", enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"]
        ),
        "first_name": fields.String(description="First Name"),
        "last_name": fields.String(description="Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "username": fields.String(description="Username"),
        "email": fields.String(description="Email"),
        "type": fields.String(description="User Type"),
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(description="Student Matric No."),
        "teacher_id": fields.Integer(description="Teacher ID"),
        "staff_code": fields.String(description="Teacher's Staff Code"),
        "is_staff": fields.String(description="Is Staff Flag"),
        "is_active": fields.String(description="Is Active Flag"),
        "department_id": fields.String(description="Department ID"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    },
)

# CHANGE PASSWORD SCHEMA
change_password_model = auth_namespace.model(
    name="Change Password",
    model={
        "old_password": fields.String(required=True, description="Old Password"),
        "new_password": fields.String(required=True, description="New Password"),
        "confirm_password": fields.String(
            required=True, description="Confirm New Password"
        ),
    },
)
