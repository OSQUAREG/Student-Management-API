from flask_restx import fields
from ..course import course_namespace


# CREATE COURSE SCHEMA MODEL
new_course_model = course_namespace.model(
    name="New Course Model",
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
    name="Course Model",
    model={
        "id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "course_credit": fields.String(description="Course Credit"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "department_id": fields.String(description="Deparment Id"),
        "department_name": fields.String(description="Department Name"),
        "teacher_id": fields.Integer(description="Teaacher ID"),
        "teacher_name": fields.String(description="Teacher Full Name"),
        "gender": fields.String(description="Gender"),
    },
)

course_response_model = course_namespace.model(
    name="Course Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(course_model, description="Response Data")
    }
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
        "teacher_name": fields.String(description="Teacher Full Name"),
        "registered_on": fields.DateTime(description="Created Date"),
        "registered_by": fields.String(description="Creator's Username"),
    },
)

course_students_response_model = course_namespace.model(
    name="Course Students Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(course_students_model, description="Response Data")
    }
)


# COURSE STUDENTS GRADES SCHEMA MODEL
course_students_grades_model = course_namespace.model(
    name="Course Students Grades Model",
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

course_students_grades_response_model = course_namespace.model(
    name="Course Students Grades Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(course_students_grades_model, description="Response Data")
    }
)


# UPDATE COURSE SCHEMA
update_course_model = course_namespace.model(
    name="Update Course Model",
    model={
        "name": fields.String(description="Course Name"),
        "code": fields.String(description="Course Code"),
        "credit": fields.String(description="Course Credit"),
        "department": fields.String(description="Department Id or Code"),
        "teacher": fields.String(description="Teacher Id or Staff Code")
    },
)


update_multiple_course_students_scores_model = course_namespace.model(
    name="Update Multiple Students Grades for a Course",
    model={
        "student1": fields.Integer( description="Student 1 Id or Code"),
        "score1": fields.Integer(description="Student 1 Score"),
        "student2": fields.Integer(description="Student 2 Id or Code"),
        "score2": fields.Integer(description="Student 2 Score"),
        "student3": fields.Integer(description="Student 3 Id or Code"),
        "score3": fields.Integer(description="Student 3 Score"),
        "student4": fields.Integer(description="Student 4 Id or Code"),
        "score4": fields.Integer(description="Student 4 Score"),
        "student5": fields.Integer(description="Student 5 Id or Code"),
        "score5": fields.Integer(description="Student 5 Score"),
        "student6": fields.Integer(description="Student 6 Id or Code"),
        "score6": fields.Integer(description="Student 6 Score"),
        "student7": fields.Integer(description="Student 7 Id or Code"),
        "score7": fields.Integer(description="Student 7 Score"),
        "student8": fields.Integer(description="Student 8 Id or Code"),
        "score8": fields.Integer(description="Student 8 Score"),
        "student9": fields.Integer(description="Student 9 Id or Code"),
        "score9": fields.Integer(description="Student 9 Score"),
        "student10": fields.Integer(description="Student 10 Id or Code"),
        "score10": fields.Integer(description="Student 10 Score"),
    },
)

