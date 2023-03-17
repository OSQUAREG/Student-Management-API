from flask_restx import fields
from ..course import course_namespace


# CREATE COURSE SCHEMA MODEL
new_course_model = course_namespace.model(
    name="New Course Details",
    model={
        "code": fields.String(required=True, description="Course Code"),
        "name": fields.String(required=True, description="Course Name"),
        "credit": fields.Integer(required=True, description="Course Credit"),
        "department_id": fields.Integer(required=True, description="Department ID"),
        "teacher_id": fields.String(required=True, description="Teacher ID"),
    },
)


# COURSE SCHEMA MODEL
course_model = course_namespace.model(
    name="Course Details",
    model={
        "id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "course_credit": fields.String(description="Course Credit"),
        "department_name": fields.String(description="Department ID"),
        "gender": fields.String(description="Gender"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "teacher_id": fields.Integer(description="Teaacher ID"),
        "teacher": fields.String(description="Teacher Full Name"),
    },
)


# COURSE STUDENTS SCHEMA MODEL
course_students_model = course_namespace.model(
    name="Course Students",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(description="Matric No."),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "registered_on": fields.DateTime(description="Created Date"),
        "registered_by": fields.String(description="Creator's Username"),
    },
)


# COURSE STUDENTS GRADES SCHEMA MODEL
course_students_grades_model = course_namespace.model(
    name="Student Specific Course",
    model={
        "student_id": fields.Integer(description="student ID"),
        "matric_no": fields.String(description="Student"),
        "student_name": fields.String(description="Student Name"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "course_credit": fields.Integer(description="Course Credit"),
        "score": fields.Integer(description="Score"),
        "grade": fields.String(description="Grade"),
        "grade_point": fields.Integer(description="Grade Point"),
        "scored_point": fields.Integer(description="Scored Points"),
    }
)


update_multiple_course_students_scores_model = course_namespace.model(
    name="Update Multiple Students Grades for a Course",
    model={
        "student_id1": fields.Integer( description="Student 1 ID"),
        "score1": fields.Integer(description="Student 1 Score"),
        "student_id2": fields.Integer(description="Student 2 ID"),
        "score2": fields.Integer(description="Student 2 Score"),
        "student_id3": fields.Integer(description="Student 3 ID"),
        "score3": fields.Integer(description="Student 3 Score"),
        "student_id4": fields.Integer(description="Student 4 ID"),
        "score4": fields.Integer(description="Student 4 Score"),
        "student_id5": fields.Integer(description="Student 5 ID"),
        "score5": fields.Integer(description="Student 5 Score"),
        "student_id6": fields.Integer(description="Student 6 ID"),
        "score6": fields.Integer(description="Student 6 Score"),
        "student_id7": fields.Integer(description="Student 7 ID"),
        "score7": fields.Integer(description="Student 7 Score"),
        "student_id8": fields.Integer(description="Student 8 ID"),
        "score8": fields.Integer(description="Student 8 Score"),
        "student_id9": fields.Integer(description="Student 9 ID"),
        "score9": fields.Integer(description="Student 9 Score"),
        "student_id10": fields.Integer(description="Student 10 ID"),
        "score10": fields.Integer(description="Student 10 Score"),
    },
)

