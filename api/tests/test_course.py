from . import UnitTestCase, create_test_admin, get_auth_token_headers, year_str
from ..models import Course, StudentCourseScore


class CourseTestCase(UnitTestCase):
    
    def test_create_course(self):
        admin = create_test_admin()

        data = {
            "name": "Test Course",
            "code": "TCO",
            "credit": 3,
            "teacher_id": 1,
            "department_id": 1,
        }

        response = self.client.post(
            "/courses/", 
            json=data, 
            headers=get_auth_token_headers(admin.username))

        # assert the route response status
        assert response.status_code == 201
        # asserting the data saved
        course = Course.query.filter_by(id=1).first()
        assert course.name == "Test Course"
        assert course.code == "TCO"
        assert course.credit == 3
        assert course.teacher_id == 1
        assert course.department_id == 1
        assert course.created_by == admin.username

    
    def test_gel_all_courses(self):
        admin = create_test_admin()
        
        response = self.client.get(
            "/courses/", 
            headers=get_auth_token_headers(admin.username))
        
        assert response.status_code == 200
        assert response.json == []


    def test_get_all_course_students(self):
        admin = create_test_admin()

        course = Course(
            name="Test Course",
            code="TCO",
            credit=3,
            teacher_id=1,
            department_id=1
        )

        course_student1 = StudentCourseScore(
            student_id=1,
            matric_no=f"STU/{year_str}/0001",
            course_id=1,
            course_code="TCO",
            department_id=1,
            credit=3,
        )

        course_student2 = StudentCourseScore(
            student_id=2,
            matric_no=f"STU/{year_str}/0002",
            course_id=1,
            course_code="TCO",
            department_id=1,
            credit=3,
        )

        course_student3 = StudentCourseScore(
            student_id=3,
            matric_no=f"STU/{year_str}/0003",
            course_id=2,
            course_code="TCO",
            department_id=1,
            credit=3,
        )

        course.save_to_db()
        course_student1.save_to_db()
        course_student2.save_to_db()
        course_student3.save_to_db()

        course_id = course.id

        response = self.client.get(
            f"/courses/{course_id}/students", 
            headers=get_auth_token_headers(admin.username))
        
        # asserting the response status code
        assert response.status_code == 200
        # asserting the count of students for the course
        assert StudentCourseScore.query.filter_by(course_id=1).count() == 2

        course_students = StudentCourseScore.query.filter_by(course_id=1).first()
        assert course_students.course_code == "TCO"
        
        