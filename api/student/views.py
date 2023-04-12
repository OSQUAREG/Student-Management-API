from flask import request
from ..student import (
    student_namespace, 
    adm_student_namespace, 
    student_courses_namespace, 
    student_grades_namespace, 
    student_records_namespace
)
from flask_restx import Resource, abort
from http import HTTPStatus
from flask_jwt_extended import current_user, jwt_required
from ..models import Student, StudentCourseScore, Course, StudentRecord, User
from ..student.schemas import (
    student_response_model,
    student_course_response_model,
    student_records_response_model,
    student_grades_response_model,
    update_student_model,
    update_student_course_score_model,
    register_multiple_student_courses_model,
    update_multiple_student_courses_scores_model,
)
from ..utils.query_func import (
    get_all_students_records,
    get_current_student,
    get_student_courses_by_id_or_code_list,
    get_student_courses_details,
    get_student_course_detail_by_id,
    get_student_records,
)


"""GET ALL STUDENTS"""
@student_namespace.route("/", doc=dict(description="Retrieve Current Student (Students Only)"))
@adm_student_namespace.route("/", doc=dict(description="Retrieve All Students (Admin Only)"))
class GetCurrentAllStudents(Resource):
    @adm_student_namespace.marshal_with(student_response_model)
    @jwt_required()
    def get(self):
        """Get All Students | Current Student"""
        if current_user.is_admin and current_user.is_active:
            students = Student.get_all()

            message = "All Students Retrieved Successfully"
            response = {"message": message, "data": students}            
            return response, HTTPStatus.OK
        
        elif current_user.type == "student" and current_user.is_active:
            current_student = get_current_student()
            
            message = "Current Student Retrieved Successfully"
            response = {"message": message, "data": current_student}
            return response, HTTPStatus.OK

        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")


"""GET-UPDATE-DELETE STUDENT DETAILS (Admins Only)"""
@adm_student_namespace.route("/<student_id_or_matric>", doc=dict(params=dict(student_id_or_matric="Student ID or Matric No")))
class GetUpdateDeleteSpecificStudent(Resource):

    # GET SPECIFIC STUDENT (by Student ID or Matric No)
    @adm_student_namespace.marshal_with(student_response_model)
    @adm_student_namespace.doc(description="Retrieve Specific Student (Admins Only)")
    @jwt_required()
    def get(self, student_id_or_matric):
        """Get Student by ID or Matric No"""
        if current_user.is_admin and current_user.is_active:
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:
                message = f"Student with Matric_no: {student.matric_no} Retrieved Successfully"
                response = {"message": message, "data": student}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Student Not Found. Please enter vlaid Id or Matric No.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

    # UPDATE SPECIFIC STUDENT (by Student ID or Matric No)
    @adm_student_namespace.expect(update_student_model)
    @adm_student_namespace.marshal_with(student_response_model)
    @adm_student_namespace.doc(description="Update Specific Student (Admins Only)")
    @jwt_required()
    def put(self, student_id_or_matric):
        """Update Any Student Detail by Id or Matric No."""
        if current_user.is_admin and current_user.is_active:
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:            
                data = adm_student_namespace.payload

                student.title = data.get("title") if data.get("title") else student.title
                student.first_name = data.get("first_name") if data.get("first_name") else student.first_name
                student.last_name = data.get("last_name") if data.get("last_name") else student.last_name
                # checks if email is provided and if new email provided already exists
                student.email = (student.email if not data.get("email") or data.get("email") == student.email 
                    else (data.get("email") if not User.check_email_exist(data.get("email")) 
                    else abort(HTTPStatus.CONFLICT, message="Email already exist.")))
                
                student.generate_username()
                student.modified_by = current_user.username
                student.update_db()
                
                message = f"Student with Matric_no: {student.matric_no} Updated Successfully"
                response = {"message": message, "data": student}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Student Not Found.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

    # DELETE SPECIFIC STUDENT (by Student ID or Matric No)
    @adm_student_namespace.doc(description="Delete Specific Student (Admins Only)")
    @jwt_required()
    def delete(self, student_id_or_matric):
        """Delete Student by ID or Matric No."""
        if current_user.is_admin and current_user.is_active:
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:            
                student.delete_from_db()
                return {"message": f"Student {student.matric_no} Deleted Successfully!"}, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Student Not Found.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")


"""STUDENT MULTIPLE COURSES REGISTRATION (ADMIN ONLY)"""
@student_courses_namespace.route("/<student_id_or_matric>", doc={"params": dict(student_id_or_matric="Student ID or Matric No.")})
class RegisterUnregisterStudentCourses(Resource):
    # REGISTER MULTIPLE COURSES FOR A STUDENT
    @student_courses_namespace.expect(register_multiple_student_courses_model)
    @student_courses_namespace.marshal_with(student_course_response_model)
    @student_courses_namespace.doc(description="Register Student Course (Admin Only)")
    @jwt_required()
    def post(self, student_id_or_matric):
        """Register Multiple Courses for a Student"""
        if current_user.is_admin and current_user.is_active:
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:                
                data = student_courses_namespace.payload
                
                course_ids_or_codes = []
                invalid_course_ids_or_codes = []
                regd_course_ids_or_codes = []
                
                i = 0
                while i < len(data):
                    i += 1
                    course = Course.get_by_course_id_or_code(data.get(f"course{i}"))
                    if course:
                        student_course_exist = StudentCourseScore.get_student_course_by_id_or_code(student.student_id, course.id)
                        if not student_course_exist:
                            course_ids_or_codes.append(data.get(f"course{i}"))

                            student_course = StudentCourseScore(
                                student_id=student.student_id,
                                matric_no=student.matric_no,
                                course_id=course.id,
                                course_code=course.code,
                                department_id=course.department_id,
                                credit=course.credit,
                                registered_by=current_user.username,
                            )
                            student_course.save_to_db()
                            
                            # update student records
                            stu_record = StudentRecord.get_by_student_id_or_matric(student.student_id)
                            stu_record.calc_course_count_credits()
                            stu_record.modified_by = current_user.username
                            stu_record.update_db()
                        else:
                            regd_course_ids_or_codes.append(data.get(f"course{i}"))                        
                    else:
                        invalid_course_ids_or_codes.append(data.get(f"course{i}"))

                # response data
                student_courses = get_student_courses_by_id_or_code_list(student.student_id, course_ids_or_codes)
                
                message = f"Courses: {course_ids_or_codes} Registered Successfully for Student {student.matric_no}. Courses: {regd_course_ids_or_codes} already registered for Student {student.matric_no}. Courses: {invalid_course_ids_or_codes} are invalid."
                
                response = {"message": message, "data": student_courses}                
                return response, HTTPStatus.CREATED
            abort(HTTPStatus.NOT_FOUND, message="Student Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")


    # UNREGISTER MULTIPLE COURSES FOR A STUDENT
    @student_courses_namespace.expect(register_multiple_student_courses_model)
    @student_courses_namespace.doc(description="Unregister Student Course (Admin Only)")
    @jwt_required()
    def delete(self, student_id_or_matric):
        """Unregister Multiple Courses for a Student"""
        if current_user.is_admin and current_user.is_active:
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:
                data = student_courses_namespace.payload
                course_ids_or_codes = []
                
                i = 0
                while i < len(data):
                    i += 1
                    course = Course.get_by_course_id_or_code(data.get(f"course{i}"))
                    student_course = StudentCourseScore.get_student_course_by_id_or_code(student.student_id, course.id)
                    if course and student_course:
                        course_ids_or_codes.append(data.get(f"course{i}"))
                        
                        student_course.delete_from_db()
                        # update student records
                        stu_record = StudentRecord.get_by_id(student.student_id)
                        stu_record.calc_course_count_credits()
                        stu_record.modified_by = current_user.username
                        stu_record.update_db()
                        
                return {"message": f"Courses: {course_ids_or_codes} unregistered successfully"}, HTTPStatus.OK            
            abort(HTTPStatus.NOT_FOUND, message="Student Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")


"""GET STUDENT REGISTERED COURSES (STUDENTS & ADMIN ONLY)"""
@student_namespace.route("/courses", 
    doc={"description": "Retrieve Student Registered Courses (Student Only)"})
@student_courses_namespace.route("/<student_id_or_matric>", 
    doc={"description": "Retrieve Student Registered Courses (Admin Only)", "params": dict(student_id_or_matric="Student ID or Matric No.")})
class GetStudentRegisteredCourses(Resource):
    @student_courses_namespace.marshal_with(student_course_response_model)
    @jwt_required()
    def get(self, student_id_or_matric=None):
        """Get Student Registered Courses"""
        if student_id_or_matric:
            if current_user.is_admin and current_user.is_active:
                student = Student.get_by_student_id_or_matric(student_id_or_matric)
                if student:
                    student_courses = get_student_courses_details(student.student_id)
                    
                    message = f"Student {student.matric_no} Courses Retrieved Successfully!"
                    response = {"message": message, "data": student_courses} 
                    return response, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Student Not Found")
            abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

        else:
            if current_user.type == "student" and current_user.is_active and get_current_student():
                student_courses = get_student_courses_details(current_user.student_id)

                message = f"Student {current_user.matric_no} Courses Retrieved Successfully!"
                response = {"message": message, "data": student_courses} 
                return response, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED, message="Students Only")


"""STUDENT SINGLE COURSE GRADE (ADMIN ONLY)"""
@student_grades_namespace.route("/student/<student_id_or_matric>/course/<course_id_or_code>", 
    doc={"params": dict(student_id_or_matric="Student Id or Matric No.", course_id_or_code="Course Id or Code")})
class GetUpdateSingleStudentCourseGrade(Resource):
    
    # UPDATE SINGLE STUDENT COURSE GRADE (ADMIN ONLY)
    @student_grades_namespace.expect(update_student_course_score_model)
    @student_grades_namespace.marshal_with(student_grades_response_model)
    @student_grades_namespace.doc(description="Student Course Grade Update (Admins Only).")
    @jwt_required()
    def patch(self, student_id_or_matric, course_id_or_code):
        """Update Student Grade for a Course"""
        if current_user.is_admin and current_user.is_active:
            # check if student and course exist
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if student and course:
                # check if student registered for the course
                student_course = StudentCourseScore.get_student_course_by_id_or_code(student.student_id, course.id)
                if student_course:
                    # get data
                    data = student_grades_namespace.payload                    
                    # update the student course score table
                    student_course.score = data.get("score")
                    student_course.calc_grade_scored_point(data.get("score"))
                    student_course.modified_by = current_user.username
                    student_course.update_db()                    
                    # updating the student records table
                    student_records = StudentRecord.get_by_student_id_or_matric(student.student_id)
                    student_records.calc_points_gpa_honours()
                    student_records.modified_by = current_user.username
                    student_records.update_db()
                    
                    # response data
                    student_course_detail = get_student_course_detail_by_id(student.student_id, course.id)
                    
                    message = f"Student {student_course.matric_no} Grade for Course {course.code} Updated Successfully!"
                    response = {"message": message, "data": student_course_detail} 
                    return response, HTTPStatus.OK
                    # return student_course_detail, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Course not registered for Student")
            abort(HTTPStatus.NOT_FOUND, message="Student or Course Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

    # GET STUDENT COURSE GRADE (ADMIN ONLY)
    @student_grades_namespace.marshal_with(student_grades_response_model)
    @student_grades_namespace.doc(description="Retrieve Student Course Grade (Admins Only)")
    @jwt_required()
    def get(self, student_id_or_matric, course_id_or_code):
        """Get Student Grade for a Course"""
        if current_user.is_admin:
            # check if student and course exist
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if student and course:
                # check if student course
                student_course = StudentCourseScore.get_student_course_by_id_or_code(student.student_id, course.id)
                if student_course:
                    message = f"Student {student_course.matric_no} Grade for Course {course.code} Retrieved Successfully!"
                    response = {"message": message, "data": student_course} 
                    return response, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Course not registered for Student")
            abort(HTTPStatus.NOT_FOUND, message="Student or Course Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")


"""GET-UPDATE MULTIPLE COURSE GRADES FOR A STUDENT (ADMIN ONLY)"""
@student_grades_namespace.route("/<student_id_or_matric>/courses", doc={"params": dict(student_id_or_matric="Student Id or Matric")})
class GetUpdateCourseStudentsGrades(Resource):

    # GET MULTIPLE COURSE GRADES FOR A STUDENT
    @student_grades_namespace.marshal_with(student_grades_response_model)
    @student_grades_namespace.doc(description="Retrieve All Courses Grades for a Student (Admin Only)")
    @jwt_required()
    def get(self, student_id_or_matric):
        """Get Multiple Course Grades for a Student"""
        if current_user.is_admin and current_user.is_active:
            # check if student and course exist
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:
                student_courses = get_student_courses_details(student.student_id)
                
                message = f"All Course Grades for Student {student.matric_no} Retrieved Successfully!"
                response = {"message": message, "data": student_courses} 
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, message="Student Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")

    # UPDATE MULTIPLE COURSE GRADES FOR A STUDENT
    @student_grades_namespace.expect(update_multiple_student_courses_scores_model)
    @student_grades_namespace.marshal_with(student_grades_response_model)
    @student_grades_namespace.doc(description="Update Multiple Course Grades for a Student (Admin Only)")
    @jwt_required()
    def patch(self, student_id_or_matric):
        """Update Multiple Course Grades for a Student"""
        if current_user.is_admin and current_user.is_active:
            student = Student.get_by_student_id_or_matric(student_id_or_matric)
            if student:
                data = student_grades_namespace.payload
                course_ids_or_codes = []
                valid_course_codes = []
                score_list = []
                for key in data.keys():
                    if key.startswith("course"):
                        course_ids_or_codes.append(data[key])
                    if key.startswith("score"):
                        score_list.append(data[key])

                i = 0
                while i < len(course_ids_or_codes):
                    # get and check for course
                    course = Course.get_by_course_id_or_code(course_ids_or_codes[i])
                    if course:
                        # add to valid course code list
                        valid_course_codes.append(course.code)
                        # check and get student course
                        student_course = StudentCourseScore.get_student_course_by_id_or_code(student.student_id, course.id)
                        if student_course:
                            student_course.score = score_list[i]
                            student_course.calc_grade_scored_point(score_list[i])
                            student_course.modified_by = current_user.username
                            student_course.update_db()
                    i += 1

                # updating the student records table
                student_records = StudentRecord.get_by_id(student.student_id)
                student_records.calc_points_gpa_honours()
                student_records.modified_by = current_user.username
                student_records.update_db()
                # response data
                student_courses = get_student_courses_by_id_or_code_list(student.student_id, valid_course_codes)
                
                message = f"Student {student.matric_no} Grades for Courses {valid_course_codes} Updated Successfully!"
                response = {"message": message, "data": student_courses} 
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, message="Student Not Found.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")


"""GET COURSE GRADES FOR A STUDENT (STUDENTS ONLY)"""
@student_namespace.route("/grades")
class GetCurrentStudentCoursesGrades(Resource):
    @student_namespace.marshal_with(student_grades_response_model)
    @student_namespace.doc(description="Retrieve Current Student Course Grades (Student Only)")
    @jwt_required()
    def get(self):
        """Get Course Grades for Current Student"""
        if current_user.type == "student" and current_user.is_active and get_current_student():
            student_grades = get_student_courses_details(current_user.student_id)

            message = f"Course Grades for Student {current_user.matric_no} Retrieved Successfully!"
            response = {"message": message, "data": student_grades} 
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Students Only")


"""GET STUDENT RECORDS (STUDENTS & ADMIN ONLY)"""
@student_namespace.route("/records", doc={"description": "Retrieve Current Student Records (Student Only)"})
@student_records_namespace.route("/<student_id_or_matric>",
    doc={"description": "Retrieve Specific Student Records (Admin Only)", "params": dict(student_id_or_matric="Student Id or Matric")})
class GetSpecificStudentRecords(Resource):
    @student_records_namespace.marshal_with(student_records_response_model)
    @jwt_required()
    def get(self, student_id_or_matric=None):
        """Get Specific Student Records"""
        if student_id_or_matric:
            if current_user.is_admin and current_user.is_active:
                student = Student.get_by_student_id_or_matric(student_id_or_matric)
                if student:
                    student_records = get_student_records(student.student_id)

                    message = f"Report for Student {student.matric_no} Retrieved Successfully!"
                    response = {"message": message, "data": student_records} 
                    return response, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, message="Please provide a Valid Student ID")
            abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

        else:
            if current_user.type == "student" and current_user.is_active and get_current_student():
                student_record = get_student_records(current_user.student_id)

                message = f"Report for Student {current_user.matric_no} Retrieved Successfully!"
                response = {"message": message, "data": student_record} 
                return response, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED, message="Students Only")


"""GET-UPDATE ALL STUDENTS RECORDS (ADMIN ONLY)"""
@student_records_namespace.route("/")
class GetUpdateAllStudentGradesRecords(Resource):
    @student_records_namespace.marshal_with(student_records_response_model)
    @student_records_namespace.doc(description="Retrieve All Students Records (Admin Only)")
    @jwt_required()
    def get(self):
        """Get All Student Records"""
        if current_user.is_admin and current_user.is_active:
            student_records = get_all_students_records()

            message = "All Student Reports Retrieved Successfully!"
            response = {"message": message, "data": student_records} 
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

    @student_records_namespace.marshal_with(student_records_response_model)
    @student_records_namespace.doc(description="Update All Students Records (Admin Only)")
    @jwt_required()
    def put(self):
        """Update All Student Grades & Records"""
        if current_user.is_admin and current_user.is_active:
            # update all student course grades and points
            student_courses = StudentCourseScore.query.all()
            for student_course in student_courses:
                # updating course details in student_courses_scores table
                course = Course.get_by_id(student_course.course_id)
                student_course.course_code = course.code
                student_course.credit
                # updating grade and points
                student_course.calc_grade_scored_point(student_course.score)
                student_course.modified_by = current_user.username
                student_course.update_db()

            # update all student records
            student_records = StudentRecord.query.all()
            for student_record in student_records:
                student_record.calc_points_gpa_honours()
                student_record.modified_by = current_user.username
                student_record.update_db()
            # respponse data
            student_records = get_all_students_records()
            message = "All Student Grades and Reports Updated Successfully!"
            response = {"message": message, "data": student_records} 
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")
        