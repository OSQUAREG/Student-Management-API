"""
To test only this file, run below command in terminal: 
pytest api/tests/test_departments.py -rA
"""

from . import UnitTestCase, create_test_admin, create_test_courses, create_test_department, create_test_students, create_test_teachers, create_test_super_admin, get_auth_token_headers
from ..models import Department, Student, Course, Teacher


class DepartmentTestCase(UnitTestCase):
    
    def testCreateGetDepartments(self):
        test_admin = create_test_admin()

        data = {
            "name": "Test Department",
            "code": "TD"
        }

        # testing post route
        get_response = self.client.post(
            "/departments/", 
            json=data, 
            headers=get_auth_token_headers(test_admin.username))
        # assert the route response status
        assert get_response.status_code == 201

        test_department = Department.query.filter_by(id=1).first()
        assert test_department.name == "Test Department"
        assert test_department.code == "TD"
        assert test_department.created_by == test_admin.username

        # testing get route
        get_response = self.client.get(
            "/departments/", 
            headers=get_auth_token_headers(test_admin.username)
        )
        # asserting response status
        assert get_response.status_code == 200
        # asserting saved data
        department = Department.get_by_id(1)
        assert department.name == "Test Department"
        assert department.code == "TD"


    def testGetUpdateDeleteDepartment(self):
        test_admin = create_test_admin()
        test_super_admin = create_test_super_admin()
        test_department = create_test_department()

        department_id = test_department.id
        department_code = test_department.code

        # testing get route
        get_response = self.client.get(
            f"/departments/{department_id}", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert get_response.status_code == 200
        # asserting saved data
        get_dept = Department.get_by_department_id_or_code(department_code)
        assert get_dept.name == "Test Department"
        assert get_dept.code == "TD"

        # testing get route
        update_data = {
            "name": "Test Department 1",
            "code": "TD1"
        }
        update_response = self.client.put(
            f"/departments/{department_code}", 
            json=update_data,
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert update_response.status_code == 200
        # asserting updated data
        update_dept = Department.get_by_department_id_or_code(department_id)
        assert update_dept.name == "Test Department 1"
        assert update_dept.code == "TD1"

        # testing delete route
        delete_response = self.client.delete(
            f"/departments/{department_id}", 
            headers=get_auth_token_headers(test_super_admin.username))
        # asserting response status
        assert delete_response.status_code == 200
        # asserting deleted data
        dept = Department.get_by_department_id_or_code(department_id)
        assert dept == None


    def testGetDepartmentStudents(self):
        test_admin = create_test_admin()
        test_department = create_test_department()
        test_students = create_test_students()

        department_id = test_department.id
        department_code = test_department.code

        # testing get route
        response_w_id = self.client.get(
            f"/departments/{department_id}/students", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert response_w_id.status_code == 200
        # asserting saved data
        student_w_dept_id = Student.get_by_department_id(department_id)
        assert len(student_w_dept_id) == 3

        response_w_code = self.client.get(
            f"/departments/{department_code}/students", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert response_w_code.status_code == 200
        # asserting saved data
        student_w_dept_id = Student.get_by_department_id(department_id)
        assert len(student_w_dept_id) == 3


    def testGetDepartmentCourses(self):
        test_admin = create_test_admin()
        test_department = create_test_department()
        test_courses = create_test_courses()

        department_id = test_department.id
        department_code = test_department.code

        # testing get route
        response_w_id = self.client.get(
            f"/departments/{department_id}/courses", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert response_w_id.status_code == 200
        # asserting saved data
        student_w_dept_id = Course.get_by_department_id(department_id)
        assert len(student_w_dept_id) == 3

        response_w_code = self.client.get(
            f"/departments/{department_id}/courses", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert response_w_code.status_code == 200
        # asserting saved data
        student_w_dept_code = Course.get_by_department_id(department_id)
        assert len(student_w_dept_code) == 3


    def GetDepartmentTeachers(self):
        test_admin = create_test_admin()
        test_department = create_test_department()
        test_teachers = create_test_teachers()

        department_id = test_department.id
        department_code = test_department.code

        # testing get route
        response_w_id = self.client.get(
            f"/departments/{department_id}/teachers", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert response_w_id.status_code == 200
        # asserting saved data
        teacher_w_dept_id = Teacher.get_by_department_id(department_id)
        assert len(teacher_w_dept_id) == 3

        response_w_code = self.client.get(
            f"/departments/{department_id}/teachers", 
            headers=get_auth_token_headers(test_admin.username))
        # asserting response status
        assert response_w_code.status_code == 200
        # asserting saved data
        teacher_w_dept_code = Teacher.get_by_department_id(department_id)
        assert len(teacher_w_dept_code) == 3