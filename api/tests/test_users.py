from . import UnitTestCase, create_test_admin, create_test_user, create_test_student, get_auth_token_headers, year_str
from ..models import Student, User, Teacher
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()


class UserTestCase(UnitTestCase):
    # testing the sign-up route
    def testUserRegister(self):
        test_admin=create_test_admin()

        # Student Test Data & Response
        stu_data = {
            "user_type": "STUDENT",
            "title": "MR",
            "first_name": "Student",
            "last_name": "Test",
            "email": "student@test.com",
            "gender": "MALE",
            "password": os.environ["DEFAULT_STUDENT_PASSWORD"],
            "department_id": 1
        }

        stu_response = self.client.post(
            "/auth/register", 
            json=stu_data, 
            headers=get_auth_token_headers(test_admin.username))

        # Teacher Test Data & Response
        tch_data = {
            "user_type": "TEACHER",
            "title": "MR",
            "first_name": "Teacher",
            "last_name": "Test",
            "email": "teacher@test.com",
            "gender": "MALE",
            "password": os.environ["DEFAULT_TEACHER_PASSWORD"],
            "department_id": 1
        }

        tch_response = self.client.post(
            "/auth/register", 
            json=tch_data, 
            headers=get_auth_token_headers(test_admin.username))

        print(os.environ["DEFAULT_STUDENT_PASSWORD"])
        
        # Asserting the route response status
        assert stu_response.status_code == 201
        assert tch_response.status_code == 201
        
        # Asserting the test data saved in users table
        user = User.query.filter_by(id=2).first()
        assert user.username == "student.test2"
        assert user.type == "student"

        # Asserting the test data saved in students table
        student = Student.query.filter_by(student_id=1).first()
        assert student.username == "student.test2"
        assert student.matric_no == f"STU-{year_str}-0001"
        assert student.email == "student@test.com"

        # Asserting the test data saved in teachers table DB
        teacher = Teacher.query.filter_by(teacher_id=1).first()
        assert teacher.username == "teacher.test3"
        assert teacher.staff_code == f"TCH-{year_str}-0001"
        assert teacher.email == "teacher@test.com"

        
    # testing the login route
    def testUserLogin(self):
        test_user = create_test_user()
        
        data = {
            "email": "student@test.com", 
            "password": os.environ["DEFAULT_STUDENT_PASSWORD"]
        }

        response = self.client.post("/auth/login", json=data)

        assert response.status_code == 201


    # testing the user password change
    def testUserChangePassword(self):
        test_user = create_test_user()        
        
        data = {
            "old_password": os.environ["DEFAULT_STUDENT_PASSWORD"], 
            "new_password": "password123",
            "confirm_password": "password123",
        }

        response = self.client.patch(
            "/auth/change-password", 
            json=data,
            headers=get_auth_token_headers(test_user.username)
        )

        assert response.status_code == 200
