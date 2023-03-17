from ..student import student_namespace
from flask_restx import Resource, abort
from sqlalchemy import and_, desc, asc, func
from http import HTTPStatus
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity
from ..models import Student, StudentCourseScore, Course, StudentRecord
from ..student.schemas import (
    student_model,
    update_student_model,
    student_course_model,
    student_records_model,
    update_student_course_score_model,
    student_grades_model,
    register_multiple_student_courses_model,
    student_courses_grades_model,
    update_multiple_student_courses_scores_model
)
from ..utils.query_func import (
    check_course_exist,
    check_student_registered_course,
    check_student_exist,
    get_all_students,
    get_all_students_records,
    get_student_courses_by_id_list,
    get_student_courses_details,
    get_student_course_detail_by_id,
    get_student_registered_course_by_id,
    get_student_records,
    check_email_exist,
)
from ..utils.calc_func import (
    calc_course_count,
    calc_total_credits,
    get_score_grade,
    calc_scored_point,
    calc_total_points,
    calc_student_gpa_honours,
)
from ..utils import db


"""GET ALL STUDENTS"""
@student_namespace.route("/")
class Students(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Retrieve All Students (Admin Only) or Current Student (Students Only)")
    @jwt_required()
    def get(self):
        """
        Get All Students (Admin Only) | Current Student (Student Only)
        """
        if current_user.is_admin:
            students = get_all_students()
            return students, HTTPStatus.OK
        elif current_user.type == "student":
            student = Student.query.filter_by(username=get_jwt_identity()).first()
            student = Student.get_by_student_id(student.student_id)
            return student, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")


"""GET-UPDATE-DELETE STUDENT DETAILS"""
@student_namespace.route("/<int:student_id>", doc=dict(params=dict(student_id="Student ID")))
class GetUpdateDeleteSpecificStudent(Resource):

    # GET SPECIFIC STUDENT (by Student ID)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Retrieve Specific Student by ID (Admin Only)")
    @jwt_required()
    def get(self, student_id):
        """
        Admin: Get Student by ID
        """
        if current_user.is_admin:
            student = Student.get_by_student_id(student_id)
            return student, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

    # UPDATE SPECIFIC STUDENT (by Student ID)
    @student_namespace.expect(update_student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Update Specific Student (Admin Only)")
    @jwt_required()
    def put(self, student_id):
        """
        Admin: Update Any or All 3 Student Detail by ID
        """
        if current_user.is_admin:
            student = Student.get_by_student_id(student_id)
            data = student_namespace.payload
            # check if first name is provided
            if data.get("first_name"):
                student.first_name = data.get("first_name")
            else:
                student.first_name = student.first_name
            # check if last name is provided
            if data.get("last_name"):
                student.last_name = data.get("last_name")
            else:
                student.last_name = student.last_name
            # check if email is provided
            if data.get("email") and student.email != data.get("email"):
                if not check_email_exist(data.get("email")):
                    student.email = data.get("email")
                else:
                    abort(HTTPStatus.CONFLICT, message="Email already exist.")
            else:
                student.email = student.email
            student.update_db()
            return student, HTTPStatus.OK

        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

    # DELETE SPECIFIC STUDENT (by Student ID)
    @student_namespace.doc(description="Delete Specific Student (Admin Only)")
    @jwt_required()
    def delete(self, student_id):
        """
        Admin: Delete Student by ID
        """
        if current_user.is_admin:
            student = Student.get_by_student_id(student_id)
            student.delete_from_db()
            return {"message": "Student Deleted Successfully!"}, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")


"""STUDENT MULTIPLE COURSES REGISTRATION (ADMIN ONLY)"""
@student_namespace.route("/<int:student_id>/courses")
class RegisterUnregisterStudentCourses(Resource):
    # REGISTER MULTIPLE COURSES FOR A STUDENT
    @student_namespace.expect(register_multiple_student_courses_model)
    @student_namespace.marshal_with(student_course_model)
    @student_namespace.doc(description="Register Student Course (Admin Only)", params=dict(student_id="Student ID"))
    @jwt_required()
    def post(self, student_id):
        """
        Admin: Register Multiple Courses for a Student
        """
        if current_user.is_admin:
            if check_student_exist(student_id):
                student = Student.get_by_student_id(student_id)
                data = student_namespace.payload
                course_ids = []
                i = 0
                while i < len(data):
                    i += 1                    
                    if check_course_exist(data.get(f"course{i}")) and not check_student_registered_course(student_id, data.get(f"course{i}")):
                        course_id = data.get(f"course{i}")
                        course_ids.append(course_id)
                        
                        course = Course.get_by_id(course_id)
                        student_course = StudentCourseScore(
                            student_id=student_id,
                            matric_no=student.matric_no,
                            course_id=course_id,
                            course_code=course.code,
                            department_id=course.department_id,
                            credit=course.credit,
                            registered_by=current_user.username,
                        )
                        student_course.save_to_db()
                        
                        # update student records
                        stu_record = StudentRecord.get_by_id(student_id)
                        stu_record.course_count = calc_course_count(student_id)
                        stu_record.total_credits = calc_total_credits(student_id)
                        stu_record.update_db()
                # response data
                student_courses = get_student_courses_by_id_list(student_id, course_ids)
                return student_courses, HTTPStatus.CREATED


    # UNREGISTER MULTIPLE COURSES FOR A STUDENT
    @student_namespace.expect(register_multiple_student_courses_model)
    @student_namespace.doc(description="Unregister Student Course (Admin Only)", params=dict(student_id="Student ID"))
    @jwt_required()
    def delete(self, student_id):
        """Admin: Unregister Multiple Courses for a Student"""
        if current_user.is_admin:
            if check_student_exist(student_id):
                student = Student.get_by_student_id(student_id)
                data = student_namespace.payload
                course_ids = []
                i = 0
                while i < len(data):
                    i += 1                    
                    if check_course_exist(data.get(f"course{i}")) and check_student_registered_course(student_id, data.get(f"course{i}")):
                        course_id = data.get(f"course{i}")
                        course_ids.append(course_id)
                        
                        student_course = get_student_registered_course_by_id(student_id, course_id)
                        student_course.delete_from_db()
                        # update student records
                        stu_record = StudentRecord.get_by_id(student_id)
                        stu_record.course_count = calc_course_count(student_id)
                        stu_record.total_credits = calc_total_credits(student_id)
                        stu_record.update_db()
                return {"message": "Courses unregistered successfully"}, HTTPStatus.OK
            
            abort(HTTPStatus.CONFLICT, message=f"Student with {student_id} does not exist")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")


"""GET STUDENT REGISTERED COURSES (STUDENTS & ADMIN ONLY)"""
@student_namespace.route("/courses/student", doc={"description": "Retrieve Student Registered Courses (Student Only Route)", "envelop": "Testing"})
@student_namespace.route("/courses/<int:student_id>", 
    doc={"description": "Retrieve Student Registered Courses (Admin Only Route)", "params": {"student_id": "Student ID"}})
class StudentCourses(Resource):
    @student_namespace.marshal_with(student_course_model)
    @jwt_required()
    def get(self, student_id=None):
        """Get Student's Registered Courses"""
        if student_id:
            if current_user.is_admin:
                if check_student_exist(student_id):
                    student_courses = get_student_courses_details(student_id)
                    return student_courses, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Please provide a Valid Student ID")
            abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

        else:
            if current_user.type == "student":
                student = Student.query.filter_by(username=current_user.username).first()
                student_courses = get_student_courses_details(student.student_id)
                return student_courses, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED, message="Student Only")


"""STUDENT COURSE GRADE (ADMIN ONLY)"""
@student_namespace.route("/grades/<int:student_id>/course/<int:course_id>")
class GetUpdateStudentCourseGrade(Resource):
    
    # UPDATE STUDENT COURSE GRADE (ADMIN ONLY)
    @student_namespace.expect(update_student_course_score_model)
    @student_namespace.marshal_with(student_grades_model)
    @student_namespace.doc(description="Student Course Score/Grade Update", params=dict(student_id="Student ID", course_id="Course ID"))
    @jwt_required()
    def patch(self, student_id, course_id):
        """Admin: Update Student Course Score/Grade"""
        if current_user.is_admin:
            student_course = get_student_registered_course_by_id(student_id, course_id)
            # check if student and course exist
            if check_student_exist(student_id) and check_course_exist(course_id):
                # check if student registered for the course
                if student_course:
                    data = student_namespace.payload

                    # updating the student course score table
                    student_course.score = data["score"]
                    student_course.grade, student_course.grade_point = get_score_grade(student_id, course_id, data["score"])
                    student_course.scored_point = calc_scored_point(student_id, course_id)
                    student_course.update_db()
                    
                    # updating the student records table
                    student_records = StudentRecord.get_by_id(student_id)
                    student_records.total_points = calc_total_points(student_id)
                    student_records.gpa, student_records.honours = calc_student_gpa_honours(student_id)
                    student_records.update_db()
                    
                    # response data
                    student_course_detail = get_student_course_detail_by_id(student_id, course_id)
                    return student_course_detail, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Course not registered for Student")
            abort(HTTPStatus.NOT_FOUND, message="Student ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

    # GET STUDENT COURSE GRADE (ADMIN ONLY)
    @student_namespace.marshal_with(student_grades_model)
    @student_namespace.doc(description="Retrieve Student Course Score/Grade (Admin Only)", params=dict(student_id="Student ID", course_id="Course ID"))
    @jwt_required()
    def get(self, student_id, course_id):
        """Admin: Get Student Grade for a Course"""
        if current_user.is_admin:
            if check_student_exist(student_id) and check_course_exist(course_id):
                student_courses = get_student_course_detail_by_id(student_id, course_id)
                return student_courses, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, message="Please provide a Valid Student ID")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


"""GET-UPDATE COURSES GRADES FOR A STUDENT (ADMIN ONLY)"""
@student_namespace.route("/grades/<int:student_id>/courses", doc={"params": dict(course_id="Course ID")})
class GetUpdateCourseStudentsGrades(Resource):

    # GET ALL EGISTERED COURSES GRADES FOR A STUDENT
    @student_namespace.marshal_with(student_courses_grades_model)
    @student_namespace.doc(description="Retrieve All Courses Grades for a Student (Admin Only)")
    @jwt_required()
    def get(self, student_id):
        """Admin: Get All Course Grades for a Specific Student"""
        if current_user.is_admin:
            if check_student_exist(student_id):
                student_courses = get_student_courses_details(student_id)
                return student_courses, HTTPStatus.OK            
            abort(HTTPStatus.NOT_FOUND, message="Student ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")

    # UPDATE MULTIPLE REGISTERED COURSES GRADES FOR A STUDENT
    @student_namespace.expect(update_multiple_student_courses_scores_model)
    @student_namespace.marshal_with(student_courses_grades_model)
    @student_namespace.doc(description="Update Multiple Courses Grades for a Student (Admin Only)")
    @jwt_required()
    def patch(self, student_id):
        """Admin: Update Multiple Courses Grades for a Student"""
        if current_user.is_admin:
            if check_student_exist(student_id):
                data = student_namespace.payload
                course_ids = []
                score_list = []
                for key in data.keys():
                    if key.startswith("course"):
                        course_ids.append(data[key])
                    if key.startswith("score"):
                        score_list.append(data[key])

                i = 0
                while i < len(course_ids):
                    if check_course_exist(course_ids[i]):
                        if check_student_registered_course(student_id, course_ids[i]):
                            student_course = get_student_registered_course_by_id(student_id, course_ids[i])

                            student_course.score = score_list[i]
                            student_course.grade, student_course.grade_point = get_score_grade(student_id, course_ids[i], score_list[i])
                            student_course.scored_point = calc_scored_point(student_id, course_ids[i])
                            student_course.update_db()
                    i += 1
                # response data
                course_students = get_student_courses_by_id_list(student_id, course_ids)
                return course_students, HTTPStatus.OK
            abort(HTTPStatus.CONFLICT, message="Student does not exist.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


"""GET STUDENT ALL GRADES (STUDENTS & ADMIN ONLY)"""
@student_namespace.route("/grades/student", doc={"description": "Retrieve Student Grades (Student Only)"})
@student_namespace.route("/grades/<int:student_id>",
    doc={"description": "Retrieve Student Grades for Registered Courses (Admin Only)", "params": {"student_id": "Student ID"}})
class StudentCourseGrades(Resource):
    @student_namespace.marshal_with(student_grades_model)
    @jwt_required()
    def get(self, student_id=None):
        """Get Student Grades for Registered Courses"""
        if student_id:
            if current_user.is_admin:
                if check_student_exist(student_id):
                    student_grades = get_student_courses_details(student_id)
                    return student_grades, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Please provide a Valid Student ID")
            abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

        else:
            if current_user.type == "student":
                student = Student.query.filter_by(username=current_user.username).first()
                student_grades = get_student_courses_details(student.student_id)
                return student_grades, HTTPStatus.CREATED
            abort(HTTPStatus.UNAUTHORIZED, message="Student Only")


"""GET STUDENT RECORDS (STUDENTS & ADMIN ONLY)"""
@student_namespace.route("/records/student", doc={"description": "Retrieve Student Records (Student Only)"})
@student_namespace.route("/records/<int:student_id>",
    doc={"description": "Retrieve Student Records (Admin Only)", "params": {"student_id": "Student ID"}})
@student_namespace.route("/records", doc={"description": "Retrieve All Students Records (Admin Only)"})
class GetStudentRecords(Resource):
    @student_namespace.marshal_with(student_records_model)
    @jwt_required()
    def get(self, student_id=None):
        """Get Student Records"""
        if student_id:
            if current_user.is_admin:
                if check_student_exist(student_id):
                    student_records = get_student_records(student_id)
                    return student_records, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Please provide a Valid Student ID")
            abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

        else:
            if current_user.type == "student":
                student = Student.query.filter_by(username=current_user.username).first()
                student_records = get_student_records(student.student_id)
                return student_records, HTTPStatus.CREATED
            abort(HTTPStatus.UNAUTHORIZED, message="Student Only")


"""GET ALL STUDENTS RECORDS (ADMIN ONLY)"""
@student_namespace.route("/records")
class GetStudentRecords(Resource):
    @student_namespace.marshal_with(student_records_model)
    @student_namespace.doc(description="Retrieve All Students Records (Admin Only)")
    @jwt_required()
    def get(self):
        """Get All Students Records"""
        if current_user.is_admin:
            students_records = get_all_students_records()
            return students_records, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")
        