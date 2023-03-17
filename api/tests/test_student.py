from . import UnitTestCase, create_test_admin, create_test_course, create_test_courses, create_test_grade_scale, create_test_student_course, create_test_student_courses, create_test_student_record, create_test_students, create_test_user, create_test_student, get_auth_token_headers, year_str
from ..models import Course, StudentCourseScore, Student, StudentRecord
from ..utils.calc_func import calc_course_count, calc_scored_point, calc_total_credits, calc_student_gpa_honours, calc_total_points



class StudentTestCase(UnitTestCase):
    
    def test_get_all_students_or_current_student(self):
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
        user_response = self.client.get(
            "/students/", 
            headers=get_auth_token_headers(test_student.username)
        )
        assert user_response.status_code == 200
        # asserting saved data
        t_student = Student.query.filter_by(student_id=test_student.student_id).first()
        assert t_student.email == "student@test.com"


    def test_get_update_delete_student_by_id(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        student_id = test_student.student_id

        # get route 
        get_response = self.client.get(
            f"/students/{student_id}", 
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_response.status_code == 200

        stu = Student.get_by_student_id(student_id)
        assert stu.email == "student@test.com"
        assert stu.username == "student.test"
        
        # update route        
        update_data = {
            "first_name": "Stu1",
            "last_name": "Test1",
            "email": "stu3@test1.com"
        }

        update_response = self.client.put(
            f"/students/{student_id}", 
            json=update_data, 
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_response.status_code == 200
        
        update_stu = Student.get_by_student_id(student_id)
        assert update_stu.email == "stu3@test1.com"
        assert update_stu.first_name == "Stu1"
        assert update_stu.last_name == "Test1"

        # delete route
        delete_response = self.client.delete(
            f"/students/{student_id}",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert delete_response.status_code == 200
        
        delete_stu = Student.get_by_student_id(student_id)
        assert delete_stu == None        


    def test_register_unregister_multiple_student_courses(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_courses = create_test_courses()
        test_student_records = create_test_student_record()
        student_id = test_student.student_id

        reg_data = {
            "course1": 1, # 2 credits
            "course2": 2, # 3 credits
            "course3": 3, # 4 credits
        }
        
        # register route
        reg_response = self.client.post(
            f"/students/{student_id}/courses",
            json=reg_data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert reg_response.status_code == 201
        # asserting saved data
        assert StudentCourseScore.query.filter_by(student_id=student_id).count() == 3
        reg_stu_records = StudentRecord.query.filter_by(student_id=student_id).first()
        assert reg_stu_records.course_count == 3
        assert reg_stu_records.total_credits == 9
        
        # unregister route
        unreg_data = {
            "course1": 3, # 4 credits
        }
        
        unreg_response = self.client.delete(
            f"/students/{student_id}/courses",
            json=unreg_data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert unreg_response.status_code == 200
        # asserting saved data
        assert StudentCourseScore.query.filter_by(student_id=student_id).count() == 2
        unreg_stu_records = StudentRecord.query.filter_by(student_id=student_id).first()
        assert unreg_stu_records.course_count == 2
        assert unreg_stu_records.total_credits == 5
        

    def test_get_student_registered_courses(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_courses = create_test_student_courses()
        student_id = test_student.student_id

        # test_admin get route
        adm_response = self.client.get(
            f"/students/courses/{student_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 200
        # asserting saved data
        adm_count = StudentCourseScore.query.filter_by(student_id=student_id).count()
        assert adm_count == 3

        # test_student get route
        stu_response = self.client.get(
            f"/students/courses/student",
            headers=get_auth_token_headers(test_student.username)
        )        
        assert stu_response.status_code == 200

        
    def test_get_update_student_course_grade(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_record = create_test_student_record()
        test_course = create_test_course()
        test_grade_scale = create_test_grade_scale()
        test_student_course = create_test_student_course()
        
        student_id = test_student.student_id
        course_id = test_course.id  # 3 credits

        test_student_record.course_count = calc_course_count(student_id)
        test_student_record.total_credits = calc_total_credits(student_id)
        test_student_record.update_db()

        data = {
            "score": 80
        }
        
        # update route
        update_response = self.client.patch(
            f"/students/grades/{student_id}/course/{course_id}",
            json=data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_response.status_code == 200

        # get route
        get_response = self.client.get(
            f"/students/grades/{student_id}/course/{course_id}",
            headers=get_auth_token_headers(test_admin.username)
        )        
        assert get_response.status_code == 200
        # asserting saved data
        stu_records = StudentRecord.query.filter_by(student_id=student_id).first()
        assert stu_records.total_points == 12 # 3 credits * 4 points (Grade A)
        assert stu_records.gpa/100 == 4
        assert stu_records.honours == "First Class Honours"


    def test_get_update_courses_grades_for_student():
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_record = create_test_student_record()
        test_courses = create_test_courses()
        test_student_courses = create_test_student_courses()
        test_grade_scale = create_test_grade_scale()
        

    def test_get_current_or_specific_students_courses_grades(self):
        test_admin = create_test_admin()
        test_student = create_test_student()
        test_student_record = create_test_student_record()
        test_courses = create_test_courses()
        test_grade_scale = create_test_grade_scale()
        test_student_course = create_test_student_course()
        
        student_id = test_student.student_id

        test_student_record.course_count = calc_course_count(student_id)
        test_student_record.total_credits = calc_total_credits(student_id)
        test_student_record.update_db()

        # specific student by test_admin
        adm_response = self.client.get(
            f"/students/grades/{student_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_response.status_code == 201
        
        # current student user
        stu_response = self.client.get(
            "/students/grades/student",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert stu_response.status_code == 200
        

    # def get_student_records(self):
    #     pass


    # def get_all_students_records(self):
    #     pass
