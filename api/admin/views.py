from flask_restx import Resource
from werkzeug.security import generate_password_hash
from ..admin import admin_namespace
from ..models import User
from ..admin.schemas import admin_model, admin_create_model
from http import HTTPStatus


@admin_namespace.route("/create")
class AdminRegister(Resource):
    @admin_namespace.expect(admin_create_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description="Admin Registration")
    def post(self):
        """
        Register an Admin
        """
        data = admin_namespace.payload

        first_name = data["first_name"]
        last_name = data["last_name"]
        gender = data["gender"]
        # matric_no = data["matric_no"]
        email = data["email"]
        password_hash = generate_password_hash(data["password"])

        # instantiate the User class
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            # matric_no=matric_no,
            email=email,
            password_hash=password_hash,
            is_admin=True
        )
        new_user.save_to_db()

        new_user.matric_no = f"{new_user.first_name}.{new_user.last_name}"
        new_user.update_db()

        return new_user, HTTPStatus.CREATED



