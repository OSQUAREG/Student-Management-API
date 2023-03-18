from .models import User, Department, GradeScale
from .utils import db

"""
To Create Tables and The Defaults Record, Run These Commands in Heroku CLI/Console:
export FLASK_APP=runserver.py
flask shell
create_defaults()
"""
def create_defaults():

    from decouple import config
    from werkzeug.security import generate_password_hash
    from datetime import datetime

    db.drop_all()
    db.create_all()
        
    admin_department = Department(
        name="Admins",
        code="ADMS",
        created_by="super.admin",
        created_on=datetime.utcnow(),  
    )
    admin_department.save_to_db()
    
    super_admin = User(
        first_name="Super",
        last_name="Admin",
        gender="MALE",
        email="superadmin@sm.com",
        username="super.admin",
        password_hash=generate_password_hash(config("DEFAULT_SUPERADMIN_PASSWORD")),
        type="user",
        department_id=1,
        created_on=datetime.utcnow(),
        is_staff=False,
        is_admin=True,
    )
    super_admin.save_to_db()

    admin = User(
        first_name="Admin",
        last_name="Admin",
        gender="MALE",
        email="admin@sm.com",
        username="admin",
        password_hash=generate_password_hash(config("DEFAULT_ADMIN_PASSWORD")),
        type="user",
        department_id=1,
        created_on=datetime.utcnow(),
        is_staff=False,
        is_admin=True,
    )
    admin.save_to_db()

    grade = ["A", "B", "C", "D", "E", "F"]
    point = [4, 3, 2, 1, 0, 0]
    min = [70, 60, 50, 45, 40, 0]
    max = [100, 69, 59, 49, 44, 39]
    i = 0
    while i < len(grade):
        gradescale = GradeScale(
            grade=grade[i],
            point=point[i],
            min=min[i],
            max=max[i],
            created_by="super.admin",
            created_on=datetime.utcnow(),
        )
        gradescale.save_to_db()
        i += 1
