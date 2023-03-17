from flask_restx import Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required, current_user
from ..auth import auth_namespace
from ..auth.schemas import login_model, register_model, user_model, change_password_model
from ..models import User, Student, Teacher, StudentRecord
from http import HTTPStatus
from ..blocklist import BLOCKLIST
from decouple import config


# USER REGISTRATION
@auth_namespace.route("/register")
class UserRegister(Resource):
    @auth_namespace.expect(register_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description="User Registration (Admin Only)")
    @jwt_required()
    def post(self):
        """
        Admin: Register a User
        """
        if current_user.is_admin:
            data = auth_namespace.payload
            
            # if new user is a student
            if data["user_type"].upper() == "STUDENT":
                # check if email exist
                email_exist = Student.query.filter_by(email=data["email"]).first()
                if email_exist is None:
                    new_student = Student(
                        title=data["title"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        gender=data["gender"],
                        email=data["email"],
                        password_hash=generate_password_hash(config("DEFAULT_STUDENT_PASSWORD")),
                        department_id=data["department_id"],
                        created_by=current_user.username,
                        is_staff=False,
                    )
                    new_student.save_to_db()
                    # generate username
                    new_student.generate_username(new_student.user_id, new_student.first_name, new_student.last_name)
                    # generate matric number
                    new_student.generate_matric_no(new_student.student_id)

                    # instantiate new Student Records class
                    new_stu_record = StudentRecord(
                        student_id=new_student.student_id,
                        matric_no=new_student.matric_no,
                        department_id=new_student.department_id,
                        created_by=current_user.username
                    )
                    new_stu_record.save_to_db()

                    return new_student, HTTPStatus.CREATED
                
                abort(HTTPStatus.CONFLICT, message="Email already exist")

            # if new user is a teacher
            elif data["user_type"].upper() == "TEACHER":
                # check if email exist
                email_exist = Teacher.query.filter_by(email=data["email"]).first()
                if email_exist is None:
                    new_teacher = Teacher(
                        title=data["title"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        gender=data["gender"],
                        email=data["email"],
                        password_hash=generate_password_hash(config("DEFAULT_TEACHER_PASSWORD")),
                        department_id=data["department_id"],
                        created_by=current_user.username,
                        is_staff=True,
                    )
                    new_teacher.save_to_db()
                    # generate username
                    new_teacher.generate_username(new_teacher.user_id, new_teacher.first_name, new_teacher.last_name)
                    # generate matric number
                    new_teacher.generate_staff_code(new_teacher.teacher_id)

                    return new_teacher, HTTPStatus.CREATED
                
                abort(HTTPStatus.CONFLICT, message="Email already exist")
                
            abort(HTTPStatus.BAD_REQUEST, message="Select User Type: TEACHER or STUDENT")
        
        abort(HTTPStatus.UNAUTHORIZED, message="Admin Only")


# USER LOGIN
@auth_namespace.route("/login")
class UserLogin(Resource):
    @auth_namespace.expect(login_model)
    @auth_namespace.doc(description="Login: Generate JWT Tokens")
    def post(self):
        """
        Login: Genrate JWT Tokens
        """
        data = auth_namespace.payload

        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            # check if login password is still default password: password12345
            if check_password_hash(user.password_hash, config("DEFAULT_STUDENT_PASSWORD")) or check_password_hash(user.password_hash, config("DEFAULT_TEACHER_PASSWORD")) or check_password_hash(user.password_hash, config("DEFAULT_ADMIN_PASSWORD")):
                response = {
                    "message": "Login Successful! Please Change the Default Password!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                return response, HTTPStatus.CREATED

            response = {
                    "message": "Login Successful!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }

            return response, HTTPStatus.CREATED
    
        abort(HTTPStatus.UNAUTHORIZED, message="Invalid Credentials")


# TOKEN REFRESH
@auth_namespace.route("/refresh")
class TokenRefresh(Resource):
    @auth_namespace.doc(description="Refresh JWT Access Token")
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh JWT Access Token
        """
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)

        response = {
            "message": "Refresh Successful.",
            "access_token": access_token,
        }

        return response, HTTPStatus.CREATED


# USER LOGOUT
@auth_namespace.route("/logout")
class UserLogout(Resource):
    @auth_namespace.doc(description="Logout: Block JWT Token")
    @jwt_required()
    def post(self):
        """
        Logout: Add JWT Token to Blocklist
        """
        token = get_jwt()
        jti = token["jti"]
        BLOCKLIST.add(jti)

        return {"message": "Logged Out Successfully!"}


# USER CHANGE PASSWORD
@auth_namespace.route("/change-password")
class UserPasswordChange(Resource):
    @auth_namespace.expect(change_password_model)
    @auth_namespace.doc(description="Change Current User Password")
    @jwt_required()
    def patch(self):
        """
        Change Current User Password
        """
        data = auth_namespace.payload
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        old_password = data["old_password"]
        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        if new_password == confirm_password:
            if user and check_password_hash(user.password_hash, old_password):
                user.password_hash = generate_password_hash(new_password)

                user.update_db()

                # logs out current user
                token = get_jwt()
                jti = token["jti"]
                BLOCKLIST.add(jti)

                response = {"message": "Password Changed Successfully. Please Log-in Again"}
                return response, HTTPStatus.OK

            response = {"message": "You are not authorized to perform this operation"}
            return response, HTTPStatus.UNAUTHORIZED
        
        response = {"message": "Mismatched New and Confirm Password"}
        return response, HTTPStatus.CONFLICT
