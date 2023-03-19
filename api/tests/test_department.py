from . import UnitTestCase, create_test_admin, get_auth_token_headers
from ..models import Department


class DepartmentTestCase(UnitTestCase):
    
    def test_create_department(self):
        test_admin = create_test_admin()

        data = {
            "name": "Department of Test",
            "code": "DOT"
        }

        response = self.client.post(
            "/departments/", 
            json=data, 
            headers=get_auth_token_headers(test_admin.username))

        # assert the route response status
        assert response.status_code == 201

        test_department = Department.query.filter_by(id=1).first()
        assert test_department.name == "Department of Test"
        assert test_department.code == "DOT"
        assert test_department.created_by == test_admin.username

    
    def test_gel_all_departments(self):
        test_admin = create_test_admin()
        
        response = self.client.get(
            "/departments/", 
            headers=get_auth_token_headers(test_admin.username)
        )

        assert response.status_code == 200
        assert response.json == []