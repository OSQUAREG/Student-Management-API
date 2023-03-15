from . import UnitTestCase, create_test_admin, get_auth_token_headers
from ..models import Department


class DepartmentTestCase(UnitTestCase):
    
    def test_create_department(self):
        admin = create_test_admin()

        data = {
            "name": "Department of Test",
            "code": "DOT"
        }

        response = self.client.post(
            "/departments/", 
            json=data, 
            headers=get_auth_token_headers(admin.username))

        # assert the route response status
        assert response.status_code == 201

        department = Department.query.filter_by(id=1).first()
        assert department.name == "Department of Test"
        assert department.code == "DOT"
        assert department.created_by == admin.username

    
    def test_gel_all_departments(self):
        admin = create_test_admin()
        
        response = self.client.get(
            "/departments/", 
            headers=get_auth_token_headers(admin.username))

        assert response.status_code == 200
        assert response.json == []