"""empty message

Revision ID: 0a73da054ce3
Revises: 686142c4f4e6
Create Date: 2023-03-11 22:54:08.586232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a73da054ce3'
down_revision = '686142c4f4e6'
branch_labels = None
depends_on = None


def upgrade():
    from decouple import config
    from werkzeug.security import generate_password_hash
    
    password_hash=generate_password_hash(config("DEFAULT_ADMIN_PASSWORD"))
    
    op.execute(
    f'''
    INSERT INTO users 
    (first_name, last_name, gender, email, username, password_hash, type, department_id, created_by, created_on, is_staff, is_admin)
    VALUES 
    ("Admin", "Admin", "MALE", "admin@sm.com", "admin", "{password_hash}", "user", 1, "admin", CURRENT_TIMESTAMP, True, True)
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
    op.execute(
    f'DELETE FROM users WHERE email = "admin@sm.com"'
    )
    
    op.execute(
    f'''
    DELETE FROM gradescale WHERE grade IN ('A', 'B', 'C', 'D', 'E', 'F');
    '''
    )

