from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user
from api.models.grading import StudentRecord
from api.models.users import Student
# from api.utils.calc_func import calc_scored_point, get_score_grade
from api.utils.query_func import (
    get_all_courses, get_course_students, 
    get_course_details_by_id_or_code, 
    get_course_students_by_id_or_matric_list, 
    get_course_details_by_id_or_code,
)
from ..course.schemas import (
    new_course_model,
    course_response_model,
    course_students_response_model, 
    course_students_grades_response_model, 
    update_course_model,
    update_multiple_course_students_scores_model
)
from ..course import course_namespace, course_student_namespace
from ..models import Course, StudentCourseScore, Department, Teacher
from http import HTTPStatus


"""CREATE-GET ALL COURSES"""
@course_namespace.route("/")
class CreateGetAllCourses(Resource):

    # CREATE A NEW COURSE
    @course_namespace.expect(new_course_model)
    @course_namespace.marshal_with(course_response_model)
    @course_namespace.doc(description="New Course Creation (Admin Only)")
    @jwt_required()
    def post(self):
        """
        Create a New Course
        """
        if current_user.is_admin:
            data = course_namespace.payload
            # check if course code already exist
            if Course.check_course_code_exist(data["code"]):
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
            new_course = get_course_details_by_id_or_code(new_course.id)

            message = f"New Course: {new_course.course_name}, with code: {new_course.course_code}, Created Successfully"
            response = {"message": message, "data": new_course}
            return response, HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")

    # GET ALL COURSES
    @course_namespace.marshal_with(course_response_model)
    @course_namespace.doc(description="Retrieve All Courses (Admin Only)")
    @jwt_required()
    def get(self):
        """
        Get All Courses
        """
        if current_user.is_admin:
            courses = get_all_courses()
            
            message = f"All Courses Retrieved Successfully"
            response = {"message": message, "data": courses}
            return response, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")



"""GET-UPDATE-DELETE COURSE BY ID OR CODE"""
@course_namespace.route("/<course_id_or_code>", doc={"params": dict(course_id_or_code="Course Id or Code")})
class GetUpdateDeleteCourse(Resource):

    # GET A COURSE
    @course_namespace.marshal_with(course_response_model)
    @course_namespace.doc(description="Retrieve Specific Course (Admins Only)")
    @jwt_required()
    def get(self, course_id_or_code):
        if current_user.is_admin:
            course = get_course_details_by_id_or_code(course_id_or_code)
            if course:
                message = f"Course: {course.course_code} Retrieved Successfully"
                response = {"message": message, "data": course}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Course Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only") 


    # UPDATE SPECIFIC COURSE (by ID or Code)
    @course_namespace.expect(update_course_model)
    @course_namespace.marshal_with(course_response_model)
    @course_namespace.doc(description="Update Specific Course (Admins Only)")
    @jwt_required()
    def put(self, course_id_or_code):
        """Update Any Course Detail by Id or Code"""
        if current_user.is_admin:
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if course:
                data = course_namespace.payload
                # check department and teacher id or code provided
                department = Department.get_by_department_id_or_code(data.get("department"))
                teacher = Teacher.get_by_teacher_id_or_code(data.get("teacher"))

                course.name = data.get("name") if data.get("name") else course.name
                course.credit = data.get("credit") if data.get("credit") else course.credit
                course.department_id = department.id if data.get("department") and department else course.department_id
                course.teacher_id = teacher.teacher_id if data.get("teacher") and teacher else course.teacher_id
                # checks if code is provided and if new code provided already exists
                course.code = (course.code if not data.get("code") or data.get("code") == course.code 
                    else (data.get("code") if not Course.check_course_code_exist(data.get("code")) 
                    else abort(HTTPStatus.CONFLICT, message="Code already exist.")))
                course.modified_by = current_user.username
                course.update_db()

                # update course credit in StudentCourseScore table
                stu_courses = StudentCourseScore.get_students_by_course_id_or_code(course.id)
                for stu_course in stu_courses:
                    if course.credit != stu_course.credit:
                        stu_course.credit = course.credit
                        stu_course.calc_grade_scored_point(stu_course.score)
                    if course.code != stu_course.course_code:
                        stu_course.course_code == course.code
                    stu_course.update_db()
                
                course = get_course_details_by_id_or_code(course.id)
                
                message = f"Course: {course.course_code} Updated Successfully"
                response = {"message": message, "data": course}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Student Not Found.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")

    # DELETE SPECIFIC COURSE (by ID or Code)
    @course_namespace.doc(description="Delete Specific Course (Admins Only)")
    @jwt_required()
    def delete(self, course_id_or_code):
        """Delete Course by ID or Code"""
        if current_user.is_admin:
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if course:            
                course.delete_from_db()
                return {"message": f"Course {course.code} Deleted Successfully!"}, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, "Student Not Found.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only.")
    

"""GET ALL STUDENTS REGISTERED FOR A COURSE"""
@course_student_namespace.route("/<course_id_or_code>")
class GetCourseStudents(Resource):
    @course_student_namespace.marshal_with(course_students_response_model)
    @course_student_namespace.doc(description="Retrieve Specific Course Students (Admin Only)", params=dict(course_id_or_code="Course Id or Code"))
    @jwt_required()
    def get(self, course_id_or_code):
        """
        Get All Students Offering Specific Course
        """
        if current_user.is_admin:
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if course:
                course_students = get_course_students(course.id)
                
                message = f"All Course Students Retrieved Successfully"
                response = {"message": message, "data": course_students}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, message="Course ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


"""GET-UPDATE STUDENTS GRADES FOR A COURSE (ADMIN ONLY)"""
@course_student_namespace.route("/grades/<course_id_or_code>", doc={"params": dict(course_id_or_code="Course Id or Code")})
class GetUpdateCourseStudentsGrades(Resource):

    # GET ALL STUDENTS GRADES FOR A COURSE
    @course_student_namespace.marshal_with(course_students_grades_response_model)
    @course_student_namespace.doc(description="Retrieve Students Grades for a Course (Admin Only)")
    @jwt_required()
    def get(self, course_id_or_code):
        """Get Multiple Students Grades for a Course"""
        if current_user.is_admin:
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if course:
                course_students = get_course_students(course.id)

                message = f"All Students Grades for Course {course.code} Retrieved Successfully"
                response = {"message": message, "data": course_students}
                return response, HTTPStatus.OK
            abort(HTTPStatus.NOT_FOUND, message="Course Not Found")
        abort(HTTPStatus.UNAUTHORIZED, message="Admins Only")

    # UPDATE MULTIPLE STUDENTS GRADE FOR A COURSE
    @course_student_namespace.expect(update_multiple_course_students_scores_model)
    @course_student_namespace.marshal_with(course_students_grades_response_model)
    @course_student_namespace.doc(description="Update Multiple Students Course Grades (Admin Only)")
    @jwt_required()
    def patch(self, course_id_or_code):
        """Update Multiple Students Grades for a Course"""
        if current_user.is_admin:
            course = Course.get_by_course_id_or_code(course_id_or_code)
            if course:
                data = course_student_namespace.payload
                student_ids_or_matrics = []
                valid_student_matrics = []
                score_list = []
                for key in data.keys():
                    if key.startswith("student"):
                        student_ids_or_matrics.append(data[key])
                    if key.startswith("score"):
                        score_list.append(data[key])

                i = 0
                while i < len(student_ids_or_matrics):
                    student = Student.get_by_student_id_or_matric(student_ids_or_matrics[i])                    
                    if student:
                        # add to valid student code list
                        valid_student_matrics.append(student.matric_no)
                        # check and get student course
                        student_course = StudentCourseScore.get_student_course_by_id_or_code(student.student_id, course.id)
                        if student_course:                            
                            # update student course score, grade, grade_point and scored_points
                            student_course.score = score_list[i]
                            student_course.calc_grade_scored_point(score_list[i])
                            student_course.modified_by = current_user.username
                            student_course.update_db()
                            # updating the student records table
                            student_records = StudentRecord.get_by_student_id_or_matric(student.student_id)
                            student_records.calc_points_gpa_honours()
                            student_records.modified_by = current_user.username
                            student_records.update_db()
                    i += 1
                # response data
                course_students = get_course_students_by_id_or_matric_list(valid_student_matrics, course.id)

                message = f"Students: {valid_student_matrics} Grades for Course: {course.code} Updated Successfully!"
                response = {"message": message, "data": course_students} 
                return response, HTTPStatus.OK
            abort(HTTPStatus.CONFLICT, message="Course does not exist.")
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")
