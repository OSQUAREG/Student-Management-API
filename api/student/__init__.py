from flask_restx import Namespace

student_namespace = Namespace(name="Student", description="Current Student Operations")

adm_student_namespace = Namespace(name="Students", description="Operations on Student (Admins Only)")

student_courses_namespace = Namespace(name="Student Courses", description="Operations on Student Courses (Admins Only)")

student_grades_namespace = Namespace(name="Student Grades", description="Operations on Student Grades (Admins Only)")

student_records_namespace = Namespace(name="Student Records", description="Operations on Student Records (Admins Only)")