from flask_restx import fields
from ..student import student_namespace
from ..course.schemas import course_model


# STUDENT SCHEMA
student_model = student_namespace.model(
    name="Student Details",
    model={
        "id": fields.Integer(description="User ID"),
        "first_name": fields.String(description="First Name"),
        "last_name": fields.String(description="Last Name"),
        "gender": fields.String(description="Gender", enum=["MALE", "FEMALE"]),
        "matric_no": fields.String(description="Student Matric No."),
        "gpa": fields.Float(description="Student GPA"),
        "email": fields.String(description="Email"),
        "is_active": fields.Boolean(description="Is Active Flag"),
        "date_registered": fields.DateTime(description="Date Registered"),
        # "courses": fields.Nested(student_course_list),
    },
)

student_courses = student_namespace.model(
    name="Student Courses",
    model={
        "student_id": fields.Nested(model=student_model, description="Student"),
        "course_id": fields.Nested(model=course_model, description="Course")
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


# # STUDENT REGISTER COURSES SCHEMA
# update_student_model = student_namespace.model(
#     name="Student Register Courses",
#     model={
#         "course_id": fields.String(description="Student First Name"),
#     },
# )
