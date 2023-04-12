from flask_restx import fields
from ..student import student_namespace
from ..course.schemas import course_model


# STUDENT SCHEMA
student_model = student_namespace.model(
    name="Student Model",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "user_id": fields.Integer(description="User ID"),
        "title": fields.String(
            description="Title", enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"]
        ),
        "first_name": fields.String(description="First Name"),
        "last_name": fields.String(description="Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "username": fields.String(description="Username"),
        "email": fields.String(description="Email"),
        "type": fields.String(description="User Type"),
        "matric_no": fields.String(description="Student Matric No."),
        "is_active": fields.Boolean(description="Is Active Flag"),
        "department_id": fields.String(description="Department ID"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    },
)

student_response_model = student_namespace.model(
    name="Student Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(student_model, description="Response Data")
    }
)


# STUDENT ALL COURSES SCHEMA
student_course_model = student_namespace.model(
    name="Student Courses Model",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(description="Student"),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "course_credit": fields.Integer(description="Course Credit"),
        "department_name": fields.String(description="Department Name"),
        "registered_on": fields.DateTime(description="Date of Course Registration"),
        "registered_by": fields.String(description="Username of Registrar"),      
        "teacher_name": fields.String(description="Teacher Full Name"),
    }
)

student_course_response_model = student_namespace.model(
    name="Student Courses Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(student_course_model, description="Response Data")
    }
)


# STUDENT SPECIFIC COURSE
student_grades_model = student_namespace.model(
    name="Student Grades Model",
    model={
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

student_grades_response_model = student_namespace.model(
    name="Student Grades Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(student_grades_model, description="Response Data")
    }
)


# STUDENT RECORDS SCHEMA
student_records_model = student_namespace.model(
    name="Student Records Model",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(description="Student Matric No."),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "department_name": fields.String(description="Department Name"),
        "course_count": fields.Integer(description="Course Count"),
        "total_credits": fields.Integer(description="Total Credits"),
        "total_points": fields.Integer(description="Total Points"),
        "GPA": fields.Float(description="Student GPA"),
        "honours": fields.String(description="Honours"),
    }
)

student_records_response_model = student_namespace.model(
    name="Student Records Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(student_records_model, description="Response Data")
    }
)


# UPDATE STUDENT SCHEMA
update_student_model = student_namespace.model(
    name="Update Student Model",
    model={
        "title": fields.String(description="Student Title", enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"]),
        "first_name": fields.String(description="Student First Name"),
        "last_name": fields.String(description="Student Last Name"),
        "email": fields.String(description="Student Email"),
    },
)


register_multiple_student_courses_model = student_namespace.model(
    name="Student Multiple Course Registration",
    model={
        "course1": fields.Integer(description="Course 1 ID or Code"),
        "course2": fields.Integer(description="Course 2 ID or Code"),
        "course3": fields.Integer(description="Course 3 ID or Code"),
        "course4": fields.Integer(description="Course 4 ID or Code"),
        "course5": fields.Integer(description="Course 5 ID or Code"),
        "course6": fields.Integer(description="Course 6 ID or Code"),
        "course7": fields.Integer(description="Course 7 ID or Code"),
        "course8": fields.Integer(description="Course 8 ID or Code"),
        "course9": fields.Integer(description="Course 9 ID or Code"),
        "course10": fields.Integer(description="Course 10 ID or Code"),
    },
)


update_student_course_score_model = student_namespace.model(
    name="Update Single Score Model",
    model={
        "score": fields.Integer(required=True, description="Student Score for a Course"),
    }
)

update_multiple_student_courses_scores_model = student_namespace.model(
    name="Update Multiple Courses Grades for a Student",
    model={
        "course1": fields.Integer( description="Course 1 ID or Code"),
        "score1": fields.Integer(description="Course 1 Score"),
        "course2": fields.Integer(description="Course 2 ID or Code"),
        "score2": fields.Integer(description="Course 2 Score"),
        "course3": fields.Integer(description="Course 3 ID or Code"),
        "score3": fields.Integer(description="Course 3 Score"),
        "course4": fields.Integer(description="Course 4 ID or Code"),
        "score4": fields.Integer(description="Course 4 Score"),
        "course5": fields.Integer(description="Course 5 ID or Code"),
        "score5": fields.Integer(description="Course 5 Score"),
        "course6": fields.Integer(description="Course 6 ID or Code"),
        "score6": fields.Integer(description="Course 6 Score"),
        "course7": fields.Integer(description="Course 7 ID or Code"),
        "score7": fields.Integer(description="Course 7 Score"),
        "course8": fields.Integer(description="Course 8 ID or Code"),
        "score8": fields.Integer(description="Course 8 Score"),
        "course9": fields.Integer(description="Course 9 ID or Code"),
        "score9": fields.Integer(description="Course 9 Score"),
        "course10": fields.Integer(description="Course 10 ID or Code"),
        "score10": fields.Integer(description="Course 10 Score"),
    },
)
