from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sum2004",
    database="student_db"
)

@app.route('/')
def home():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("students.html", students=students)


@app.route('/student/<int:id>')
def student_detail(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    return render_template("student_detail.html", student=student)


if __name__ == '__main__':
    app.run(debug=True)