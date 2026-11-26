
create database course_enrollment;
use course_enrollment;
create table enrollments(enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
                         student_name VARCHAR(20) NOT NULL,
                         course_name VARCHAR(20) NOT NULL,
                         duration_months INT CHECK(duration_months>0),
                         enrollment_date DATE,
                         fee INT CHECK(fee>=0),
                         status VARCHAR(20));
                         
