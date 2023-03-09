from datetime import datetime

id = 9900

cur_year = datetime.utcnow().year

# new_id = f"STU/{datetime.now().year}/{id:05d}"
# print(new_id)

new_id1 = f"ST/{cur_year}/{id:04d}"
print(new_id1)


