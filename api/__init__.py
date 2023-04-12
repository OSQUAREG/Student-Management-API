from http import HTTPStatus
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from api.admin_setup.views import MyAdminIndexView, MyModelView
from .utils import db
from .config.config import config_dict
from .models import (
    User,
    Admins,
    Student,
    Teacher,
    Course,
    StudentCourseScore,
    Department,
    GradeScale,
    StudentRecord,
)
from .auth.views import auth_namespace
from .student.views import student_namespace, adm_student_namespace, student_courses_namespace, student_grades_namespace, student_records_namespace
from .teacher.views import teacher_namespace, adm_teacher_namespace
from .admin.views import admin_namespace
from .course.views import course_namespace, course_student_namespace
from .department.views import department_namespace
from .blocklist import BLOCKLIST
from werkzeug.exceptions import NotFound, MethodNotAllowed, Unauthorized
from flask_jwt_extended.exceptions import NoAuthorizationError
from .create_defaults import create_defaults
from flask_login import LoginManager


def create_app(config=config_dict["dev"]):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    # Initialize flask-admin
    app.config["FLASK_ADMIN_SWATCH"] = "united"
    admin = Admin(app, name='Admin: SM-API', template_mode='bootstrap3', index_view=MyAdminIndexView(), base_template="my_master.html")

    admin.add_view(MyModelView(Department, db.session))
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Admins, db.session))
    admin.add_view(MyModelView(Student, db.session))
    admin.add_view(MyModelView(Teacher, db.session))
    admin.add_view(MyModelView(Course, db.session))
    admin.add_view(MyModelView(GradeScale, db.session))
    admin.add_view(MyModelView(StudentCourseScore, db.session))
    admin.add_view(MyModelView(StudentRecord, db.session))
    # admin.add_view(MyModelView(LogOut, db.session))

    # Initialize flask-migrate
    migrate = Migrate(app, db)

    # Initialize flask-jwt
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # Initialize flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return HTTPStatus.UNAUTHORIZED
        return db.session.query(User).get(user_id)

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
        title="Student Management API (SM-API)",
        description="This is a Student Management API (SM-API) build with Flask RESTX in Python",
        version="1.0",
        authorizations=authorizations,
        security="Bearer Auth",
        errors=Flask.errorhandler,
    )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(admin_namespace, path="/admin")
    api.add_namespace(department_namespace, path="/departments")
    api.add_namespace(course_namespace, path="/courses")
    api.add_namespace(course_student_namespace, path="/course/students")
    api.add_namespace(adm_student_namespace, path="/students")
    api.add_namespace(student_namespace, path="/student")
    api.add_namespace(student_courses_namespace, path="/students/courses")
    api.add_namespace(student_grades_namespace, path="/students/grades")
    api.add_namespace(student_records_namespace, path="/students/records")
    api.add_namespace(adm_teacher_namespace, path="/teachers")
    api.add_namespace(teacher_namespace, path="/teacher/")

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

    # @app.errorhandler(AttributeError)
    # def attribute_error(error):
    #     return {"error": "Attribute Error, 'NoneType' object has no attribute 'is_active'"}

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
            "Admin": Admins,
            "Student": Student,
            "Teacher": Teacher,
            "Course": Course,
            "GradeScale": GradeScale,
            "StudentCourse": StudentCourseScore,
            "StudentCourse": StudentRecord,
            "Department": Department,
            "create_defaults": create_defaults
        }

    # Flask views
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
