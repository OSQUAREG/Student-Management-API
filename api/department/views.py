from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user
from ..models import Department
from api.utils.query_func import check_department_exist, get_all_departments
from ..department.schemas import department_model
from ..department import department_namespace
from http import HTTPStatus


@department_namespace.route("/")
# @department_namespace.doc(security='apikey')
class CreateGetDepartment(Resource):

    # CREATE NEW DEPARTMENT
    @department_namespace.expect(department_model)
    @department_namespace.marshal_with(department_model)
    @department_namespace.doc(description="Department Creation (Admin Only)")
    @jwt_required()
    def post(self):
        """
        Admin: Create New Department
        """        
        if current_user.is_admin:
            data = department_namespace.payload
            # check if department code already exist
            if check_department_exist(data["code"]):
                abort(HTTPStatus.CONFLICT, message="Department Code Already Exist")

            new_department = Department(
                name=data["name"],
                code=data["code"],
                created_by=current_user.username
            )

            new_department.save_to_db()            
            return new_department, HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    # GET ALL DEPARTMENTS
    @department_namespace.marshal_with(department_model)
    @department_namespace.doc(description="Retrieve All Department (Admin Only)")
    @jwt_required()
    def get(self):
        """
        Admin: Get All Departments
        """
        
        if current_user.is_admin:
            departments = get_all_departments()
            return departments, HTTPStatus.OK        
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


@department_namespace.route("/<int:department_id>")
class GetUpdateDelete(Resource):

    # GET A SPECIFIC DEPARTMENT
    @department_namespace.marshal_with(department_model)
    @department_namespace.doc(description="Retrieve Specific Department Details (Super Admin Only)")
    @jwt_required()
    def get(self, department_id):
        """Super Admin: Get Department by ID"""
        if current_user.is_admin:
            department = Department.get_by_id(department_id)
            return department, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


    @department_namespace.expect(department_model)
    @department_namespace.doc(description="Update Specific Department (Admin Only)")
    @jwt_required()
    def put(self, department_id):
        """Admin: Update Department Details by ID"""
        if current_user.is_admin:
            department = Department.get_by_id(department_id)
            data = department_namespace.payload
            
            department.name = data.get("name")
            department.code = data.get("code")

            department.update()
            return department, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    @department_namespace.doc(description="Delete Specific Department (Admin Only)")
    @jwt_required()
    def delete(self, department_id):
        """Super Admin: Delete Department by ID"""
        if current_user.is_admin and current_user.username == "super.admin":
            department = Department.get_by_id(department_id)
            department.delete()
            return {"message": "Department Deleted Successfully!"}, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Super Admin Only")