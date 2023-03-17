from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user
from api.utils.calc_func import calc_scored_point, get_score_grade
from api.utils.query_func import check_course_code_exist, check_course_exist, check_student_exist, check_student_registered_course, get_all_courses, get_course_students, get_course_details_by_id, get_courses_students_by_id_list, get_student_course_detail_by_id, get_student_registered_course_by_id
from ..course.schemas import course_model, new_course_model, course_students_model, course_students_grades_model, update_multiple_course_students_scores_model
from ..course import course_namespace
from ..models import Course, StudentCourseScore
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
        Admin: Get All Students Offering Specific Course
        """
        if current_user.is_admin:
            if check_course_exist(course_id):
                course_students = get_course_students(course_id)
                return course_students, HTTPStatus.OK
            
            abort(HTTPStatus.NOT_FOUND, message="Course ID Not Found")

        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


"""GET-UPDATE STUDENTS GRADES FOR A COURSE (ADMIN ONLY)"""
@course_namespace.route("/grades/<int:course_id>/students", doc={"params": dict(course_id="Course ID")})
class GetUpdateCourseStudentsGrades(Resource):

    # GET ALL STUDENTS GRADES FOR A COURSE
    @course_namespace.marshal_with(course_students_grades_model)
    @course_namespace.doc(description="Retrieve All Student Grades for a Course (Admin Only)")
    @jwt_required()
    def get(self, course_id):
        """Admin: Get All Students Grades for a Specific Course"""
        if current_user.is_admin:
            if check_course_exist(course_id):
                course_students = get_course_students(course_id)
                return course_students, HTTPStatus.OK            
            abort(HTTPStatus.NOT_FOUND, message="Course ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    # UPDATE MULTIPLE STUDENTS GRADE FOR A COURSE
    @course_namespace.expect(update_multiple_course_students_scores_model)
    @course_namespace.marshal_with(course_students_grades_model)
    @course_namespace.doc(description="Update Multiple Students Grades for a Course (Admin Only)")
    @jwt_required()
    def patch(self, course_id):
        """Admin: Update Multiple Students Grades for a Course"""
        if current_user.is_admin:
            if check_course_exist(course_id):
                data = course_namespace.payload
                student_ids = []
                score_list = []
                for key in data.keys():
                    if key.startswith("student"):
                        student_ids.append(data[key])
                    if key.startswith("score"):
                        score_list.append(data[key])

                i = 0
                while i < len(student_ids):
                    if check_student_exist(student_ids[i]):
                        if check_student_registered_course(student_ids[i], course_id):
                            student_course = get_student_registered_course_by_id(student_ids[i], course_id)

                            student_course.score = score_list[i]
                            student_course.grade, student_course.grade_point = get_score_grade(student_ids[i], course_id, score_list[i])
                            student_course.scored_point = calc_scored_point(student_ids[i], course_id)
                            student_course.update_db()
                    i += 1
                # response data
                course_students = get_courses_students_by_id_list(student_ids, course_id)
                return course_students, HTTPStatus.OK
            abort(HTTPStatus.CONFLICT, message="Course does not exist.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")
