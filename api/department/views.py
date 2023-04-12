from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user

from api.utils.query_func import get_department_courses, get_department_students, get_department_teachers
from ..models import Department
from ..department.schemas import (
    department_model, 
    department_response_model, 
    department_students_response_model, 
    department_courses_response_model,
    department_teachers_response_model
)
from ..department import department_namespace
from http import HTTPStatus


@department_namespace.route("/")
class CreateGetDepartments(Resource):

    # CREATE NEW DEPARTMENT
    @department_namespace.expect(department_model)
    @department_namespace.marshal_with(department_response_model)
    @department_namespace.doc(description="Department Creation (Admins Only)")
    @jwt_required()
    def post(self):
        """
        Admin: Create New Department
        """        
        if current_user.is_admin:
            data = department_namespace.payload
            # check if department code already exist
            if Department.check_department_code_exist(data["code"]):
                abort(HTTPStatus.CONFLICT, message="Department Code Already Exist.")

            new_department = Department(
                name=data["name"],
                code=data["code"],
                created_by=current_user.username
            )
            new_department.save_to_db()
            
            message = f"Department: {new_department.name} Created Successfully"
            response = {"message": message, "data": new_department}
            return response, HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    # GET ALL DEPARTMENTS
    @department_namespace.marshal_with(department_response_model)
    @department_namespace.doc(description="Retrieve All Departments (Admins Only)")
    @jwt_required()
    def get(self):
        """
        Get All Departments
        """
        if current_user.is_admin:
            departments = Department.query.all()

            message = f"All Departments Retrieved Successfully"
            response = {"message": message, "data": departments}
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


@department_namespace.route("/<department_id_or_code>", doc=dict(params=dict(department_id_or_code="Department Id or Code")))
class GetUpdateDeleteDepartment(Resource):

    # GET A SPECIFIC DEPARTMENT
    @department_namespace.marshal_with(department_response_model)
    @department_namespace.doc(description="Retrieve Specific Department Details (Admins Only)")
    @jwt_required()
    def get(self, department_id_or_code):
        """Get Department by Id or Code"""
        if current_user.is_admin:
            department = Department.get_by_department_id_or_code(department_id_or_code)

            message = f"Department: {department.name}, Updated Successfully"
            response = {"message": message, "data": department}
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


    @department_namespace.expect(department_model)
    @department_namespace.marshal_with(department_response_model)
    @department_namespace.doc(description="Update Specific Department (Admins Only)")
    @jwt_required()
    def put(self, department_id_or_code):
        """Update Department Details by Id or Code"""
        if current_user.is_admin:
            department = Department.get_by_department_id_or_code(department_id_or_code)
            data = department_namespace.payload

            department.name = data.get("name") if data.get("name") else department.name
            # checks if code is provided and if new code provided already exists
            department.code = (department.code if not data.get("code") or data.get("code") == department.code 
                else (data.get("code") if not Department.check_department_code_exist(data.get("code")) 
                else abort(HTTPStatus.CONFLICT, message="Code already exist.")))
            department.modified_by = current_user.username
            department.update_db()
            
            message = f"Department: {department.name}, Updated Successfully"
            response = {"message": message, "data": department}
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    @department_namespace.doc(description="Delete Specific Department (Super Admin Only)")
    @jwt_required()
    def delete(self, department_id_or_code):
        """Super Admin: Delete Department by Id or Code"""
        if current_user.is_admin and current_user.username == "super.admin":
            department = Department.get_by_department_id_or_code(department_id_or_code)
            department.delete_from_db()
            
            return {"message": f"Department: {department.name} Deleted Successfully!"}, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Super Admin Only")


@department_namespace.route("/<department_id_or_code>/students")
class GetDepartmentStudents(Resource):
    @department_namespace.marshal_with(department_students_response_model)
    @department_namespace.doc(description="Retrieve Department Students (Admins Only)", 
                            params=dict(department_id_or_code="Department Id or Code"))
    @jwt_required()
    def get(self, department_id_or_code):
        """Get All Students in a Department"""
        if current_user.is_admin:
            department = Department.get_by_department_id_or_code(department_id_or_code)
            if department:
                deaprtment_students = get_department_students(department.id)

                message = f"Department: {department.code} Students Retrieved Successfully"
                response = {"message": message, "data": deaprtment_students}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Department Not Found")
        abort(HTTPStatus.OK, "Admins Only")


@department_namespace.route("/<department_id_or_code>/courses")
class GetDepartmentCourses(Resource):
    @department_namespace.marshal_with(department_courses_response_model)
    @department_namespace.doc(description="Retrieve Department Courses (Admins Only)", 
                            params=dict(department_id_or_code="Department Id or Code"))
    @jwt_required()
    def get(self, department_id_or_code):
        """Get All Courses in a Department"""
        if current_user.is_admin:
            department = Department.get_by_department_id_or_code(department_id_or_code)
            if department:
                deaprtment_courses = get_department_courses(department.id)

                message = f"Department: {department.code} Courses Retrieved Successfully"
                response = {"message": message, "data": deaprtment_courses}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Department Not Found")
        abort(HTTPStatus.OK, "Admins Only")


@department_namespace.route("/<department_id_or_code>/teachers")
class GetDepartmentTeachers(Resource):
    @department_namespace.marshal_with(department_teachers_response_model)
    @department_namespace.doc(description="Retrieve Department Courses (Admins Only)", 
                            params=dict(department_id_or_code="Department Id or Code"))
    @jwt_required()
    def get(self, department_id_or_code):
        """Get All Courses in a Department"""
        if current_user.is_admin:
            department = Department.get_by_department_id_or_code(department_id_or_code)
            if department:
                deaprtment_teachers = get_department_teachers(department.id)

                message = f"Department: {department.code} Teachers Retrieved Successfully"
                response = {"message": message, "data": deaprtment_teachers}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Department Not Found")
        abort(HTTPStatus.OK, "Admins Only")
