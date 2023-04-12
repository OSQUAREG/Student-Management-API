from datetime import datetime
import unittest
from flask_jwt_extended import create_access_token
from ..models import User, Student, Course, StudentCourseScore, StudentRecord, GradeScale, Department, Teacher, Admins
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
import os


class UnitTestCase(unittest.TestCase):
    # called before each test
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        # using a test client
        self.client = self.app.test_client()
        db.create_all()

    # called after each test case
    def tearDown(self):
        db.drop_all
        self.app_ctxt.pop()
        self.app = None
        self.client = None


year_str = str(datetime.utcnow().year)[-3:]


def get_auth_token_headers(identity):
    token = create_access_token(identity=identity)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


"""FUNCTIONS TO CREATE SINGLE RECORD DATA"""
def create_test_admin():
    test_admin = Admins(
        first_name="Admin",
        last_name="Test",
        gender="MALE",
        email="admin@test.com",
        admin_code="ADM-admin.test",
        username="admin.test",
        password_hash="admin@password",
        is_staff=True,
        is_admin=True,
    )
    test_admin.save_to_db()
    return test_admin


def create_test_super_admin():
    test_super_admin = Admins(
        first_name="Super",
        last_name="Admin",
        gender="MALE",
        email="superadmin@test.com",
        admin_code="ADM-super.admin",
        username="super.admin",
        password_hash="admin@password",
        is_staff=True,
        is_admin=True,
    )
    test_super_admin.save_to_db()
    return test_super_admin


def create_test_user():
    test_user = User(
        type="user",
        title="MR",
        first_name="Student",
        last_name="Test",
        username="student.test",
        email="student@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_STUDENT_PASSWORD"]),
        department_id=1
    )
    test_user.save_to_db()
    return test_user


def create_test_student():
    test_student = Student(
        type="student",
        title="MR",
        first_name="Student",
        last_name="Test",
        matric_no=f"STU-{year_str}-0000",
        username="student.test",
        email="student@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_STUDENT_PASSWORD"]),
        department_id=1
    )
    test_student.save_to_db()
    return test_student


def create_test_student_record():
    test_student_record = StudentRecord(
        student_id=1,
        matric_no=f"STU-{year_str}-0000",
        department_id=1,
    )
    test_student_record.save_to_db()

    return test_student_record


def create_test_grade_scale():
    test_grade_scale = []

    test_grade_a = GradeScale(
        grade="A",
        point=4,
        min=70,
        max=100
    )

    test_grade_b = GradeScale(
        grade="B",
        point=3,
        min=60,
        max=69
    )
    
    test_grade_a.save_to_db()
    test_grade_b.save_to_db()

    test_grade_scale.append(test_grade_a)
    test_grade_scale.append(test_grade_b)
    
    return test_grade_scale


def create_test_course():
    test_course = Course(
        name="Test Course",
        code="TCO",
        credit=3,
        teacher_id=1,
        department_id=1
    )
    test_course.save_to_db()
    return test_course


def create_test_student_course():
    test_student_course = StudentCourseScore(
        student_id=1,
        matric_no=f"STU-{year_str}-0001",
        course_id=1,
        course_code="TCO",
        credit=3,
        department_id=1
    )
    test_student_course.save_to_db()
    return test_student_course


def create_test_department():
    test_department = Department(
        name="Test Department",
        code="TD"
    )
    test_department.save_to_db()
    return test_department


def create_test_teacher():
    test_teacher = Teacher(
        type="teacher",
        title="MR",
        first_name="Teacher",
        last_name="Test",
        staff_code=f"TCH-{year_str}-0000",
        username="teacher.test",
        email="teacher@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_TEACHER_PASSWORD"]),
        department_id=1
    )
    test_teacher.save_to_db()
    return test_teacher


"""FUNCTION TO CREATE MULTIPLE RECORD DATA"""
def create_test_students():
    test_students = []
    
    test_student1 = Student(
        type="student",
        title="MR",
        first_name="Student1",
        last_name="Test",
        matric_no=f"STU-{year_str}-0001",
        username="student1.test",
        email="student1@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_STUDENT_PASSWORD"]),
        department_id=1
    )

    test_student2 = Student(
        type="student",
        title="MR",
        first_name="Student2",
        last_name="Test",
        matric_no=f"STU-{year_str}-0002",
        username="student2.test",
        email="student2@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_STUDENT_PASSWORD"]),
        department_id=1
    )

    test_student3 = Student(
        type="student",
        title="MR",
        first_name="Student3",
        last_name="Test",
        matric_no=f"STU-{year_str}-0003",
        username="student3.test",
        email="student3@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_STUDENT_PASSWORD"]),
        department_id=1
    )
    
    test_student1.save_to_db()
    test_student2.save_to_db()
    test_student3.save_to_db()

    test_students.append(test_student1)
    test_students.append(test_student2)
    test_students.append(test_student3)
    
    return test_students


def create_test_teachers():
    test_teachers = []
    
    test_teacher1 = Teacher(
        type="teacher",
        title="MR",
        first_name="Teacher1",
        last_name="Test",
        staff_code=f"TCH-{year_str}-0001",
        username="teacher1.test",
        email="teacher1@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_TEACHER_PASSWORD"]),
        department_id=1
    )

    test_teacher2 = Teacher(
        type="teacher",
        title="MR",
        first_name="Teacher2",
        last_name="Test",
        staff_code=f"TCH-{year_str}-0002",
        username="teacher2.test",
        email="teacher2@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_TEACHER_PASSWORD"]),
        department_id=1
    )

    test_teacher3 = Teacher(
        type="teacher",
        title="MR",
        first_name="Teacher3",
        last_name="Test",
        staff_code=f"TCH-{year_str}-0003",
        username="teacher3.test",
        email="teacher3@test.com",
        gender="MALE",
        password_hash=generate_password_hash(os.environ["DEFAULT_TEACHER_PASSWORD"]),
        department_id=1
    )
    
    test_teacher1.save_to_db()
    test_teacher2.save_to_db()
    test_teacher3.save_to_db()

    test_teachers.append(test_teacher1)
    test_teachers.append(test_teacher2)
    test_teachers.append(test_teacher3)
    
    return test_teachers


def create_test_students_records():
    test_students_records = []
    
    test_student_record1 = StudentRecord(
        student_id=1,
        matric_no=f"STU-{year_str}-0001",
        department_id=1,
        course_count=3,
        total_credits=9,
        total_points=33,
        gpa=367
    )

    test_student_record2 = StudentRecord(
        student_id=2,
        matric_no=f"STU-{year_str}-0002",
        department_id=1,
        course_count=3,
        total_credits=9,
        total_points=18,
        gpa=200
    )

    test_student_record3 = StudentRecord(
        student_id=3,
        matric_no=f"STU-{year_str}-0003",
        department_id=1,
        course_count=3,
        total_credits=9,
        total_points=27,
        gpa=300      
    )
    
    test_student_record1.save_to_db()
    test_student_record2.save_to_db()
    test_student_record3.save_to_db()

    test_students_records.append(test_student_record1)
    test_students_records.append(test_student_record2)
    test_students_records.append(test_student_record3)
    
    return test_students_records


def create_test_courses():
    test_courses = []
    
    test_course1 = Course(
        name="Test Course1",
        code="TC1",
        credit=2,
        teacher_id=1,
        department_id=1
    )

    test_course2 = Course(
        name="Test Course2",
        code="TC2",
        credit=3,
        teacher_id=2,
        department_id=1
    )

    test_course3 = Course(
        name="Test Course3",
        code="TC3",
        credit=4,
        teacher_id=3,
        department_id=1
    )

    test_course1.save_to_db()
    test_course2.save_to_db()
    test_course3.save_to_db()

    test_courses.append(test_course1)
    test_courses.append(test_course2)
    test_courses.append(test_course3)

    return test_courses

def create_test_student_courses():
    test_student_courses = []
    
    test_student_course1 = StudentCourseScore(
        student_id=1,
        matric_no=f"STU-{year_str}-0001",
        course_id=1,
        course_code="TC1",
        department_id=1,
        credit=2,
    )

    test_student_course2 = StudentCourseScore(
        student_id=1,
        matric_no=f"STU-{year_str}-0001",
        course_id=2,
        course_code="TC2",
        department_id=1,
        credit=3,
    )

    test_student_course3 = StudentCourseScore(
        student_id=1,
        matric_no=f"STU-{year_str}-0001",
        course_id=3,
        course_code="TC3",
        department_id=1,
        credit=4,
    )

    test_student_course1.save_to_db()
    test_student_course2.save_to_db()
    test_student_course3.save_to_db()
    
    test_student_courses.append(test_student_course1)
    test_student_courses.append(test_student_course2)
    test_student_courses.append(test_student_course3)
    
    return test_student_courses


def create_test_course_students_with_scores():
    test_course_students = []
    
    test_course_student1 = StudentCourseScore(
        course_id=1,
        course_code="TCO",
        department_id=1,
        credit=3,
        student_id=1,
        matric_no=f"STU-{year_str}-0001",
        score=80,
    )

    test_course_student2 = StudentCourseScore(
        course_id=1,
        course_code="TCO",
        department_id=1,
        credit=3,
        student_id=2,
        matric_no=f"STU-{year_str}-0002",
        score=75,
    )

    test_course_student3 = StudentCourseScore(
        course_id=1,
        course_code="TCO",
        department_id=1,
        credit=3,
        student_id=3,
        matric_no=f"STU-{year_str}-0003",
        score=65,
    )

    test_course_student1.save_to_db()
    test_course_student2.save_to_db()
    test_course_student3.save_to_db()
    
    test_course_students.append(test_course_student1)
    test_course_students.append(test_course_student2)
    test_course_students.append(test_course_student3)
    
    return test_course_students


