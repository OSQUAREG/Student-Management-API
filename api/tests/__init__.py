from datetime import datetime
import unittest
from flask import current_app
from flask_jwt_extended import create_access_token

from api.models.users import Student
from ..models import User
from .. import create_app
from ..config.config import config_dict
from ..utils import db


def get_auth_token_headers(identity):
    token = create_access_token(identity=identity)
    headers = {"Authorization": f"Bearer {token}"}
    return headers

year_str = str(datetime.utcnow().year)[-3:]


class UnitTestCase(unittest.TestCase):
    # called before each test
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        # using a test client
        self.client = self.app.test_client()
        db.create_all()

    # called after each test case
    def tearDown(self):
        db.drop_all
        self.app_ctxt.pop()
        self.app = None
        self.client = None


def create_test_admin():
    admin = User(
        first_name="Admin",
        last_name="Test",
        gender="MALE",
        email="admin@test.com",
        username="admin.test",
        password_hash="admin@password",
        is_staff=True,
        is_admin=True,
    )

    admin.save_to_db()
    return admin
