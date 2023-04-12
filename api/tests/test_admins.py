"""
To test only this file, run below command in terminal: 
pytest api/tests/test_admins.py -rA
"""

from . import (
    UnitTestCase,
    create_test_admin,
    create_test_courses,
    create_test_department,
    create_test_students,
    create_test_teachers,
    create_test_super_admin,
    get_auth_token_headers,
)
from ..models import Admins
import os


class AdminTestCase(UnitTestCase):
    
    def testCreateGetAllAdmins(self):
        test_admin = create_test_admin()

        data = {
            "first_name": "Admin1",
            "last_name": "Test",
            "email": "admin1@test.com",
            "gender": "MALE",
            "password": os.environ["DEFAULT_ADMIN_PASSWORD"]
        }

        # testing post route
        post_response = self.client.post(
            "/admin/",
            json=data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert post_response.status_code == 201
        # asserting created data
        new_adm = Admins.get_by_admin_id_or_code(2)
        assert new_adm.first_name == "Admin1"
        assert new_adm.email == "admin1@test.com"
        assert new_adm.username == "admin1.test2"
        assert new_adm.admin_code == "ADM-admin1.test2"

        # testing get route
        get_response = self.client.get(
            "/admin/",
            headers=get_auth_token_headers(test_admin.username)
        )
        # assert get_response.status_code == 200
        adms = Admins.get_all()
        assert len(adms) == 2
        

    def testGetUpdateDeleteAdminByID(self):
        test_admin = create_test_admin()
        test_super_admin = create_test_super_admin()

        admin_id = test_admin.admin_id

        # testing get route
        get_response = self.client.get(
            f"/admin/{admin_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert get_response.status_code == 200
        

        # testing update route
        update_data = {
            "first_name": "Admin1",
            "email": "admin1@test.com"
        }
        
        update_response = self.client.put(
            f"/admin/{admin_id}",
            json=update_data,
            headers=get_auth_token_headers(test_admin.username)
        )
        assert update_response.status_code == 200
        # asserting updated data
        adm = Admins.get_by_admin_id_or_code(admin_id)
        assert adm.first_name == "Admin1"
        assert adm.email == "admin1@test.com"
        assert adm.admin_code == "ADM-admin1.test1"

        # asserting data deleted
        adm_delete_response = self.client.delete(
            f"/admin/{admin_id}",
            headers=get_auth_token_headers(test_admin.username)
        )
        assert adm_delete_response.status_code == 401

        # asserting data deleted
        sup_adm_delete_response = self.client.delete(
            f"/admin/{admin_id}",
            headers=get_auth_token_headers(test_super_admin.username)
        )
        assert sup_adm_delete_response.status_code == 200
        # asserting saved data
        del_adm = Admins.get_by_admin_id_or_code(admin_id)
        assert del_adm == None
