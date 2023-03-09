from flask_restx import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, current_user
from ..teacher import teacher_namespace
from ..models import Teacher
from ..teacher.schemas import teacher_model
from ..teacher.schemas import teacher_model


@teacher_namespace.route("/")
class Teachers(Resource):
    
    # Create a Teacher
    @teacher_namespace.expect(teacher_model)
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(description="Teacher Creation")
    @jwt_required()
    def post(self):
        """
        Admin: Create a Teacher
        """
        if current_user.is_admin:
            data = teacher_namespace.payload

            title = data["title"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            gender = data["gender"]

            new_teacher = Teacher(
                title=title,
                first_name=first_name,
                last_name=last_name,
                gender=gender
            )

            new_teacher.save_to_db()
            
            return new_teacher, HTTPStatus.CREATED

    # Get All Teachers
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(description="Retrieve All Teachers")
    @jwt_required()
    def get(self):
        """
        Get All Teachers
        """
        if current_user.is_admin:
            teachers = Teacher.query.all()

            return teachers, HTTPStatus.OK
