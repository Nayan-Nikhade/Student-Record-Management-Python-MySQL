# Student Record Management System

A Python + MySQL based CRUD application to manage student records with auto grade calculation.

## Features
- ✅ Add New Student
- ✅ Remove Student by Roll Number  
- ✅ Search Student by Roll Number
- ✅ Modify Student Marks
- ✅ View All Students with Grades
- ✅ Auto Grade: A+ >=90, A >=75, B >=60, C >=40, Fail <40
- ✅ Data Validation & Exception Handling
- ✅ MySQL Database Integration

## Tech Stack
`Python` `MySQL` `mysql-connector-python`

## Setup & Run
1. Install dependency: `pip install mysql-connector-python`
2. Create MySQL database or let the script auto-create it
3. Update password in `main.py` → `DB_CONFIG`
4. Run: `python main.py`

## Database Schema
```sql
CREATE TABLE students (
    RollNo INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Marks INT CHECK (Marks >= 0 AND Marks <= 100)
);
