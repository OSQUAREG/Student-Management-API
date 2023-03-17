from . import UnitTestCase, create_test_admin, create_test_course, create_test_course_students, get_auth_token_headers, year_str
from ..models import Course, StudentCourseScore


class CourseTestCase(UnitTestCase):
    
    def test_create_course(self):
        test_admin = create_test_admin()

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
            headers=get_auth_token_headers(test_admin.username))

        # assert the route response status
        assert response.status_code == 201
        # asserting the data saved
        course = Course.query.filter_by(id=1).first()
        assert course.name == "Test Course"
        assert course.code == "TCO"
        assert course.credit == 3
        assert course.created_by == test_admin.username

    
    def test_gel_all_courses(self):
        test_admin = create_test_admin()
        
        response = self.client.get(
            "/courses/", 
            headers=get_auth_token_headers(test_admin.username))
        
        assert response.status_code == 200
        assert response.json == []


    def test_get_all_course_students(self):
        test_admin = create_test_admin()
        test_course = create_test_course()
        test_course_students = create_test_course_students()

        course_id = test_course.id

        response = self.client.get(
            f"/courses/{course_id}/students", 
            headers=get_auth_token_headers(test_admin.username))
        
        # asserting the response status code
        assert response.status_code == 200
        # asserting the count of students for the course
        assert StudentCourseScore.query.filter_by(course_id=1).count() == 2

        course_students = StudentCourseScore.query.filter_by(course_id=1).first()
        assert course_students.course_code == "TCO"
