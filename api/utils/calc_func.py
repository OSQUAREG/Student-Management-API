from sqlalchemy import func
from . import db
from ..models import StudentCourseScore, StudentRecord, GradeScale


"""STUDENT COURSE SCORE CALC FUNCTIONS"""

def get_score_grade(student_id, course_id, score):
    grade_point = (
        db.session.query(GradeScale.grade, GradeScale.point)
        .filter(GradeScale.min <= score, GradeScale.max >= score)
        .filter(
            StudentCourseScore.student_id == student_id,
            StudentCourseScore.course_id == course_id,
        )
    ).first()
    return grade_point.grade, grade_point.point


def calc_scored_point(student_id, course_id):
    scored_point = (
        db.session.query(StudentCourseScore.credit * StudentCourseScore.grade_point)
        .filter(
            StudentCourseScore.student_id == student_id,
            StudentCourseScore.course_id == course_id,
        )
        .scalar()
    )
    return scored_point


"""STUDENT RECORDS CALC FUNCTIONS"""

def calc_course_count(student_id):
    course_count = (
        db.session.query(StudentCourseScore)
        .filter(StudentCourseScore.student_id == student_id)
        .count()
    )
    return course_count


def calc_total_credits(student_id):
    total_credits = (
        db.session.query(func.sum(StudentCourseScore.credit))
        .filter(StudentCourseScore.student_id == student_id)
        .scalar()
    )
    return total_credits


def calc_total_points(student_id):
    total_points = (
        db.session.query(func.sum(StudentCourseScore.scored_point))
        .filter(StudentCourseScore.student_id == student_id)
        .scalar()
    )
    return total_points


def calc_student_gpa_honours(student_id):
    # multiplied the gpa value by 100 before storing it in the database.
    # divide by 100 when retrieving it from the database.
    gpa = (
        db.session.query((StudentRecord.total_points / StudentRecord.total_credits) * 100) 
        .filter(StudentRecord.student_id == student_id)
        .scalar()
    )

    honours = None

    if gpa/100 >= 3.5:
        honours = "First Class Honours"
    elif gpa/100 >=3.0 and gpa/100 <=3.49:
        honours = "Second Class Honours (Upper Division)"
    elif gpa/100 >=2.0 and gpa/100 <=2.99:
        honours = "Second Class Honours (Lower Division)"
    elif gpa/100 >=1.0 and gpa/100 <=1.99:
        honours = "Third Class Honours"
    else:
        honours = "No Honours/Degree"
        
    return int(gpa), honours
