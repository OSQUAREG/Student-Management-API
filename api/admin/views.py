from flask_jwt_extended import current_user, jwt_required
from flask_restx import Resource, abort
from werkzeug.security import generate_password_hash
from api.models.users import Admins
from ..admin import admin_namespace
from ..models import User
from ..admin.schemas import admin_model, new_admin_model, admin_response_model
from http import HTTPStatus
from decouple import config


@admin_namespace.route("/")
class CreateGetAllAdmins(Resource):
    @admin_namespace.expect(new_admin_model)
    @admin_namespace.marshal_with(admin_response_model)
    @admin_namespace.doc(description="Admin Creation (Admin Only)")
    @jwt_required()
    def post(self):
        """Admin: Create an Admin"""
        if current_user.is_admin:
            data = admin_namespace.payload
            
            if User.check_email_exist(data["email"]):
                abort(HTTPStatus.CONFLICT, message="Email already exist.")
                
            # instantiate the User class
            new_admin = Admins(
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
            new_admin.save_to_db()
            new_admin.generate_username()
            new_admin.generate_admin_code()
            new_admin.modified_by = current_user.username
            new_admin.update_db()

            message = f"Admin: {new_admin.username} Created Successfully!"
            response = {"message": message, "data": new_admin} 
            return response, HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")


    @admin_namespace.marshal_with(admin_response_model)
    @admin_namespace.doc(description="Retrieve ALl Admin (Admin Only)")
    @jwt_required()
    def get(self):
        """Admin: Get All Admins"""
        if current_user.is_admin:
            admins = Admins.get_all()

            message = f"Admins Retrieved Successfully!"
            response = {"message": message, "data": admins} 
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")


@admin_namespace.route("/<int:admin_id_or_code>", doc=dict(params=dict(admin_id="Admin ID")))
class GetUpdateDeleteAdminByID(Resource):
    @admin_namespace.marshal_with(admin_response_model)
    @admin_namespace.doc(description="Retrieve Admin by ID")
    @jwt_required()
    def get(self, admin_id_or_code):
        """Admin: Get Admin by ID"""
        if current_user.is_admin:
            admin = Admins.get_by_admin_id_or_code(admin_id_or_code)
            if admin:

                message = f"Admin: {admin.username} Retrieved Successfully!"
                response = {"message": message, "data": admin} 
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Admin ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")

    @admin_namespace.expect(admin_model)
    @admin_namespace.marshal_with(admin_response_model)
    @admin_namespace.doc(description="Update Admin Info (Admin Only)")
    @jwt_required()
    def put(self, admin_id_or_code):
        """Admin: Update Admin by ID"""
        if current_user.is_admin:
            admin = Admins.get_by_admin_id_or_code(admin_id_or_code)
            data = admin_namespace.payload

            admin.title = data.get("title") if data.get("title") else admin.title
            admin.first_name = data.get("first_name") if data.get("first_name") else admin.first_name
            admin.last_name = data.get("last_name") if data.get("last_name") else admin.last_name
            # checks if email is provided and if new email provided already exists
            admin.email = (admin.email if not data.get("email") or data.get("email") == admin.email 
                else (data.get("email") if not User.check_email_exist(data.get("email")) 
                else abort(HTTPStatus.CONFLICT, message="Email already exist.")))
            
            admin.modified_by = current_user.username
            admin.generate_username()
            admin.generate_admin_code()
            admin.update_db()

            message = f"Admin: {admin.username} Updated Successfully!"
            response = {"message": message, "data": admin} 
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Admin Only")

    @admin_namespace.doc(description="Delete Admin (Super Admin Only)")
    @jwt_required()
    def delete(self, admin_id_or_code):
        """Super Admin: Delete Admin by ID"""
        if current_user.is_admin and current_user.username == "super.admin":
            admin = Admins.get_by_admin_id_or_code(admin_id_or_code)
            if not current_user == admin or not admin.username == "super.admin":
                admin.delete_from_db()
                return {"message": f"Admin {admin.username} Deleted Successfully!"}
            abort(HTTPStatus.CONFLICT, "Can't Perform Operation")
        abort(HTTPStatus.UNAUTHORIZED, "Super Admin Only")
