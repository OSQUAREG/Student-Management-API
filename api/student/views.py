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
    score_model,
    student_grades_model,
    register_multiple_course_model
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
@student_namespace.route("/<int:student_id>")
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
        Admin: Update Student by ID
        """
        if current_user.is_admin:
            data = student_namespace.payload            
            if not check_email_exist(data["email"]):
                abort(HTTPStatus.CONFLICT, message="Email already exist.")
                
            student = Student.get_by_student_id(student_id)
            student.first_name = data["first_name"]
            student.last_name = data["last_name"]
            student.email = data["email"]        
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



# """STUDENT COURSE REGISTRATION (ADMIN ONLY)"""
# @student_namespace.route("/register/course/<int:course_id>/student/<int:student_id>")
# class RegisterStudentCourse(Resource):

#     # REGISTER A COURSE FOR A STUDENT
#     @student_namespace.marshal_with(student_course_model)
#     @student_namespace.doc(description="Register Student Course (Admin Only)", params=dict(student_id="Student ID", course_id="Course ID"))
#     @jwt_required()
#     def post(self, student_id, course_id):
#         """
#         Admin: Register a Course by ID for a Student
#         """
#         if current_user.is_admin:
#             student = Student.get_by_student_id(student_id)
#             course = Course.get_by_id(course_id)
            
#             if check_student_exist(student_id):
#                 if check_course_exist(course_id):
#                     if check_student_registered_course(student_id, course_id):
#                         abort(HTTPStatus.CONFLICT, message="Course already registered for Student")
#                     # instantiate the StudentCourse class
#                     student_course = StudentCourseScore(
#                         student_id=student_id,
#                         matric_no=student.matric_no,
#                         course_id=course_id,
#                         course_code=course.code,
#                         department_id=course.department_id,
#                         credit=course.credit,
#                         registered_by=current_user.username,
#                     )
#                     student_course.save_to_db()
#                     # update student records
#                     stu_record = StudentRecord.get_by_id(student_id)
#                     stu_record.course_count = calc_course_count(student_id)
#                     stu_record.total_credits = calc_total_credits(student_id)
#                     stu_record.update_db()
#                     # response data
#                     student_course = get_student_course_detail_by_id(student_id, course_id)
#                     return student_course, HTTPStatus.CREATED
                
#                 abort(HTTPStatus.CONFLICT, message=f"Course with {course_id} does not exist")
#             abort(HTTPStatus.CONFLICT, message=f"Student with {student_id} does not exist")
#         abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

#     # UNREGISTER A COURSE FOR A STUDENT
#     @student_namespace.doc(description="Unregister Student Course (Admin Only)")
#     @jwt_required()
#     def delete(self, student_id, course_id):
#         """
#         Admin: Unregister a Course by ID for a Student
#         """
#         if current_user.is_admin:
#             student = Student.get_by_student_id(student_id)
#             course = Course.get_by_id(course_id)
            
#             if check_student_exist(student_id):
#                 if check_course_exist(course_id):
#                     if check_student_registered_course(student_id, course_id):
#                         student_course = get_student_registered_course_by_id(student_id, course_id)
#                         student_course.delete_from_db()
#                         # update student records
#                         stu_record = StudentRecord.get_by_id(student_id)
#                         stu_record.course_count = calc_course_count(student_id)
#                         stu_record.total_credit = calc_total_credits(student_id)
#                         stu_record.update_db()
#                         # response data
#                         student_course = get_student_course_detail_by_id(student.id, course.id)
#                         return {"message": f"Student Course: {course.code} Unregistered Successfully"}, HTTPStatus.OK

#                     abort(HTTPStatus.CONFLICT, message="Course Not Registered for Student")
#                 abort(HTTPStatus.CONFLICT, message=f"Course with {course_id} does not exist")
#             abort(HTTPStatus.CONFLICT, message=f"Student with {student_id} does not exist")
#         abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")


"""STUDENT MULTIPLE COURSES REGISTRATION (ADMIN ONLY)"""
@student_namespace.route("/register/courses/<int:student_id>")
class StudentRegisterCourses(Resource):
    # REGISTER MULTIPLE COURSES FOR A STUDENT
    @student_namespace.expect(register_multiple_course_model)
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
                if check_course_exist(data.get("course1")) and not check_student_registered_course(student_id, data.get("course1")):
                    course_ids.append(data["course1"])
                if check_course_exist(data.get("course2")) and not check_student_registered_course(student_id, data.get("course2")):
                    course_ids.append(data["course2"])
                if check_course_exist(data.get("course3")) and not check_student_registered_course(student_id, data.get("course3")):
                    course_ids.append(data["course3"])
                if check_course_exist(data.get("course4")) and not check_student_registered_course(student_id, data.get("course4")):
                    course_ids.append(data["course4"])
                if check_course_exist(data.get("course5")) and not check_student_registered_course(student_id, data.get("course5")):
                    course_ids.append(data["course5"])

                if len(course_ids) <= 5 and len(course_ids) >= 1:
                    for course_id in course_ids:
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
                elif len(course_ids) == 0:
                    abort(HTTPStatus.CONFLICT, message="Courses are already registered for Student")
                else:                
                    abort(HTTPStatus.CONFLICT, message="You can only register not more than 5 Courses at once")
            abort(HTTPStatus.CONFLICT, message=f"Student with {student_id} does not exist")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")


    # UNREGISTER MULTIPLE COURSES FOR A STUDENT
    @student_namespace.expect(register_multiple_course_model)
    @student_namespace.doc(description="Unregister Student Course (Admin Only)", params=dict(student_id="Student ID"))
    @jwt_required()
    def delete(self, student_id):
        """Admin: Register Multiple Courses for a Student"""
        if current_user.is_admin:
            if check_student_exist(student_id):
                data = student_namespace.payload
                course_ids = []
                if check_course_exist(data.get("course1")) and check_student_registered_course(student_id, data.get("course1")):
                    course_ids.append(data["course1"])
                if check_course_exist(data.get("course2")) and check_student_registered_course(student_id, data.get("course2")):
                    course_ids.append(data["course2"])
                if check_course_exist(data.get("course3")) and check_student_registered_course(student_id, data.get("course3")):
                    course_ids.append(data["course3"])
                if check_course_exist(data.get("course4")) and check_student_registered_course(student_id, data.get("course4")):
                    course_ids.append(data["course4"])
                if check_course_exist(data.get("course5")) and check_student_registered_course(student_id, data.get("course5")):
                    course_ids.append(data["course5"])

                for course_id in course_ids:
                    student_course = get_student_registered_course_by_id(student_id, course_id)
                    student_course.delete_from_db()
                    # update student records
                    stu_record = StudentRecord.get_by_id(student_id)
                    stu_record.course_count = calc_course_count(student_id)
                    stu_record.total_credit = calc_total_credits(student_id)
                    stu_record.update_db()
                return {"message": "Courses unregistered successfully"}, HTTPStatus.OK
            
            abort(HTTPStatus.CONFLICT, message=f"Student with {student_id} does not exist")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")


"""GET STUDENT REGISTERED COURSES (STUDENTS & ADMIN ONLY)"""
@student_namespace.route("/courses/student", doc={"description": "Retrieve Student Registered Courses (Student Only Route)"})
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
                return student_courses, HTTPStatus.CREATED
            abort(HTTPStatus.UNAUTHORIZED, message="Student Only")


"""STUDENT COURSE GRADE (ADMIN ONLY)"""
@student_namespace.route("/grades/<int:student_id>/course/<int:course_id>")
class StudentCourseScoreGrade(Resource):
    
    # UPDATE STUDENT COURSE GRADE (ADMIN ONLY)
    @student_namespace.expect(score_model)
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
            abort(HTTPStatus.UNAUTHORIZED, message="Admin Only.")

    # GET STUDENT COURSE GRADE (ADMIN ONLY)
    @student_namespace.marshal_with(student_grades_model)
    @jwt_required()
    def get(self, student_id, course_id):
        """Get Student Grade for a Registered Course"""
        if current_user.is_admin:
            if check_student_exist(student_id) and check_course_exist(course_id):
                student_courses = get_student_course_detail_by_id(student_id, course_id)
                return student_courses, HTTPStatus.CREATED
            abort(HTTPStatus.NOT_FOUND, message="Please provide a Valid Student ID")
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
        