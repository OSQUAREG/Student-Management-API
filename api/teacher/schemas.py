from flask_restx import fields

from api.models.users import Student
from ..teacher import teacher_namespace


# TEACHER SCHEMA
teacher_model = teacher_namespace.model(
    name="Teacher Details",
    model={
        "teacher_id": fields.Integer(description="Teacher ID"),
        "user_id": fields.Integer(description="User ID"),
        "title": fields.String(description="Title", enum=["PROF", "ENGR", "DR", "MR", "MRS", "MS"]),
        "first_name": fields.String(description="Teacher's First Name"),
        "last_name": fields.String(description="Teacher's Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "username": fields.String(description="Username"),
        "email": fields.String(description="An Email"),
        "staff_code": fields.String(description="Teacher's Staff Code"),
        "is_staff": fields.String(description="Is Staff Flag"),
        "type": fields.String(description="User Type"),
        "department_id": fields.String(description="Department ID"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    },
)

teacher_response_model = teacher_namespace.model(
    name="Course Students Grades Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(teacher_model, description="Response Data")
    }
)


# TEACHER COURSES
teacher_courses_model = teacher_namespace.model(
    name="Teacher Courses Model",
    model={
        "course_id": fields.Integer(description="Course Id"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        # "teacher_courses": fields.String(description="Teacher Courses"),
        "teacher_id": fields.Integer(description="Teacher Id"),
        "teacher_name": fields.String(description="Teacher Name"),
    }
)

teacher_courses_response_model = teacher_namespace.model(
    name="Teacher Courses Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(teacher_courses_model, description="Response Data")
    }
)

course_list_model = teacher_namespace.model(
    name="Course List Model",
    model={
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
    }
)

# TEACHER STUDENTS
teacher_students_model = teacher_namespace.model(
    name="Teacher Students Model",
    model={
        "student_id": fields.Integer(description="Student Id"),
        "matric_no": fields.String(description="Student Matric No."),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Student Gender"),
        # "student_courses": fields.Nested(course_list_model),
        "teacher_name": fields.String(description="Teacher Name"),
        "staff_code": fields.String(description="Teacher Staff Code")
    }
)

teacher_students_response_model = teacher_namespace.model(
    name="Course Students Grades Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(teacher_students_model, description="Response Data")
    }
)


# TEACHER STUDENTS GRADES
teacher_students_grades_model = teacher_namespace.model(
    name="Teacher Students Model",
    model={
        "student_id": fields.Integer(description="Student Id"),
        "matric_no": fields.String(description="Student Matric No."),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Student Gender"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "credit": fields.Integer(description="Course Credit"),
        "score": fields.Integer(description="Student Score"),
        "grade": fields.String(description="Student Grade"),
        "scored_point": fields.Integer(description="Scored Point"),
        "teacher_name": fields.String(description="Teacher Name"),
        "staff_code": fields.String(description="Teacher Staff Code")
    }
)

teacher_students_grades_response_model = teacher_namespace.model(
    name="Course Students Grades Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(teacher_students_grades_model, description="Response Data")
    }
)