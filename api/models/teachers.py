from ..utils import db
from ..utils.db_func import DB_Func
from datetime import datetime
from .users import Gender
from enum import Enum


class Title(Enum):
    PROF = "prof"
    ENGR = "engr"
    DR = "dr"
    MR = "mr"
    MRS = "mrs"
    MS = "ms"


class Teacher(db.Model, DB_Func):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Enum(Title), nullable=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship("Course", backref="teacher", lazy=True)

    def __repr__(self):
        return f"<Teacher ID: {self.id}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
