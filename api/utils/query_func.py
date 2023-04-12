from typing import List
from flask_jwt_extended import current_user, get_jwt_identity
from sqlalchemy import and_, asc, desc, func, or_
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
from sqlalchemy.orm import aliased


# create aliases for the tables
StudentAlias = aliased(Student, flat=True)
CourseAlias = aliased(Course, flat=True)
DepartmentAlias = aliased(Department, flat=True)
TeacherAlias = aliased(Teacher, flat=True)


"""DEPARTMENT FUNCTIONS"""

def get_department_students(department_id):
    """
    Gets All Students in a Department,
    by querying students and departments tables.
    
    :param department_id: the id of the department
    :type department_id: int
    :return: departmental students
    :rtype: list:dict
    """
    department_students = (
        db.session.query(
            StudentAlias.student_id,
            StudentAlias.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            StudentAlias.department_id,
            DepartmentAlias.name.label("department_name"),
            DepartmentAlias.code.label("department_code")
        )
        .outerjoin(DepartmentAlias, DepartmentAlias.id == StudentAlias.department_id)
        .filter(StudentAlias.department_id == department_id)
        .all()
    )
    return department_students

def get_department_courses(department_id):
    """
    Gets All Courses in a Department,
    by querying departments and courses tables.
    
    :param department_id: the id of the department
    :type department_id: int
    :return: departmental courses
    :rtype: list:dict
    """
    department_courses = (
        db.session.query(
            CourseAlias.id.label("course_id"),
            CourseAlias.code.label("course_code"),
            CourseAlias.name.label("course_name"),
            CourseAlias.department_id,
            DepartmentAlias.name.label("department_name"),
            DepartmentAlias.code.label("department_code")
        )
        .outerjoin(DepartmentAlias, DepartmentAlias.id == CourseAlias.department_id)
        .filter(CourseAlias.department_id == department_id)
        .all()
    )
    return department_courses

def get_department_teachers(department_id):
    """
    Gets All Teachers in a Department,
    by querying departments and teachers tables.
    
    :param department_id: the id of the department
    :type department_id: int
    :return: departmental teachers
    :rtype: list:dict
    """
    department_teachers = (
        db.session.query(
            TeacherAlias.teacher_id,
            TeacherAlias.staff_code,
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
            TeacherAlias.department_id,
            DepartmentAlias.name.label("department_name"),
            DepartmentAlias.code.label("department_code")
        )
        .outerjoin(DepartmentAlias, DepartmentAlias.id == TeacherAlias.department_id)
        .filter(TeacherAlias.department_id == department_id)
        .all()
    )
    return department_teachers


"""TEACHER FUNCTIONS"""

def get_current_teacher():
    """"Gets the Currently Logged-in Teacher's Data"""
    current_teacher = Teacher.get_by_teacher_id_or_code(current_user.teacher_id)
    return current_teacher

def get_teacher_students(teacher_id):
    """
    Gets All Students offering a Specific Teacher's Course(s),
    by querying students, courses, teachers and student_courses_scores tables.
    
    :param teacher_id: the id of the teacher
    :type teacher_id: int
    :return: teacher's students
    :rtype: list:dict
    """
    teacher_students = (
        db.session.query(
            StudentCourseScore.student_id,
            StudentCourseScore.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            # StudentCourseScore.course_code,
            # CourseAlias.name.label("course_name"),
            Student.student_courses,
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
            TeacherAlias.staff_code
        )
        .distinct()
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .filter(TeacherAlias.teacher_id == teacher_id)
        .all()
    )
    return teacher_students

def get_teacher_courses(teacher_id):
    """
    Gets All Courses taken by a Specific Teacher,
    by querying courses and teachers table.
    
    :param teacher_id: the id of the teacher
    :type teacher_id: int
    :return: teacher's course(s)
    :rtype: list:dict
    """
    teacher_courses = (
        db.session.query(
            CourseAlias.id.label("course_id"),
            CourseAlias.code.label("course_code"),
            CourseAlias.name.label("course_name"),
            CourseAlias.teacher_id,
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
            TeacherAlias.staff_code
        )
        .distinct()
        .outerjoin(CourseAlias, CourseAlias.teacher_id == TeacherAlias.teacher_id)
        .filter(TeacherAlias.teacher_id == teacher_id)
        .all()
    )
    return teacher_courses

def get_teacher_students_grades(teacher_id, course_id):
    """
    Gets All Students' Grades for a Specific Teacher's Course,
    by querying students, courses, teachers and student_courses_scores table.
    
    :param teacher_id: the id of the teacher
    :param course_id: the id of the course
    :type teacher_id: int
    :type course_id: int
    :return: students' grades for a teacher's course
    :rtype: list:dict
    """
    teacher_students_grades = (
        db.session.query(
            StudentCourseScore.student_id,
            StudentCourseScore.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            StudentCourseScore.course_code,
            CourseAlias.name.label("course_name"),
            StudentCourseScore.credit,
            StudentCourseScore.score,
            StudentCourseScore.grade,
            StudentCourseScore.scored_point,
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
            TeacherAlias.staff_code
        )
        .distinct()
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .filter(TeacherAlias.teacher_id == teacher_id,
                CourseAlias.id == course_id)
        .order_by(desc(StudentCourseScore.score))
        .all()
    )
    return teacher_students_grades


"""COURSES FUNCTION"""

def get_all_courses():
    """
    Gets All Courses from the courses table in the database,
    by querying courses, departments and teachers tables.

    :return: all courses.
    :rtype: list:dict
    """
    courses = (
        db.session.query(
            CourseAlias.id,
            CourseAlias.name.label("course_name"),
            CourseAlias.code.label("course_code"),
            CourseAlias.credit.label("course_credit"),
            DepartmentAlias.name.label("department_name"),
            CourseAlias.teacher_id,
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
            (TeacherAlias.gender + "").label("gender"),
            CourseAlias.created_by,
            CourseAlias.created_on,
        )
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .outerjoin(DepartmentAlias, DepartmentAlias.id == CourseAlias.department_id)
        .order_by(CourseAlias.id)
        .all()
    )
    return courses

def get_course_details_by_id_or_code(course_id_or_code):
    """
    Gets a Specific Course Details by either Course Id or Code,
    by querying courses, department and teachers tables.

    :param course_id_or_code: Course Id or Code
    :type course_id: str
    :return: course details
    :rtype: list:dict
    """
    course = (
        db.session.query(
            CourseAlias.id,
            CourseAlias.name.label("course_name"),
            CourseAlias.code.label("course_code"),
            CourseAlias.credit.label("course_credit"),
            CourseAlias.department_id,
            DepartmentAlias.name.label("department_name"),
            CourseAlias.teacher_id,
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
            (TeacherAlias.gender + "").label("gender"),
            CourseAlias.created_by,
            CourseAlias.created_on,
        )
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .outerjoin(DepartmentAlias, DepartmentAlias.id == CourseAlias.department_id)
        .filter(or_(CourseAlias.id == course_id_or_code, CourseAlias.code == course_id_or_code))
        .first()
    )
    return course

def get_course_students(course_id):
    """
    Gets All Students Offering for a Specific Course,
    by querying student_courses_score, students and courses tables.

    :param course_id: Course Id
    :type course_id: int
    :return: course students
    :rtype: list:dict
    """
    course_students = (
        db.session.query(
            StudentCourseScore.student_id,
            StudentCourseScore.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            (StudentAlias.gender + "").label("gender"),
            StudentCourseScore.course_id,
            StudentCourseScore.course_code,
            CourseAlias.name.label("course_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score,
            StudentCourseScore.grade,
            StudentCourseScore.grade_point,
            StudentCourseScore.scored_point,
        )
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .filter(StudentCourseScore.course_id == course_id)
        .order_by(desc(StudentCourseScore.score))
        .all()
    )
    return course_students

def get_course_students_by_id_or_matric_list(student_ids_or_matric:list, course_id):
    """
    Gets Specific List of Students Offering a Course by their Student Ids or Codes in a List,
    by querying the student, student_courses_scores, courses and teachers table.

    :param student_id_or_matric: a list of student ids or matric no.
    :param course_ids: the id of the course
    :type student_id_or_matric: list:str
    :type course_id: int
    :return: the query result
    :rtype: list:dict
    """
    course_students = (
        db.session.query(
            StudentAlias.student_id,
            StudentAlias.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            StudentCourseScore.course_id,
            CourseAlias.code.label("course_code"),
            CourseAlias.name.label("course_name"),
            CourseAlias.credit.label("course_credit"),
            DepartmentAlias.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label("teacher_name"),
        )
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(DepartmentAlias, DepartmentAlias.id == StudentCourseScore.department_id)
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .filter(
            StudentCourseScore.course_id == course_id,
            or_(StudentCourseScore.student_id.in_(student_ids_or_matric),
                StudentCourseScore.matric_no.in_(student_ids_or_matric)
            )
        )
        .order_by(desc(StudentCourseScore.score))
        .all()
    )
    return course_students


"""STUDENT FUNCTIONS"""

def get_current_student():
    """Gets Currently Logged-in Students Data
    :rtype: list:dict
    """
    current_student = Student.get_by_student_id_or_matric(current_user.student_id)
    return current_student

def get_student_records(student_id):
    """
    Gets a Specific Student Records (course count, total credits, total points, GPA and honours),
    by querying students_records, students and departments tables.

    :param student_id: Student ID
    :type student_id: int
    :return: student records
    :rtype: list:dict
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

def get_all_students_records():
    """
    Gets All Students' Records (course count, total credits, total points, GPA and honours),
    by querying students_records, students and departments tables.

    :return: all students records
    :rtype: list:dict
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

def get_student_courses_details(student_id):
    """
    Gets All Courses Details Offered by Specific Student,
    by querying students, student_courses_scores, courses, departments and teachers tables.

    :param student_id: Student Id
    :type student_id: int
    :return: student courses details
    :rtype: list:dict
    """
    student_courses = (
        db.session.query(
            StudentAlias.student_id,
            StudentAlias.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            StudentCourseScore.course_id,
            CourseAlias.code.label("course_code"),
            CourseAlias.name.label("course_name"),
            CourseAlias.credit.label("course_credit"),
            DepartmentAlias.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label(
                "teacher_name"
            ),
        )
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(DepartmentAlias, DepartmentAlias.id == StudentCourseScore.department_id)
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .filter(StudentCourseScore.student_id == student_id)
        .all()
    )
    
    return student_courses

    
# GET SPECIFIC COURSE OFFERED BY A STUDENT
def get_student_course_detail_by_id(student_id, course_id):
    """
    Gets a Specific Course Offered by a Specific Student,
    by querying students, student_courses_scores, courses, departments and teachers tables.

    :param student_id: the id of the student
    :param course_id: the id of the course
    :type student_id: int
    :type course_id: int
    :return: student course
    :rtype: list:dict
    """
    student_course = (
        db.session.query(
            StudentAlias.student_id,
            StudentAlias.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            StudentCourseScore.course_id,
            CourseAlias.code.label("course_code"),
            CourseAlias.name.label("course_name"),
            CourseAlias.credit.label("course_credit"),
            DepartmentAlias.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label(
                "teacher_name"
            ),
        )
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(DepartmentAlias, DepartmentAlias.id == StudentCourseScore.department_id)
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .filter(
            StudentCourseScore.student_id == student_id,
            StudentCourseScore.course_id == course_id,
        )
        .all()
    )
    return student_course

def get_student_courses_by_id_or_code_list(student_id_or_matric, course_ids_or_codes:list):
    """
    Gets Specific Courses Offered by a Specific Student by their Course Ids or Codes in a list,
    by querying students, student_courses_scores, courses, departments and teachers tables.

    :param student_id_or_matric: the id or matric no. of the student
    :param course_ids_or_codes: the ids or codes of courses
    :type student_id: str
    :type course_ids: list:str
    :return: student courses
    :rtype: list:dict
    """
    student_courses = (
        db.session.query(
            StudentAlias.student_id,
            StudentAlias.matric_no,
            (StudentAlias.first_name + " " + StudentAlias.last_name).label("student_name"),
            StudentAlias.gender,
            StudentCourseScore.course_id,
            CourseAlias.code.label("course_code"),
            CourseAlias.name.label("course_name"),
            CourseAlias.credit.label("course_credit"),
            DepartmentAlias.name.label("department_name"),
            StudentCourseScore.registered_on,
            StudentCourseScore.registered_by,
            StudentCourseScore.score.label("score"),
            StudentCourseScore.grade.label("grade"),
            StudentCourseScore.grade_point.label("grade_point"),
            StudentCourseScore.scored_point.label("scored_point"),
            (TeacherAlias.title + " " + TeacherAlias.first_name + " " + TeacherAlias.last_name).label(
                "teacher_name"
            ),
        )
        .outerjoin(CourseAlias, CourseAlias.id == StudentCourseScore.course_id)
        .outerjoin(StudentAlias, StudentAlias.student_id == StudentCourseScore.student_id)
        .outerjoin(DepartmentAlias, DepartmentAlias.id == StudentCourseScore.department_id)
        .outerjoin(TeacherAlias, TeacherAlias.teacher_id == CourseAlias.teacher_id)
        .filter(
            or_(StudentCourseScore.student_id == student_id_or_matric,
                StudentCourseScore.matric_no == student_id_or_matric),
            or_(StudentCourseScore.course_id.in_(course_ids_or_codes), 
                StudentCourseScore.course_code.in_(course_ids_or_codes)),
        )
        .order_by(asc(CourseAlias.name))
        .all()
    )
    return student_courses
