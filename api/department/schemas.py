from ..department import department_namespace
from flask_restx import fields


department_model = department_namespace.model(
    name="Department Model",
    model={
        "id": fields.Integer(description="Department ID"),
        "name": fields.String(required=True, description="Department Name"),
        "code": fields.String(required=True, description="Course Code"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    }
)

department_response_model = department_namespace.model(
    name="Department Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(department_model)
    }
)


# DEPARTMENT STUDENTS SCHEMA MODEL
department_students_model = department_namespace.model(
    name="Department Students Model",
    model={
        "student_id": fields.Integer(description="Student ID"),
        "matric_no": fields.String(description="Matric No."),
        "student_name": fields.String(description="Student Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "department_id": fields.Integer(description="Department ID"),
        "department_code": fields.String(description="Department Code"),
        "department_name": fields.String(description="Department Name"),
    },
)

department_students_response_model = department_namespace.model(
    name="Department Students Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(department_students_model, description="Response Data")
    }
)


# DEPARTMENT COURSES SCHEMA MODEL
department_courses_model = department_namespace.model(
    name="Department Courses Model",
    model={
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course Code"),
        "course_name": fields.String(description="Course Name"),
        "department_id": fields.Integer(description="Department ID"),
        "department_code": fields.String(description="Department Code"),
        "department_name": fields.String(description="Department Name"),
    },
)

department_courses_response_model = department_namespace.model(
    name="Department Courses Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(department_courses_model, description="Response Data")
    }
)


# DEPARTMENT TEACHERS SCHEMA MODEL
department_teachers_model = department_namespace.model(
    name="Department Teachers Model",
    model={
        "teacher_id": fields.Integer(description="Teacher ID"),
        "staff_code": fields.String(description="Matric No."),
        "teacher_name": fields.String(description="Teacher Name"),
        "department_id": fields.Integer(description="Department ID"),
        "department_code": fields.String(description="Department Code"),
        "department_name": fields.String(description="Department Name"),
    },
)

department_teachers_response_model = department_namespace.model(
    name="Department Teachers Response Model",
    model={
        "message": fields.String(description="Response Message"),
        "data": fields.Nested(department_teachers_model, description="Response Data")
    }
)
