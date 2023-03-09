from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required, current_user
from ..auth import auth_namespace
from ..auth.schemas import login_model, register_model, user_model, change_password_model
from ..models import User
from http import HTTPStatus
from ..utils.db_func import generate_matric_no
from ..blocklist import BLOCKLIST
from decouple import config


# USER REGISTRATION
@auth_namespace.route("/register")
class UserRegister(Resource):
    @auth_namespace.expect(register_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description="User Registration")
    @jwt_required()
    def post(self):
        """
        Register a User
        """
        if current_user.is_admin:
            data = auth_namespace.payload

            first_name = data["first_name"]
            last_name = data["last_name"]
            gender = data["gender"]
            email = data["email"]
            password_hash = generate_password_hash(config("DEFAULT_PASSWORD"))

            # instantiate the User class
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                password_hash=password_hash
            )
            new_user.save_to_db()

            # generate and update student matric_no
            new_user.matric_no = generate_matric_no(new_user.id)
            new_user.update_db()
            
            return new_user, HTTPStatus.CREATED
        
        return {"message": "You are not unauthorized to perform this action"}, HTTPStatus.UNAUTHORIZED


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
            access_token = create_access_token(identity=user.matric_no)
            refresh_token = create_refresh_token(identity=user.matric_no)

            # check if login password is still default password: password12345
            if check_password_hash(user.password_hash, config("DEFAULT_PASSWORD")):
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
    
        return {"message": "Invalid Credentials"}, HTTPStatus.UNAUTHORIZED


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
@auth_namespace.route("/password")
class ChangePassword(Resource):
    @auth_namespace.expect(change_password_model)
    @auth_namespace.doc(description="Change Current User Password")
    @jwt_required()
    def patch(self):
        """
        Change Current User Password
        """
        data = auth_namespace.payload
        matric_no = get_jwt_identity()
        user = User.query.filter_by(matric_no=matric_no).first()
        
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

                response = {"message": "Password Changed Successfully. Please Log in Again"}
                return response, HTTPStatus.OK

            response = {"message": "You are not authorized to perform this operation"}
            return response, HTTPStatus.UNAUTHORIZED
        
        response = {"message": "Mismatched New and Confirm Password"}
        return response, HTTPStatus.CONFLICT
