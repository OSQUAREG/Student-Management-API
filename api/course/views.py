from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user
from api.utils.query_func import check_course_code_exist, check_course_exist, get_all_courses, get_course_students, get_course_details_by_id
from ..course.schemas import course_model, new_course_model, course_students_model
from ..course import course_namespace
from ..models import Course
from http import HTTPStatus


@course_namespace.route("/")
class Courses(Resource):

    # CREATE A COURSE
    @course_namespace.expect(new_course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Course Creation (Admin Only)")
    @jwt_required()
    def post(self):
        """
        Admin: Create a Course
        """
        if current_user.is_admin:
            data = course_namespace.payload

            if check_course_code_exist(data["code"]):
                abort(HTTPStatus.CONFLICT, message="Course Code Already Exist")

            new_course = Course(
                name=data["name"],
                code=data["code"],
                credit=data["credit"],
                teacher_id=data["teacher_id"],
                department_id=data["department_id"],
                created_by=current_user.username,
            )

            new_course.save_to_db()
            new_course = get_course_details_by_id(new_course.id)

            return new_course, HTTPStatus.CREATED

        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    # GET ALL COURSES
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Retrieve All Courses (Admin Only)")
    @jwt_required()
    def get(self):
        """
        Admin: Get All Courses
        """
        if current_user.is_admin:
            courses = get_all_courses()
            return courses, HTTPStatus.OK
        
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


# GET ALL STUDENTS REGISTERED IN A COURSE
@course_namespace.route("/<int:course_id>/students")
class GetCourseStudents(Resource):
    @course_namespace.marshal_with(course_students_model)
    @course_namespace.doc(description="Retrieve Specific Course Students (Admin Only)")
    @jwt_required()
    def get(self, course_id):
        """
        Admin: Get All Students Offering Specific Courses
        """
        if current_user.is_admin:
            if check_course_exist(course_id):
                course_students = get_course_students(course_id)
                return course_students, HTTPStatus.OK
            
            abort(HTTPStatus.NOT_FOUND, message="Course ID Not Found")

        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")
