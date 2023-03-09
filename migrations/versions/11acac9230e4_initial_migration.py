"""initial migration

Revision ID: 11acac9230e4
Revises: 
Create Date: 2023-03-07 22:12:02.548852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11acac9230e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Enum('PROF', 'ENGR', 'DR', 'MR', 'MRS', 'MS', name='title'), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_teachers'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('matric_no', sa.String(length=12), nullable=True),
    sa.Column('gpa', sa.Float(precision=2, asdecimal=True), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('date_registered', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('matric_no', name=op.f('uq_users_matric_no'))
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name=op.f('fk_courses_teacher_id_teachers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_courses'))
    )
    op.create_table('student_courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('grade_percent', sa.Float(precision=2, asdecimal=True), nullable=True),
    sa.Column('grade_scale', sa.Float(precision=1, asdecimal=True), nullable=True),
    sa.Column('date_registered', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('fk_student_courses_course_id_courses')),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], name=op.f('fk_student_courses_student_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_student_courses'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_courses')
    op.drop_table('courses')
    op.drop_table('users')
    op.drop_table('teachers')
    # ### end Alembic commands ###
