"""
To test only this file, run below command in terminal: 
pytest api/tests/test_teachers.py -rA
"""

from . import (
    UnitTestCase,
    create_test_course,
    create_test_course_students_with_scores,
    year_str,
    create_test_admin,
    create_test_courses,
    create_test_department,
    create_test_students,
    create_test_teacher,
    create_test_teachers,
    create_test_super_admin,
    get_auth_token_headers,
)
from ..models import Department, Student, Course, Teacher, StudentCourseScore


class TeacherTestCase(UnitTestCase):
    
    def testGetCurrentAllTeachers(self):
        test_admin = create_test_admin()
        test_teacher = create_test_teacher()
        test_teachers = create_test_teachers()
        # test_admin get all route
        adm_response = self.client.get(
            "/teachers/", headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 200
        # asserting saved data
        teacher = Teacher.query.filter_by(email="teacher@test.com").first()
        assert teacher.first_name == "Teacher"

        teacher1 = Teacher.query.filter_by(email="teacher1@test.com").first()
        assert teacher1.first_name == "Teacher1"

        # current student get route
        tch_response = self.client.get(
            "/teachers/", headers=get_auth_token_headers(test_teacher.username)
        )
        assert tch_response.status_code == 200
        # asserting saved data
        tch = Teacher.get_by_teacher_id_or_code(test_teacher.teacher_id)
        assert tch.email == "teacher@test.com"

    def testGetUpdateDeleteTeacher(self):
        test_admin = create_test_admin()
        test_teacher = create_test_teacher()

        teacher_id = test_teacher.teacher_id
        teacher_code = test_teacher.staff_code

        get_response = self.client.get(
            f"/teachers/{teacher_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert get_response.status_code == 200
        # asserting saved data
        get_teacher = Teacher.get_by_teacher_id_or_code(teacher_code)
        assert get_teacher.first_name == "Teacher"
        assert get_teacher.staff_code == f"TCH-{year_str}-0000"

        # testing update route
        update_data = {
            "first_name": "Tch1",
            "last_name": "Test1",
            "email": "tch3@test1.com"
        }

        update_reponse = self.client.put(
            f"/teachers/{teacher_code}",
            json=update_data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_reponse.status_code == 200
        # asserting updated data
        update_teacher = Teacher.get_by_teacher_id_or_code(teacher_id)
        assert update_teacher.first_name == "Tch1"
        assert update_teacher.email == "tch3@test1.com"

        # asserting delete route
        delete_response = self.client.delete(
            f"/teachers/{teacher_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert delete_response.status_code == 200
        # asserting saved data
        get_teacher = Teacher.get_by_teacher_id_or_code(teacher_id)
        assert get_teacher == None


    def testGetTeacherStudents(self):
        test_admin = create_test_admin()
        test_teacher = create_test_teacher()
        test_course = create_test_course()
        test_course_students = create_test_course_students_with_scores()

        teacher_id = test_teacher.teacher_id
        teacher_code = test_teacher.staff_code

        # testing get response (admin)
        adm_response = self.client.get(
            f"/teachers/{teacher_code}/students",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 200
        # asserting saved data
        course = Course.get_one_by_teacher_id(teacher_id)
        students = StudentCourseScore.get_students_by_course_id_or_code(course.id)
        assert len(students) == 3

        # testing get response (current teacher)
        tch_response = self.client.get(
            f"/teacher/students",
            headers=get_auth_token_headers(test_teacher.username)
        )
        assert tch_response.status_code == 200
        # asserting saved data
        course = Course.get_one_by_teacher_id(teacher_id)
        students = StudentCourseScore.get_students_by_course_id_or_code(course.id)
        assert len(students) == 3


    def testGetTeacherCourses(self):
        test_admin = create_test_admin()
        test_teacher = create_test_teacher()
        test_course = create_test_course()

        teacher_id = test_teacher.teacher_id
        teacher_code = test_teacher.staff_code

        # testing get response (admin)
        adm_response = self.client.get(
            f"/teachers/{teacher_code}/courses",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 200
        # asserting saved data
        adm_course = Course.get_all_by_teacher_id(teacher_id)
        assert len(adm_course) == 1

        # testing get response (current teacher)
        tch_response = self.client.get(
            f"/teacher/courses",
            headers=get_auth_token_headers(test_teacher.username)
        )
        assert tch_response.status_code == 200
        # asserting saved data
        tch_course = Course.get_all_by_teacher_id(teacher_id)
        assert len(tch_course) == 1


    def testGetTeacherStudentsGrades(self):
        test_admin = create_test_admin()
        test_teacher = create_test_teacher()
        test_course = create_test_course()
        test_course_students = create_test_course_students_with_scores()

        teacher_id = test_teacher.teacher_id
        teacher_code = test_teacher.staff_code

        course_id = test_course.id
        course_code = test_course.code

        # testing get route (admin)
        adm_response = self.client.get(
            f"/teachers/{teacher_id}/students/grades/{course_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 200
        # asserting saved data
        adm_tch_course = Course.get_one_by_teacher_id(teacher_id)
        adm_stu_course = StudentCourseScore.get_students_by_course_id_or_code(adm_tch_course.id)
        assert len(adm_stu_course) == 3

        # testing get route (current teacher)
        tch_response = self.client.get(
            f"/teacher/students/grades/{course_id}",
            headers=get_auth_token_headers(test_teacher.username)
        )
        assert tch_response.status_code == 200
        # asserting saved data
        teacher_course = Course.get_one_by_teacher_id(teacher_id)
        stu_course = StudentCourseScore.get_students_by_course_id_or_code(teacher_course.id)
        assert len(stu_course) == 3