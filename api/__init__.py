from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .utils import db
from .config.config import config_dict
from .models import (
    User,
    Student,
    Teacher,
    Course,
    StudentCourseScore,
    Department,
    GradeScale,
    StudentRecord,
)
from .auth.views import auth_namespace
from .student.views import student_namespace
from .teacher.views import teacher_namespace
from .admin.views import admin_namespace
from .course.views import course_namespace
from .department.views import department_namespace
from .blocklist import BLOCKLIST
from werkzeug.exceptions import NotFound, MethodNotAllowed, Unauthorized
from flask_jwt_extended.exceptions import NoAuthorizationError
from .create_defaults import create_defaults


def create_app(config=config_dict["dev"]):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with: <Bearer {JWT token}> to authorize.",
        }
    }

    api = Api(
        app=app,
        title="Student Management API",
        description="This is a Student Management API (SM-API) build with Flask RESTX in Python",
        version="1.0",
        authorizations=authorizations,
        security="Bearer Auth",
        errors=Flask.errorhandler,
    )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(department_namespace, path="/departments")
    api.add_namespace(student_namespace, path="/students")
    api.add_namespace(course_namespace, path="/courses")
    api.add_namespace(teacher_namespace, path="/teachers")
    api.add_namespace(admin_namespace, path="/admin")

    # error handlers
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 405

    @api.errorhandler(Unauthorized)
    def unauthorized(error):
        return {"error": "Not Unauthorized"}, 401

    # I added this error handler becuase before deployment, 
    # when you send request without first adding authorization header,
    # it returns a 401 Unauthorized error.
    # But after deployment, it returns 500 Internal Server Error, 
    # and I need it to return a 401 error
    @api.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(error):
        return {"error": "Missing Authorization Header"}, 401
    

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Student": Student,
            "Teacher": Teacher,
            "Course": Course,
            "GradeScale": GradeScale,
            "StudentCourse": StudentCourseScore,
            "StudentCourse": StudentRecord,
            "Department": Department,
            "create_defaults": create_defaults
        }

    return app
