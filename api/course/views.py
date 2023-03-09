from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user

from api.utils.query_func import get_courses
from ..course.schemas import course_model, create_course_model
from ..course import course_namespace
from ..models import Course, StudentCourse
from http import HTTPStatus


@course_namespace.route("/")
class Courses(Resource):
    
    # Create a Course
    @course_namespace.expect(create_course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Course Creation (Admin Only)")
    @jwt_required()
    def post(self):
        """
        Admin: Create a Course
        """
        if current_user.is_admin:
            data = course_namespace.payload

            name = data["name"]
            teacher_id = data["teacher_id"]

            new_course = Course(name=name, teacher_id=teacher_id)
            new_course.save_to_db()
            
            return new_course, HTTPStatus.CREATED

    # Get ALl Courses
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Retrieve All Courses (Admin Only)")
    @jwt_required()
    def get(self):
        """
        Admin: Get All Courses
        """
        # if current_user.is_admin:
        # courses = Course.query.all()
        courses = get_courses()
        
        return courses, HTTPStatus.OK


@course_namespace.route("/course/<int:course_id>/students")
class GetAllCourseStudents(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Retrieve Specific Course Students")
    @jwt_required()
    def get(self):
        """
        Get All Students Offering Specific Courses
        """
        pass

