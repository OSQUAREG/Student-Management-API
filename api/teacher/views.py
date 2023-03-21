from flask_restx import Resource, abort
from http import HTTPStatus
from flask_jwt_extended import jwt_required, current_user
from ..models import Teacher
from api.utils.query_func import get_all_teachers
from ..teacher import teacher_namespace
from ..teacher.schemas import teacher_model


# GET ALL TEACHERS
@teacher_namespace.route("/")
class Teachers(Resource):
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(description="Retrieve All Teachers")
    @jwt_required()
    def get(self):
        """
        Get All Teachers
        """
        if current_user.is_admin:
            teachers = get_all_teachers()
            return teachers, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


@teacher_namespace.route("/<int:teacher_id>")
class GetUpdateDeleteTeacher(Resource):

    # GET TEACHER BY ID
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(description="Retrieve Specific Teacher Details (Admin Only)")
    @jwt_required()
    def get(self, teacher_id):
        """Admin: Get Teacher by ID"""
        if current_user.is_admin:
            teacher = Teacher.get_by_teacher_id(teacher_id)
            return teacher, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    @teacher_namespace.expect(teacher_model)
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(description="Update Specific Teacher Details (Admin Only)")
    @jwt_required()
    def put(self, teacher_id):
        """Admin: Update Teacher by ID"""
        if current_user.is_admin:
            teacher = Teacher.get_by_teacher_id(teacher_id)
            data = teacher_namespace.payload
            
            teacher.title = data.get("title")
            teacher.first_name = data.get("first_name")
            teacher.last_name = data.get("last_name")
            teacher.email = data.get("email")
            