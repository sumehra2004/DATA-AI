from pymongo import MongoClient
import pandas as pd

# -----------------------------
# CONNECT TO MONGODB
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["universityDB"]   # Database auto-created

# Drop old data (optional for fresh run)
db.students.drop()
db.courses.drop()
db.departments.drop()
db.instructors.drop()
db.enrollments.drop()

print("Connected to MongoDB & Database Created\n")

# -----------------------------
# INSERT DOCUMENTS
# -----------------------------

# Departments
departments = [
    {"dept_code": "D01", "dept_name": "Computer Science", "building": "Block A"},
    {"dept_code": "D02", "dept_name": "Information Tech", "building": "Block B"},
    {"dept_code": "D03", "dept_name": "Electronics", "building": "Block C"},
    {"dept_code": "D04", "dept_name": "Mechanical", "building": "Block D"},
    {"dept_code": "D05", "dept_name": "Civil", "building": "Block E"}
]
db.departments.insert_many(departments)

# Instructors
instructors = [
    {"inst_code": "I01", "name": "Dr. Sharma", "experience": 10},
    {"inst_code": "I02", "name": "Prof. Iyer", "experience": 8},
    {"inst_code": "I03", "name": "Dr. Khan", "experience": 12},
    {"inst_code": "I04", "name": "Prof. Mehta", "experience": 6},
    {"inst_code": "I05", "name": "Dr. Rao", "experience": 15}
]
db.instructors.insert_many(instructors)

# Students
students = [
    {"stud_code": "S01", "name": "Aman", "age": 21, "email": "aman@gmail.com", "dept_code": "D01"},
    {"stud_code": "S02", "name": "Neha", "age": 19, "email": "neha@gmail.com", "dept_code": "D02"},
    {"stud_code": "S03", "name": "Riya", "age": 23, "email": "riya@gmail.com", "dept_code": "D01"},
    {"stud_code": "S04", "name": "Kunal", "age": 22, "email": "kunal@gmail.com", "dept_code": "D03"},
    {"stud_code": "S05", "name": "Priya", "age": 20, "email": "priya@gmail.com", "dept_code": "D04"}
]
db.students.insert_many(students)

# Courses
courses = [
    {"course_code": "C01", "title": "Database Systems", "credits": 4, "inst_code": "I01"},
    {"course_code": "C02", "title": "Operating Systems", "credits": 3, "inst_code": "I02"},
    {"course_code": "C03", "title": "Computer Networks", "credits": 4, "inst_code": "I03"},
    {"course_code": "C04", "title": "AI Basics", "credits": 2, "inst_code": "I04"},
    {"course_code": "C05", "title": "Machine Learning", "credits": 3, "inst_code": "I05"}
]
db.courses.insert_many(courses)

# Enrollments
enrollments = [
    {"stud_code": "S01", "course_code": "C01"},
    {"stud_code": "S02", "course_code": "C02"},
    {"stud_code": "S03", "course_code": "C01"},
    {"stud_code": "S04", "course_code": "C03"},
    {"stud_code": "S05", "course_code": "C04"}
]
db.enrollments.insert_many(enrollments)

print("Data Inserted Successfully\n")

# -----------------------------
# READ OPERATIONS
# -----------------------------

print("All Students:")
for s in db.students.find():
    print(s)

print("\nStudents older than 20:")
for s in db.students.find({"age": {"$gt": 20}}):
    print(s)

# -----------------------------
# UPDATE OPERATION
# -----------------------------
db.students.update_one(
    {"stud_code": "S01"},
    {"$set": {"email": "aman_updated@gmail.com"}}
)
print("\nUpdated Email for S01")

# -----------------------------
# DELETE OPERATION
# -----------------------------
db.students.delete_one({"stud_code": "S05"})
print("Deleted Student S05\n")

# -----------------------------
# CREATE INDEX
# -----------------------------
db.students.create_index("email")
print("Index Created on Email\n")

# -----------------------------
# AGGREGATION
# -----------------------------
print("Students Per Department:")
result = db.students.aggregate([
    {"$group": {"_id": "$dept_code", "total": {"$sum": 1}}}
])
for r in result:
    print(r)

# -----------------------------
# EXPORT TO CSV
# -----------------------------

def export_to_csv(collection_name):
    data = list(db[collection_name].find())
    if data:
        df = pd.DataFrame(data)
        df.drop(columns=["_id"], inplace=True)
        df.to_csv(f"{collection_name}.csv", index=False)
        print(f"{collection_name}.csv exported successfully")

export_to_csv("students")
export_to_csv("courses")
export_to_csv("departments")
export_to_csv("instructors")
export_to_csv("enrollments")

print("\nAll CSV files created successfully!")