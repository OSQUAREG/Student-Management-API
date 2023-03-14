from sqlalchemy import and_, func
from sqlalchemy.orm import defer
from . import db
from ..models import (
    User,
    Student,
    Teacher,
    Department,
    Course,
    StudentCourseScore,
    StudentRecord,
)


"""USER FUNCTIONS"""

def check_email_exist(email):
    email_exist = User.query.filter_by(email=email).first()
    return True if email_exist else False


"""DEPARTMENT FUNCTIONS"""

def get_all_departments():
    return Department.query.all()


def check_department_exist(code) -> bool:
    course_exist = Department.query.filter_by(code=code).first()
    return True if course_exist else False


"""TEACHER FUNCTIONS"""

def get_all_teachers():
    return Teacher.query.all()


"""COURSES FUNCTION"""

def get_all_courses():
    return Course.query.all()

def check_course_code_exist(code) -> bool:
    code_exist = Course.query.filter_by(code=code).first()
    return True if code_exist else False

def check_course_exist(course_id) -> bool:
    course_exist = Course.query.filter_by(id=course_id).first()
    return True if course_exist else False

def get_all_courses():
    """function to get all courses from the database."""
    courses = (
        db.session.query(
            Course.id,
            Course.name.label("course_name"),
            Course.code.label("course_code"),
            Course.credit.label("course_credit"),
            Department.name.label("department_name"),
            Course.teacher_id,
            (Teacher.title + " " + Teacher.first_name + " " + Teacher.last_name).label(
                "teacher"
            ),
            (Teacher.gender + "").label("gender"),
            Course.created_by,
            Course.created_on,
        )
        .outerjoin(Teacher, Teacher.teacher_id == Course.teacher_id)
        .outerjoin(Department, Department.id == Course.department_id)
        .order_by(Course.id)
        .all()
    )
    return courses


def get_course_details_by_id(course_id):
    """
    function to get a specific course details by passing the course id as an argument.

    :param course_id: Course ID
    :type course_id: int
    :return: the result of the query
    :rtype: object
    """
    course = (
        db.session.query(
            Course.id,
            Course.name.label("course_name"),
            Course.code.label("course_code"),
            Course.credit.label("course_credit"),
            Department.name.label("department_name"),
            Course.teacher_id,
            (Teacher.title + " " + Teacher.first_name + " " + Teacher.last_name).label(
                "teacher"
            ),
            (Teacher.gender + "").label("gender"),
            Course.created_by,
            Course.created_on,
        )
        .outerjoin(Teacher, Teacher.teacher_id == Course.teacher_id)
        .outerjoin(Department, Department.id == Course.department_id)
        .filter(Course.id == course_id)
        .first()
    )
    return course


# Get Students Registered for a Course
def get_course_students(course_id):
    """
    function to get all students that regostered for a certain course by passing the course id as an argument.

    :param course_id: Course ID
    :type course_id: int
    :return: the result of the query
    :rtype: object
    """
    course_students = (
        db.session.query(
            StudentCourseScore.student_id,
            StudentCourseScore.matric_no,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            (Student.gender + "").label("gender"),
            StudentCourseScore.course_id,
            StudentCourseScore.course_code,
            Course.name.label("course_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
        )
        .outerjoin(Student, Student.student_id == StudentCourseScore.student_id)
        .outerjoin(Course, Course.id == StudentCourseScore.course_id)
        .filter(StudentCourseScore.course_id == course_id)
        .all()
    )
    return course_students


"""STUDENT FUNCTIONS"""

def get_all_students():
    """function to get all students from the databasae"""
    return Student.query.all()

def check_student_exist(student_id) -> bool:
    """function to check if student exist, by passing 'student_id' as an argument"""
    student_exist = Student.query.filter_by(student_id=student_id).first()
    return True if student_exist else False

# GET A STUDENT RECORDS
def get_student_records(student_id):
    """
    function to get all records (course count, total credits, total points, GPA and honours) for specific student by passing the student id as an argument.

    :param student_id: Student ID
    :type student_id: int
    :return: the result of the query
    :rtype: object
    """
    student_records = (
        db.session.query(
            StudentRecord.student_id,
            Student.matric_no,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            Student.gender,
            Department.name.label("department_name"),
            StudentRecord.course_count,
            StudentRecord.total_credits,
            StudentRecord.total_points,
            ((StudentRecord.gpa) / 100).label("GPA"),
            StudentRecord.honours,
        )
        .outerjoin(Student, Student.student_id == StudentRecord.student_id)
        .outerjoin(Department, Department.id == Student.student_id)
        .filter(StudentRecord.student_id == student_id)
        .first()
    )
    return student_records

# GET ALL STUDENTS RECORDS
def get_all_students_records():
    """
    function to get all records (course count, total credits, total points, GPA and honours) for all students.
    """
    students_records = (
        db.session.query(
            StudentRecord.student_id,
            Student.matric_no,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            Student.gender,
            Department.name.label("department_name"),
            StudentRecord.course_count,
            StudentRecord.total_credits,
            StudentRecord.total_points,
            ((StudentRecord.gpa) / 100).label("GPA"),
            StudentRecord.honours,
        )
        .outerjoin(Student, Student.student_id == StudentRecord.student_id)
        .outerjoin(Department, Department.id == Student.student_id)
        .all()
    )
    return students_records


# GET ALL COURSES OFFERED BY A STUDENT
def get_student_courses_details(student_id):
    """
    function to get all courses details registered by specific student by passing student id as an argument.

    :param student_id: Student ID
    :param course_id: Course ID
    :type student_id: int
    :type course_id: int
    :return: the result of the query
    :rtype: object
    """
    student_courses = (
        db.session.query(
            Student.student_id,
            Student.matric_no,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            Student.gender,
            StudentCourseScore.course_id,
            Course.code.label("course_code"),
            Course.name.label("course_name"),
            Course.credit.label("course_credit"),
            Department.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (Teacher.title + " " + Teacher.first_name + " " + Teacher.last_name).label(
                "teacher"
            ),
        )
        .outerjoin(Course, Course.id == StudentCourseScore.course_id)
        .outerjoin(Student, Student.student_id == StudentCourseScore.student_id)
        .outerjoin(Department, Department.id == StudentCourseScore.department_id)
        .outerjoin(Teacher, Teacher.teacher_id == Course.teacher_id)
        .filter(StudentCourseScore.student_id == student_id)
        .all()
    )
    return student_courses


# GET SPECIFIC COURSE OFFERED BY A STUDENT
def get_student_course_detail_by_id(student_id, course_id):
    """
    This function returns a specific course enrolled by a specific student by querying the database tables - courses (Course), teachers (Teacher) and students_courses (StudentCourse).

    :param student_id: the id of the student enrolling
    :param course_id: the id of the course being enrolled
    :type student_id: int
    :type course_id: int
    :return: the result of the query
    :rtype: object
    """
    student_course = (
        db.session.query(
            Student.student_id,
            Student.matric_no,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            Student.gender,
            StudentCourseScore.course_id,
            Course.code.label("course_code"),
            Course.name.label("course_name"),
            Course.credit.label("course_credit"),
            Department.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (Teacher.title + " " + Teacher.first_name + " " + Teacher.last_name).label(
                "teacher"
            ),
        )
        .outerjoin(Course, Course.id == StudentCourseScore.course_id)
        .outerjoin(Student, Student.student_id == StudentCourseScore.student_id)
        .outerjoin(Department, Department.id == StudentCourseScore.department_id)
        .outerjoin(Teacher, Teacher.teacher_id == Course.teacher_id)
        .filter(
            StudentCourseScore.student_id == student_id,
            StudentCourseScore.course_id == course_id,
        )
        .all()
    )
    return student_course


# GET SPECIFIC COURSE OFFERED BY A STUDENT
def get_student_courses_by_id_list(student_id, course_ids:list):
    """
    This function returns a list of course just enrolled by a specific student by passing the student ID and the course IDs as a list.

    :param student_id: the Student ID
    :param course_ids: the Course IDs to be enrolled
    :type student_id: int
    :type course_ids: list
    :return: the query result
    :rtype: object
    """
    student_courses = (
        db.session.query(
            Student.student_id,
            Student.matric_no,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            Student.gender,
            StudentCourseScore.course_id,
            Course.code.label("course_code"),
            Course.name.label("course_name"),
            Course.credit.label("course_credit"),
            Department.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (Teacher.title + " " + Teacher.first_name + " " + Teacher.last_name).label(
                "teacher"
            ),
        )
        .outerjoin(Course, Course.id == StudentCourseScore.course_id)
        .outerjoin(Student, Student.student_id == StudentCourseScore.student_id)
        .outerjoin(Department, Department.id == StudentCourseScore.department_id)
        .outerjoin(Teacher, Teacher.teacher_id == Course.teacher_id)
        .filter(
            StudentCourseScore.student_id == student_id,
            StudentCourseScore.course_id.in_(course_ids),
        )
        .all()
    )
    return student_courses



"""CHECK FUNCTIONS"""

# Check if Student Registered for a Course
def check_student_registered_course(student_id, course_id) -> bool:
    student_enrollled_course = StudentCourseScore.query.filter(
        StudentCourseScore.student_id == student_id,
        StudentCourseScore.course_id == course_id,
    ).first()
    return True if student_enrollled_course else False


# Delete Student Registration for a Course
def get_student_registered_course_by_id(student_id, course_id) -> None:
    student_enrollled_course = StudentCourseScore.query.filter(
        StudentCourseScore.student_id == student_id,
        StudentCourseScore.course_id == course_id,
    ).first()
    return student_enrollled_course
