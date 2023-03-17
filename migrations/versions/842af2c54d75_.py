"""empty message

Revision ID: 842af2c54d75
Revises: 8f7a4337fae1
Create Date: 2023-03-17 20:32:24.290680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "842af2c54d75"
down_revision = "8f7a4337fae1"
branch_labels = None
depends_on = None


def upgrade():
    from decouple import config
    from werkzeug.security import generate_password_hash

    password_hash = generate_password_hash(config("DEFAULT_SUPERADMIN_PASSWORD"))
    password_hash2 = generate_password_hash(config("DEFAULT_ADMIN_PASSWORD"))

    op.execute(
        f'''
    INSERT INTO users 
    ("first_name", "last_name", "gender", "email", "username", "password_hash", "type", "department_id", "created_by", "created_on", "is_staff", "is_admin")
    VALUES 
    ("Super", "Admin", "MALE", "superadmin@sm.com", "super.admin", "{password_hash}", "user", 1, "super.admin", CURRENT_TIMESTAMP, True, True)
    '''
    )

    op.execute(
        f'''
    INSERT INTO users 
    ("first_name", "last_name", "gender", "email", "username", "password_hash", "type", "department_id", "created_by", "created_on", "is_staff", "is_admin")
    VALUES 
    ("Admin", "Admin", "MALE", "admin@sm.com", "admin", "{password_hash2}", "user", 1, "super.admin", CURRENT_TIMESTAMP, True, True)
    '''
    )

    op.execute(
        f'''
    INSERT INTO departments 
    (name, code, created_by, created_on) 
    VALUES 
    ("Admin", "ADM", "super.admin", CURRENT_TIMESTAMP);
    '''
    )

    op.execute(
        """
    INSERT INTO gradescale (grade, point, min, max, created_by, created_on)
    VALUES 
    ('A', 4, 70, 100, 'admin', CURRENT_TIMESTAMP),
    ('B', 3, 60, 69, 'admin', CURRENT_TIMESTAMP),
    ('C', 2, 50, 59, 'admin', CURRENT_TIMESTAMP),
    ('D', 1, 45, 49, 'admin', CURRENT_TIMESTAMP),
    ('E', 0, 40, 44, 'admin', CURRENT_TIMESTAMP),
    ('F', 0, 0, 39, 'admin', CURRENT_TIMESTAMP);
    """
    )


def downgrade():
    op.execute("DELETE FROM users;")
    op.execute("DELETE FROM departments;")
    op.execute("DELETE FROM gradescale;")
