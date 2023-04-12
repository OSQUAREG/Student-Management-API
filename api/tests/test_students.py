"""
To test only this file, run below command in terminal: 
pytest api/tests/test_students.py -rA
"""

from . import (
    UnitTestCase,
    create_test_students_records, 
    create_test_admin, 
    create_test_course, 
    create_test_courses, 
    create_test_grade_scale, 
    create_test_student_course, 
    create_test_student_courses, 
    create_test_student_record, 
    create_test_students, 
    create_test_student, 
    get_auth_token_headers,
)
from ..models import StudentCourseScore, Student, StudentRecord


class StudentTestCase(UnitTestCase):
    
    def testGetCurrentAllStudents(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_students = create_test_students()
        # test_admin get all route
        admin_response = self.client.get(
            "/students/", 
            headers=get_auth_token_headers(test_admin.username)
        )
        assert admin_response.status_code == 200
        # asserting saved data
        student = Student.query.filter_by(email="student@test.com").first()
        assert student.first_name == "Student"

        student1 = Student.query.filter_by(email="student1@test.com").first()
        assert student1.first_name == "Student1"

        # current student get route
        stu_response = self.client.get(
            "/student/", 
            headers=get_auth_token_headers(test_student.username)
        )
        assert stu_response.status_code == 200
        # asserting saved data
        stu = Student.get_by_student_id_or_matric(test_student.student_id)
        assert stu.email == "student@test.com"


    def testGetUpdateDeleteSpecificStudent(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        
        student_id = test_student.student_id
        student_matric = test_student.matric_no

        # get with id route
        get_by_id_response = self.client.get(
            f"/students/{student_id}", 
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_by_id_response.status_code == 200

        stu_by_id = Student.get_by_student_id_or_matric(student_id)
        assert stu_by_id.email == "student@test.com"
        assert stu_by_id.username == "student.test"

        # get with matric route
        get_by_matric_response = self.client.get(
            f"/students/{student_matric}", 
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_by_matric_response.status_code == 200

        stu_by_matric = Student.get_by_student_id_or_matric(student_matric)
        assert stu_by_matric.email == "student@test.com"
        assert stu_by_matric.username == "student.test"
        
        # update with id route        
        update_data = {
            "first_name": "Stu1",
            "last_name": "Test1",
            "email": "stu3@test1.com"
        }

        update_by_id_response = self.client.put(
            f"/students/{student_id}", 
            json=update_data, 
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_by_id_response.status_code == 200
        
        update_stu_by_id = Student.get_by_student_id_or_matric(student_id)
        assert update_stu_by_id.email == "stu3@test1.com"
        assert update_stu_by_id.first_name == "Stu1"
        assert update_stu_by_id.last_name == "Test1"

        # update with matric route        
        update_data = {
            "first_name": "Stu1",
            "last_name": "Test1",
            "email": "stu3@test1.com"
        }

        update_by_matric_response = self.client.put(
            f"/students/{student_matric}", 
            json=update_data, 
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_by_matric_response.status_code == 200
        
        update_stu_by_matric = Student.get_by_student_id_or_matric(student_matric)
        assert update_stu_by_matric.email == "stu3@test1.com"
        assert update_stu_by_matric.first_name == "Stu1"
        assert update_stu_by_matric.last_name == "Test1"

        # delete route
        delete_response = self.client.delete(
            f"/students/{student_id}",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert delete_response.status_code == 200
        
        delete_stu = Student.get_by_student_id_or_matric(student_id)
        assert delete_stu == None        


    def testRegisterUnregisterStudentCourses(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_courses = create_test_courses()
        test_student_records = create_test_student_record()
        
        student_id = test_student.student_id
        student_matric = test_student.matric_no

        reg_data = {
            "course1": 1, # 2 credits
            "course2": "TC2", # 3 credits
            "course3": 3, # 4 credits
        }
        
        # register route
        reg_response = self.client.post(
            f"/students/courses/{student_id}",
            json=reg_data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert reg_response.status_code == 201
        # asserting saved data
        assert len(StudentCourseScore.get_courses_by_student_id_or_matric(student_id)) == 3
        reg_stu_records = StudentRecord.get_by_student_id_or_matric(student_id)
        assert reg_stu_records.course_count == 3
        assert reg_stu_records.total_credits == 9
        
        # unregister route
        unreg_data = {
            "course1": 3, # 4 credits
            "course2": "TC2", # 3 credits
        }
        
        unreg_response = self.client.delete(
            f"/students/courses/{student_matric}",
            json=unreg_data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert unreg_response.status_code == 200
        # asserting saved data
        assert len(StudentCourseScore.get_courses_by_student_id_or_matric(student_matric)) == 1
        unreg_stu_records = StudentRecord.get_by_student_id_or_matric(student_matric)
        assert unreg_stu_records.course_count == 1
        assert unreg_stu_records.total_credits == 2


    def testGetStudentRegisteredCourses(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_courses = create_test_student_courses()
        
        student_id = test_student.student_id
        student_matric = test_student.matric_no

        # test_admin: get with id route
        get_by_id_response = self.client.get(
            f"/students/courses/{student_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert get_by_id_response.status_code == 200
        # asserting saved data
        stu_by_id_count = StudentCourseScore.query.filter_by(student_id=student_id).count()
        assert stu_by_id_count == 3

        # test_admin: get with matric route
        get_by_matric_response = self.client.get(
            f"/students/courses/{student_matric}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert get_by_matric_response.status_code == 200
        # asserting saved data
        stu_by_matric_count = StudentCourseScore.query.filter_by(student_id=student_id).count()
        assert stu_by_matric_count == 3

        # test_student: get route
        stu_response = self.client.get(
            f"/student/courses",
            headers=get_auth_token_headers(test_student.username)
        )        
        assert stu_response.status_code == 200


    def testGetUpdateSingleStudentCourseGrade(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_record = create_test_student_record()
        test_course = create_test_course()
        test_grade_scale = create_test_grade_scale()
        test_student_course = create_test_student_course()
        
        student_id = test_student.student_id
        student_matric = test_student.matric_no
        course_id = test_course.id  # 3 credits
        course_code = test_course.code  # 3 credits

        test_student_record.calc_course_count_credits()
        test_student_record.update_db()

        data = {
            "score": 80
        }
        
        # update with id route
        update_by_id_response = self.client.patch(
            f"/students/grades/student/{student_id}/course/{course_id}",
            json=data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_by_id_response.status_code == 200

        # update with matric/code route
        update_by_code_response = self.client.patch(
            f"/students/grades/student/{student_matric}/course/{course_code}",
            json=data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_by_code_response.status_code == 200

        # get with id route
        get_by_id_response = self.client.get(
            f"/students/grades/student/{student_id}/course/{course_id}",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_by_id_response.status_code == 200

        # asserting saved data with code
        stu_by_id_records = StudentRecord.get_by_student_id_or_matric(student_id)
        assert stu_by_id_records.total_points == 12 # 3 credits * 4 points (Grade A)
        assert stu_by_id_records.gpa/100 == 4
        assert stu_by_id_records.honours == "First Class Honours"

        # get with code route
        get_by_code_response = self.client.get(
            f"/students/grades/student/{student_matric}/course/{course_code}",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_by_code_response.status_code == 200
        
        # asserting saved data with id
        stu_by_code_records = StudentRecord.get_by_student_id_or_matric(student_id)
        assert stu_by_code_records.total_points == 12 # 3 credits * 4 points (Grade A)
        assert stu_by_code_records.gpa/100 == 4
        assert stu_by_code_records.honours == "First Class Honours"


    def testGetUpdateCourseStudentsGrades(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_grade_scale = create_test_grade_scale()
        test_student_record = create_test_student_record()
        test_courses = create_test_courses()
        test_student_courses = create_test_student_courses()
        
        student_id = test_student.student_id
        student_matric = test_student.matric_no

        test_student_record.calc_points_gpa_honours()
        test_student_record.update_db()

        data = {
            "course1_id": 1,
            "score1": 80,
            "course2_id": "TC2",
            "score2": 65,
            "course3_id": 3,
            "score3": 75,
        }
        # update with id route
        update_by_id_response = self.client.patch(
            f"/students/grades/{student_id}/courses",
            json=data,
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert update_by_id_response.status_code == 200

        # update with matric route
        update_by_matric_response = self.client.patch(
            f"/students/grades/{student_matric}/courses",
            json=data,
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert update_by_matric_response.status_code == 200

        # get with id route
        get_by_id_response = self.client.get(
            f"/students/grades/{student_id}/courses",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_by_id_response.status_code == 200

        # get with matric route
        get_by_matric_response = self.client.get(
            f"/students/grades/{student_matric}/courses",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_by_matric_response.status_code == 200
        
        # asserting saved data
        course1_grade = StudentCourseScore.get_student_course_by_id_or_code(student_id, "TC1")
        assert course1_grade.score == 80
        assert course1_grade.grade == "A"
        
        course2_grade = StudentCourseScore.get_student_course_by_id_or_code(student_id, 2)
        assert course2_grade.score == 65
        assert course2_grade.grade == "B"

        course3_grade = StudentCourseScore.get_student_course_by_id_or_code(student_id, "TC3")
        assert course3_grade.score == 75
        assert course3_grade.grade == "A"


    def testGetCurrentStudentCoursesGrades(self):
        # test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_record = create_test_student_record()
        test_courses = create_test_courses()
        test_grade_scale = create_test_grade_scale()
        # test_student_course = create_test_student_courses()

        test_student_record.calc_course_count_credits()
        test_student_record.update_db()
        
        # current student user
        stu_response = self.client.get(
            "/student/grades",
            headers=get_auth_token_headers(test_student.username)
        )
        assert stu_response.status_code == 200
        

    def testGetSpecificStudentRecords(self):
        test_admin = create_test_admin()        
        test_student = create_test_student()
        test_student_record = create_test_student_record()

        student_id = test_student.student_id

        test_student_record.calc_points_gpa_honours()

        # current student record
        stu_response = self.client.get(
            "/student/records",
            headers=get_auth_token_headers(test_student.username)
        )
        assert stu_response.status_code == 200

        # admin get spcific student record
        adm_response = self.client.get(
            f"/students/records/{student_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 200


    def testGetUpdateAllStudentGradesRecords(self):
        test_admin = create_test_admin()        
        test_students = create_test_students()
        test_students_records = create_test_students_records()

        # testing get route
        get_response = self.client.get(
            "/students/records/",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert get_response.status_code == 200

        # testing update route
        update_response = self.client.put(
            "/students/records/",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_response.status_code == 200
