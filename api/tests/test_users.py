from . import UnitTestCase
from ..models.models import Student


class UserTestCase(UnitTestCase):
    # testing the sign-up route
    def test_user_registration(self):

        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@test.com",
            "password": "password",
        }

        # to assert that username exist in the database
        student = Student.query.filter_by(email="testuser@test.com").first()
        assert student.email == "testuser@test.com"
        assert student.first_name == "Test"

        # assert the route response status
        response = self.client.post("/auth/register", json=data)
        assert response.status_code == 201

    # # testing the login route
    # def test_user_login(self):
    #     data = {"email": "testuser@test.com", "password": "password"}

    #     response = self.client.post("/auth/login", json=data)
    #     assert response.status_code == 200
