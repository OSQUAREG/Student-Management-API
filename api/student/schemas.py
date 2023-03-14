from flask_restx import fields
from ..student import student_namespace
from ..course.schemas import course_model


# STUDENT SCHEMA
student_model = student_namespace.model(
    name="Student/Teacher Details",
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
        "is_active": fields.String(description="Is Active Flag"),
        "department_id": fields.String(description="Department ID"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    },
)

# STUDENT RECORDS SCHEMA
student_records_model = student_namespace.model(
    name="Student Records",
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

# STUDENT ALL COURSES SCHEMA
student_course_model = student_namespace.model(
    name="Student Course",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(model=student_model, description="Student"),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "course_credit": fields.Integer(description="Course Credit"),
        "department_name": fields.String(description="Department Name"),
        "registered_on": fields.DateTime(description="Date of Course Registration"),
        "registered_by": fields.String(description="Username of Registrar"),      
        "teacher": fields.String(description="Teacher Full Name"),
    }
)


# STUDENT SPECIFIC COURSE
student_grades_model = student_namespace.model(
    name="Student Specific Course",
    model={
        "matric_no": fields.String(model=student_model, description="Student"),
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


# UPDATE STUDENT SCHEMA
update_student_model = student_namespace.model(
    name="Update Student Details",
    model={
        "first_name": fields.String(description="Student First Name"),
        "last_name": fields.String(description="Student Last Name"),
        "email": fields.String(description="Student Email"),
    },
)


register_multiple_course_model = student_namespace.model(
    name="Register Multiple Course",
    model={
        "course1": fields.Integer(description="Course 1"),
        "course2": fields.Integer(description="Course 2"),
        "course3": fields.Integer(description="Course 3"),
        "course4": fields.Integer(description="Course 4"),
        "course5": fields.Integer(description="Course 5"),
    },
)


score_model = student_namespace.model(
    name="Score Model",
    model={
        "score": fields.Integer(required=True, description="Student Score for a Course"),
    }
)
