from . import UnitTestCase, create_test_admin, create_test_course, create_test_course_students, create_test_grade_scale, create_test_student_record, create_test_students, create_test_students_records, get_auth_token_headers, year_str
from ..models import Course, StudentCourseScore


class CourseTestCase(UnitTestCase):
    
    def test_create_get_all_course(self):
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

        response = self.client.get(
            "/courses/", 
            headers=get_auth_token_headers(test_admin.username))
        
        assert response.status_code == 200
        assert len(response.json) == 1


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
        assert StudentCourseScore.query.filter_by(course_id=1).count() == 3

        course_students = StudentCourseScore.query.filter_by(course_id=1).first()
        assert course_students.course_code == "TCO"


    def test_get_update_students_grades_for_course(self):
        test_admin = create_test_admin()
        test_course = create_test_course()
        test_students = create_test_students()
        test_grade_scale = create_test_grade_scale()
        test_course_students = create_test_course_students()
        test_students_records = create_test_students_records()

        course_id = test_course.id

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
            f"/courses/grades/{course_id}/students",
            json=update_data,
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert update_response.status_code == 200

        # get route
        get_response = self.client.get(
            f"/courses/grades/{course_id}/students",
            json=update_data,
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_response.status_code == 200
        # asserting saved data
        student1_grade = StudentCourseScore.query.filter_by(student_id=1, course_id=course_id).first()
        assert student1_grade.score == 80
        assert student1_grade.grade == "A"
        
        student2_grade = StudentCourseScore.query.filter_by(student_id=2, course_id=course_id).first()
        assert student2_grade.score == 65
        assert student2_grade.grade == "B"

        student3_grade = StudentCourseScore.query.filter_by(student_id=3, course_id=course_id).first()
        assert student3_grade.score == 75
        assert student3_grade.grade == "A"

