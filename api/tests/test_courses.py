"""
To test only this file, run below command in terminal: 
pytest api/tests/test_courses.py -rA
"""

from api.models.grading import StudentRecord
from . import UnitTestCase, create_test_admin, create_test_course, create_test_course_students_with_scores, create_test_grade_scale, create_test_student_record, create_test_students, create_test_students_records, get_auth_token_headers, year_str
from ..models import Course, StudentCourseScore


class CourseTestCase(UnitTestCase):
    
    def testCreateGetAllCourses(self):
        test_admin = create_test_admin()

        data = {
            "name": "Test Course",
            "code": "TCO",
            "credit": 3,
            "teacher_id": 1,
            "department_id": 1,
        }

        post_response = self.client.post(
            "/courses/", 
            json=data, 
            headers=get_auth_token_headers(test_admin.username))

        # assert the route response status
        assert post_response.status_code == 201
        # asserting the data saved
        post_course = Course.get_by_id(1)
        assert post_course.name == "Test Course"
        assert post_course.code == "TCO"
        assert post_course.credit == 3

        get_response = self.client.get(
            "/courses/", 
            headers=get_auth_token_headers(test_admin.username))
        
        assert get_response.status_code == 200
        get_course = Course.get_by_id(1)
        assert get_course.name == "Test Course"
        assert get_course.code == "TCO"


    def testGetUpdateDeleteCourse(self):
        test_admin = create_test_admin()
        test_course = create_test_course()

        course_id = test_course.id
        course_code = test_course.code

        # testing get route
        get_response = self.client.get(
            f"/courses/{course_id}",
            headers=get_auth_token_headers(test_admin.username))
        assert get_response.status_code == 200
        # asseting saved data
        get_course = Course.get_by_course_id_or_code(course_code)
        assert get_course.code == "TCO"
        assert get_course.name == "Test Course"

        # testing update route
        update_data = {
            "name": "Test Course 1",
            "code": "TCO1",
            "credit": 4,
        }
        update_response = self.client.put(
            f"/courses/{course_code}",
            json=update_data,
            headers=get_auth_token_headers(test_admin.username))
        assert update_response.status_code == 200
        # asseting updated data
        update_course = Course.get_by_course_id_or_code(course_id)
        assert update_course.name == "Test Course 1"
        assert update_course.code == "TCO1"
        assert update_course.credit == 4

        # testing delete route
        delete_response = self.client.delete(
            f"/courses/{course_id}",
            headers=get_auth_token_headers(test_admin.username))
        assert delete_response.status_code == 200
        # asseting updated data
        del_course = Course.get_by_course_id_or_code(course_id)
        assert del_course == None


    def testGetCourseStudents(self):
        test_admin = create_test_admin()
        test_course = create_test_course()
        test_course_students = create_test_course_students_with_scores()

        course_id = test_course.id
        course_code = test_course.code

        response_w_id = self.client.get(
            f"/course/students/{course_id}", 
            headers=get_auth_token_headers(test_admin.username))
        
        # asserting the response status code
        assert response_w_id.status_code == 200

        response_w_code = self.client.get(
            f"/course/students/{course_code}", 
            headers=get_auth_token_headers(test_admin.username))
        
        # asserting the response status code
        assert response_w_code.status_code == 200
        
        # asserting saved data
        course_students = StudentCourseScore.get_students_by_course_id_or_code(1)
        assert len(course_students) == 3
        for stu in course_students:
            assert stu.course_code == "TCO"


    def testGetUpdateCourseStudentsGrades(self):
        test_admin = create_test_admin()
        test_course = create_test_course()
        test_students = create_test_students()
        test_grade_scale = create_test_grade_scale()
        test_course_students = create_test_course_students_with_scores()
        test_students_records = create_test_students_records()

        course_id = test_course.id
        course_code = test_course.code

        # update route
        update_data = {
            "student1_id": 1,
            "score1": 80,
            "student2_id": 2,
            "score2": 65,
            "student3_id": 3,
            "score3": 75,
        }
        update_response = self.client.patch(
            f"/course/students/grades/{course_id}",
            json=update_data,
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert update_response.status_code == 200

        # get route
        get_response = self.client.get(
            f"/course/students/grades/{course_code}",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_response.status_code == 200
        # asserting saved data
        student1_grade = StudentCourseScore.get_student_course_by_id_or_code(1, course_id)
        assert student1_grade.score == 80
        assert student1_grade.grade == "A"
        
        student2_grade = StudentCourseScore.get_student_course_by_id_or_code(2, course_id)
        assert student2_grade.score == 65
        assert student2_grade.grade == "B"

        student3_grade = StudentCourseScore.get_student_course_by_id_or_code(3, course_id)
        assert student3_grade.score == 75
        assert student3_grade.grade == "A"

