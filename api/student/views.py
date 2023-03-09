from ..student import student_namespace
from flask_restx import Resource
from sqlalchemy import and_, desc, asc, func
from http import HTTPStatus
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity
from ..models import User, StudentCourse, Course, Teacher
from ..student.schemas import student_model, update_student_model, student_courses


# GET ALL STUDENTS
@student_namespace.route("/")
class Students(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Retrieve All Students (Admin Only)")
    @jwt_required()
    def get(self):
        """
        Admin: Get All Students
        """
        if current_user.is_admin:
            students = User.query.\
                filter(User.matric_no.contains("ST/")).\
                    order_by(asc(User.id)).all()

            return students, HTTPStatus.OK


@student_namespace.route("/<matric_no>")
class GetUpdateDeleteSpecificStudent(Resource):

    # GET SPECIFIC STUDENT (by Matric No.)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Retrieve Specific Student (Admin Only)")
    @jwt_required()
    def get(self, matric_no):
        """
        Admin: Get Specific Student
        """
        if current_user.is_admin:
            student = User.get_by_matric_no(matric_no)
            return student, HTTPStatus.OK

    # UPDATE SPECIFIC STUDENT (by Matric No.)
    @student_namespace.expect(update_student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Update Specific Student (Admin Only)")
    @jwt_required()
    def put(self, matric_no):
        """
        Admin: Update Specific Student
        """
        if current_user.is_admin:
            student = User.get_by_matric_no(matric_no)
            data = student_namespace.payload

            student.first_name = data["first_name"]
            student.last_name = data["last_name"]
            student.email = data["email"]
            
            student.update_db()

            return student, HTTPStatus.OK

    # DELETE SPECIFIC STUDENT (by Matric No.)
    @student_namespace.doc(description="Delete Specific Student (Admin Only)")
    @jwt_required()
    def delete(self, matric_no):
        """
        Admin: Delete Specific Student
        """
        if current_user.is_admin:
            student = User.get_by_matric_no(matric_no)

            student.delete_from_db()

            return {"message": "Student Deleted Successfully!"}, HTTPStatus.OK


@student_namespace.route("/enroll/<int:course_id>")
class EnrollCourse(Resource):

    # STUDENT REGISTER FOR COURSES
    @student_namespace.marshal_with(student_courses)
    @student_namespace.doc(description="Student Course Enrolment (Student Only)")
    @jwt_required()
    def post(self, course_id):
        """
        Student: Enroll Courses
        """
        student = User.query.filter_by(id=current_user.id).first()
        course = Course.get_by_id(course_id)
        
        student_course_exist = StudentCourse.query.filter_by(and_(student_id=student.id, course_id=course.id))
        # student_course_count = pass

        # check if course id exist
        if course:
            # check if student already enrolled course
            if student_course_exist:
                student_course = StudentCourse(student_id=student.id, course_id=course_id)

                student_course.save_to_db()

                # add to student course count
                student.courses_count = student.course_count + 1
                student.update_db()

                return student_course

# GET LOGGED-IN STUDENT DASHBOARD
@student_namespace.route("/student")
class GetStudentDashboard(Resource):
    
    # GET LOGGED-IN STUDENT DETAILS
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Retrieve Current Student Details (Students Only)")
    @jwt_required()
    def get(self):
        """
        Student: Get Current Student Details
        """
        matric_no = get_jwt_identity()
        student = User.query.filter_by(matric_no=matric_no).first()
        
        return student, HTTPStatus.CREATED


