from flask_restx import Namespace

course_namespace = Namespace(name="Courses", description="Operations on Courses (Admins Only)")

course_student_namespace = Namespace(name="Course Students", description="Operations on Course Students (Admins Only)")
