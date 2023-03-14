from datetime import datetime

# def generate_matric_no(student_id,dept_code):
#     today = datetime.utcnow()
#     year_str = today.strftime("%y")
#     return f"ADM/{dept_code}/{year_str}/{student_id:04d}"


# nums = ["ST/BEE/00001","ST/BEE/2023/002","ST/FEE/2023/001","ST/BEE/2023/003","ST/FEE/2023/002"]

# for num in nums:
#     if num.


def generate_matric_no(student_id):
    year_str = str(datetime.utcnow().year)
    year_str = year_str[-3:]
    return f"STU/{year_str}/{student_id:04d}"

print(generate_matric_no(4))
