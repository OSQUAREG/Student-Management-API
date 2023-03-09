from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class User(db.Model, DB_Func):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    matric_no = db.Column(db.String(12), unique=True)
    gpa = db.Column(db.Float(precision=2, asdecimal=True), default=0.00)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow())
    courses_count = db.Column(db.Integer, nullable=True)

    courses = db.relationship("StudentCourse", backref="student", lazy=True)

    def __repr__(self):
        return f"<User UID: {self.uid}>"

    @classmethod
    def get_by_matric_no(cls, matric_no):
        return cls.query.get_or_404(matric_no)

    def generate_pwd_hash(password):
        return generate_password_hash(password)
