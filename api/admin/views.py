from flask_jwt_extended import current_user, jwt_required
from flask_restx import Resource, abort
from werkzeug.security import generate_password_hash
from ..admin import admin_namespace
from ..models import User
from ..admin.schemas import admin_model, new_admin_model
from http import HTTPStatus
from decouple import config


@admin_namespace.route("/")
class CreateGetAdmins(Resource):
    @admin_namespace.expect(new_admin_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description="Admin Creation (Admin Only)")
    @jwt_required()
    def post(self):
        """Admin: Create an Admin"""
        if current_user.is_admin:
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
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")


    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description="Retrieve ALl Admin (Admin Only)")
    @jwt_required()
    def get(self):
        """Admin: Get All Admins"""
        if current_user.is_admin:
            admins = User.query.filter_by(is_admin=True).all()
            return admins, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")


@admin_namespace.route("/<int:user_id>", doc=dict(params=dict(user_id="Admin User ID")))
class GetUpdateDeleteAdminByID(Resource):
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description="Retrieve Admin by ID")
    @jwt_required()
    def get(self, user_id):
        """Admin: Get Admin by ID"""
        if current_user.is_admin:
            admin = User.get_by_id(user_id)
            return admin, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")

    @admin_namespace.expect(admin_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description="Update Admin Info (Admin Only)")
    @jwt_required()
    def put(self, user_id):
        """Admin: Update Admin by ID"""
        if current_user.is_admin:
            admin = User.get_by_id(user_id)
            data = admin_namespace.payload

            admin.title=data.get("title")
            admin.first_name=data.get("first_name")
            admin.last_name=data.get("last_name")
            admin.email=data.get("email")

            admin.update()
            return admin, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")

    @admin_namespace.doc(description="Delete Admin (Super Admin Only)")
    @jwt_required()
    def delete(self, user_id):
        """Super Admin: Delete Admin by ID"""
        if current_user.is_admin and current_user.username == "super.admin":
            admin = User.get_by_id(user_id)
            admin.delete()
            return {"message": "Admin Deleted Successfully!"}
        abort(HTTPStatus.UNAUTHORIZED, "Super Admin Only")
