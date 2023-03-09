from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .utils import db
from .config.config import config_dict
from .models import User, Teacher, Course, StudentCourse
from .auth.views import auth_namespace
from .student.views import student_namespace
from .teacher.views import teacher_namespace
from .admin.views import admin_namespace
from .course.views import course_namespace
from .blocklist import BLOCKLIST


def create_app(config=config_dict["dev"]):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(matric_no=identity).one_or_none()
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

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
        description="This is a student management API build with Flask RESTX API",
        version="1.0",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(admin_namespace, path="/admin")
    api.add_namespace(student_namespace, path="/students")
    api.add_namespace(course_namespace, path="/courses")
    api.add_namespace(teacher_namespace, path="/teachers")


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Student": User,
            "Teacher": Teacher,
            "Course": Course,
            "StudentCourse": StudentCourse,
        }

    return app
