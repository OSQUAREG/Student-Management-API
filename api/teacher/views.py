from flask_restx import Resource, abort
from http import HTTPStatus
from flask_jwt_extended import jwt_required, current_user
from api.utils.query_func import (
    get_teacher_courses, 
    get_teacher_students, 
    get_current_teacher, 
    get_teacher_students_grades
)
from ..models import Teacher, Course, User
from ..teacher import teacher_namespace, adm_teacher_namespace
from ..teacher.schemas import (
    teacher_model, 
    teacher_response_model, 
    teacher_students_response_model, 
    teacher_courses_response_model,
    teacher_students_grades_response_model
)


# GET ALL TEACHERS
@teacher_namespace.route("/", doc=dict(description="Retrieve Current Teacher (Teachers Only)"))
@adm_teacher_namespace.route("/", doc=dict(description="Retrieve All Teachers (Students Only)"))
class GetCurrentAllTeachers(Resource):
    @adm_teacher_namespace.marshal_with(teacher_response_model)
    @jwt_required()
    def get(self):
        """
        Get All Teachers | Current Teacher
        """
        if current_user.is_admin and current_user.is_active:
            teachers = Teacher.get_all()

            message = f"All Teachers Retrieved Successfully"
            response = {"message": message, "data": teachers}
            return response, HTTPStatus.OK

        elif current_user.type == "teacher" and current_user.is_active:
            current_teacher = get_current_teacher()
            
            message = "Current Teacher Retrieved Successfully"
            response = {"message": message, "data": current_teacher}
            return response, HTTPStatus.OK

        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


""""GET-UPDATE-DELETE TEACHER"""
@adm_teacher_namespace.route("/<teacher_id_or_code>", doc=dict(params=dict(teacher_id_or_code="Teacher Id or Code")))
class GetUpdateDeleteTeacher(Resource):

    # GET TEACHER BY ID
    @adm_teacher_namespace.marshal_with(teacher_response_model)
    @adm_teacher_namespace.doc(description="Retrieve Specific Teacher Details (Admin Only)")
    @jwt_required()
    def get(self, teacher_id_or_code):
        """Get Teacher by Id or Code"""
        if current_user.is_admin and current_user.is_active:
            teacher = Teacher.get_by_teacher_id_or_code(teacher_id_or_code)

            message = f"Teacher: {teacher.staff_code} Retrieved Successfully"
            response = {"message": message, "data": teacher}
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")

    @adm_teacher_namespace.expect(teacher_model)
    @adm_teacher_namespace.marshal_with(teacher_response_model)
    @adm_teacher_namespace.doc(description="Update Specific Teacher Details (Admin Only)")
    @jwt_required()
    def put(self, teacher_id_or_code):
        """Update Teacher by Id of Code"""
        if current_user.is_admin and current_user.is_active:
            teacher = Teacher.get_by_teacher_id_or_code(teacher_id_or_code)
            if teacher:
                data = adm_teacher_namespace.payload
                
                teacher.title = data.get("title") if data.get("title") else teacher.title
                teacher.first_name = data.get("first_name") if data.get("first_name") else teacher.first_name
                teacher.last_name = data.get("last_name") if data.get("last_name") else teacher.last_name
                # checks if email is provided and if new email provided already exists
                teacher.email = (teacher.email if not data.get("email") or data.get("email") == teacher.email 
                    else (data.get("email") if not User.check_email_exist(data.get("email")) 
                    else abort(HTTPStatus.CONFLICT, message="Email already exist.")))
                
                teacher.generate_username()
                teacher.modified_by = current_user.username
                teacher.update_db()
                
                message = f"Teacher: {teacher.staff_code} Updated Successfully"
                response = {"message": message, "data": teacher}
                return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")

    @adm_teacher_namespace.doc(description="Delete Specific Teacher (Admin Only)")
    @jwt_required()
    def delete(self, teacher_id_or_code):
        """Delete Teacher by Id or Code"""
        if current_user.is_admin and current_user.is_active:
            teacher = Teacher.get_by_teacher_id_or_code(teacher_id_or_code)
            teacher.delete_from_db()
            return {"message": f"Teacher {teacher.staff_code} Deleted Successfully!"}, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")


"""TEACHER STUDENTS"""
@teacher_namespace.route("/students", doc=dict(description="Retrieve Teacher Students (Teacher Only)"))
@adm_teacher_namespace.route("/<teacher_id_or_code>/students", doc=dict(description="Retrieve Teacher Students (Admin Only)", params=dict(teacher_id_or_code="Teacher Id or Code")))
class GetTeacherStudents(Resource):
    @teacher_namespace.marshal_with(teacher_students_response_model)
    @teacher_namespace.doc()
    @jwt_required()
    def get(self, teacher_id_or_code=None):
        """Get Teacher Students"""
        if current_user.is_admin and current_user.is_active:
            teacher = Teacher.get_by_teacher_id_or_code(teacher_id_or_code)
            if teacher:
                teacher_students = get_teacher_students(teacher.teacher_id)

                message = f"Teacher Courses: {teacher.staff_code} Retrieved Successfully"
                response = {"message": message, "data": teacher_students}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Teacher Not Found. Input Valid Id or Code")
        else:
            if current_user.type == "teacher" and current_user.is_active and get_current_teacher():
                teacher_students = get_teacher_students(current_user.teacher_id)
                
                message = f"Teacher Courses: {current_user.staff_code} Retrieved Successfully"
                response = {"message": message, "data": teacher_students}
                return response, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED, "Teachers Only")
        abort(HTTPStatus.UNAUTHORIZED, "Admins Only")


"""TEACHER COURSES"""
@teacher_namespace.route("/courses", doc=dict(description="Retrieve Teacher Courses (Teachers Only)"))
@adm_teacher_namespace.route("/<teacher_id_or_code>/courses", doc=dict(description="Retrieve Teacher Courses (Admins Only)", params=dict(teacher_id_or_code="Teacher Id or Code")))
class GetTeacherCourses(Resource):
    @teacher_namespace.marshal_with(teacher_courses_response_model)
    @jwt_required()
    def get(self, teacher_id_or_code=None):
        """Get Teacher Students"""
        if current_user.is_admin:
            teacher = Teacher.get_by_teacher_id_or_code(teacher_id_or_code)
            if teacher:
                teacher_courses = get_teacher_courses(teacher.teacher_id)

                message = f"Teacher Courses: {teacher.staff_code} Retrieved Successfully"
                response = {"message": message, "data": teacher_courses}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Teacher Not Found. Input Valid Id or Code")
        else:
            if current_user.type == "teacher" and current_user.is_active and get_current_teacher():
                teacher_courses = get_teacher_courses(current_user.teacher_id)

                message = f"Teacher Courses: {current_user.staff_code} Retrieved Successfully"
                response = {"message": message, "data": teacher_courses}
                return response, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED, "Teachers Only")
        abort(HTTPStatus.UNAUTHORIZED, "Admins Only")


"""TEACHER STUDENTS GRADES"""
@teacher_namespace.route("/students/grades/<course_id_or_code>", doc=dict(description="Retrieve Teacher Courses (Teachers Only)", params=dict(course_id_or_code="Course Id or Code")))
@adm_teacher_namespace.route("/<teacher_id_or_code>/students/grades/<course_id_or_code>", 
                            doc=dict(description="Retrieve Teacher Courses (Admins Only)", 
                            params=dict(teacher_id_or_code="Teacher Id or Code", course_id_or_code="Course Id or Code")))
class GetTeacherStudentsGrades(Resource):
    @teacher_namespace.marshal_with(teacher_students_grades_response_model)
    @jwt_required()
    def get(self, course_id_or_code, teacher_id_or_code=None):
        """Get Teacher Students Grades"""
        if teacher_id_or_code:
            if current_user.is_admin and current_user.is_active:
                teacher = Teacher.get_by_teacher_id_or_code(teacher_id_or_code)
                course = Course.get_by_course_id_or_code(course_id_or_code)
                if teacher and course and teacher.teacher_id == course.teacher_id:                    
                    teacher_students_grades = get_teacher_students_grades(teacher.teacher_id, course.id)

                    message = f"Teacher: {teacher.staff_code} Students Grades for Course: {course.code} Retrieved Successfully"
                    response = {"message": message, "data": teacher_students_grades}
                    return response, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, "Teacher/Course Not Found. Input Valid Ids or Codes")
            abort(HTTPStatus.UNAUTHORIZED, "Admins Only")
        else:
            if current_user.type == "teacher" and current_user.is_active and get_current_teacher():
                course = Course.get_by_course_id_or_code(course_id_or_code)
                if course and current_user.teacher_id == course.teacher_id:
                    teacher_students_grades = get_teacher_students_grades(current_user.teacher_id, course.id)

                    message = f"Teacher: {current_user.staff_code} Students Grades for Course: {course.code} Retrieved Successfully"
                    response = {"message": message, "data": teacher_students_grades}
                    return response, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, "Course Not Found. Input Valid Ids or Codes")
            abort(HTTPStatus.UNAUTHORIZED, "Teachers Only")