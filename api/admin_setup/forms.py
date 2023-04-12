from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import check_password_hash
from ..utils import db
from ..models import User, Admins


class LoginForm(FlaskForm):
    email = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[validators.InputRequired()])

    def get_user(self):
        return db.session.query(Admins).filter_by(email=self.email.data).first()

    def validate_login(self, field):
        user = self.get_user()

        if user is None and not user.is_admin and not user.is_staff:
            raise validators.ValidationError("Unauthorized Admin User")

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError("Invalid password")


class RegistrationForm(FlaskForm):
    first_name = StringField(label="First Name", validators=[validators.InputRequired()])
    last_name = StringField(label="Last Name", validators=[validators.InputRequired()])
    gender = StringField(label="Gender", validators=[validators.InputRequired()])
    email = StringField(label="Email", validators=[validators.InputRequired()])
    password = PasswordField(validators=[validators.InputRequired()])

    def validate_email(self, field):
        if User.check_email_exist(self.email.data):
            raise validators.ValidationError("Email already exist")
