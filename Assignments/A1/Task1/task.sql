-- mysql -u root -p
-- CREATE DATABASE student_db;

USE student_db;

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    course VARCHAR(100)
);

INSERT INTO students (name, age, course)
VALUES ('John Doe', 20, 'Computer Science'),('Jane Smith', 22, 'Mathematics'),('Alice Johnson', 19, 'Physics');

SELECT * FROM students;
