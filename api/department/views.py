from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user
from ..models import Department
from api.utils.query_func import check_department_exist, get_all_departments
from ..department.schemas import department_model
from ..department import department_namespace
from http import HTTPStatus


@department_namespace.route("/")
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
        from ..models import Department
        
        if current_user.is_admin:
            departments = get_all_departments()
            return departments, HTTPStatus.OK
        
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")