from flask_restx import Resource
from werkzeug.security import generate_password_hash
from ..admin import admin_namespace
from ..models import User
from ..admin.schemas import admin_model, new_admin_model
from http import HTTPStatus
from decouple import config


@admin_namespace.route("/create")
class AdminRegister(Resource):
    @admin_namespace.expect(new_admin_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description="Admin Registration")
    def post(self):
        """
        Register an Admin
        """
        data = admin_namespace.payload

        # instantiate the User class
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            gender=data["gender"],
            email=data["email"],
            password_hash=generate_password_hash(config("DEFAULT_ADMIN_PASSWORD")),
            department_id = 1,
            is_admin=True,
            is_staff=True,
            created_by="admin"
        )
        new_user.save_to_db()

        new_user.generate_username(new_user.id, new_user.first_name, new_user.last_name)

        return new_user, HTTPStatus.CREATED



