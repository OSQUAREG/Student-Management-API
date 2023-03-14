from flask_restx import Resource, abort
from http import HTTPStatus
from flask_jwt_extended import jwt_required, current_user
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
