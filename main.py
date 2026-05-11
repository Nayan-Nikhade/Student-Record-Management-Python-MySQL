import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234', 
    'database': 'student_db'
}

def get_grade(marks):
    if marks >= 90: return "A+"
    elif marks >= 75: return "A"
    elif marks >= 60: return "B"
    elif marks >= 40: return "C"
    else: return "Fail"

def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None

def setup_database():
    """
    Initialize database. Creates table only if not exists.
    Adds sample data if table is empty.
    """
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
        cursor.execute("USE student_db")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                RollNo INT PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Marks INT CHECK (Marks >= 0 AND Marks <= 100)
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]

        if count == 0:
            sample_data = [
                (101, 'Amit Sharma', 85),
                (102, 'Priya Singh', 91),
                (103, 'Rahul Verma', 65),
                (104, 'Neha Gupta', 45),
                (105, 'Rohan Das', 78)
            ]
            cursor.executemany("INSERT INTO students (RollNo, Name, Marks) VALUES (%s, %s, %s)", sample_data)
            connection.commit()
            print("Sample data added successfully.")

        print("Database initialized successfully.")
    except Error as e:
        print(f"Database Setup Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_student():
    try:
        print("\n--- Add New Student Record ---")
        name = input("Enter Student Name: ").strip()
        roll_no = int(input("Enter Roll Number: "))

        while True:
            marks = int(input("Enter Marks (0-100): "))
            if 0 <= marks <= 100:
                break
            print("Invalid input. Marks must be between 0 and 100.")

        connection = create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO students (RollNo, Name, Marks) VALUES (%s, %s, %s)"
        values = (roll_no, name, marks)
        cursor.execute(query, values)
        connection.commit()
        print("Student record added successfully.")
        print(f"Grade: {get_grade(marks)}")

    except ValueError:
        print("Invalid input. Please enter numeric values for Roll Number and Marks.")
    except mysql.connector.IntegrityError:
        print("Error: Roll Number already exists. Please use a unique Roll Number.")
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def remove_student_by_roll_no():
    try:
        roll_no = int(input("\nEnter Roll Number to remove: "))
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Name FROM students WHERE RollNo = %s", (roll_no,))
        record = cursor.fetchone()
        if not record:
            print("No student found with the provided Roll Number.")
            return
        confirm = input(f"Are you sure you want to delete {record[0]}? (y/n): ").lower()
        if confirm!= 'y':
            print("Operation cancelled.")
            return
        query = "DELETE FROM students WHERE RollNo = %s"
        cursor.execute(query, (roll_no,))
        connection.commit()
        print("Student record deleted successfully.")
    except ValueError:
        print("Invalid input. Roll Number must be numeric.")
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def search_student_by_roll_no():
    try:
        roll_no = int(input("\nEnter Roll Number to search: "))
        connection = create_connection()
        cursor = connection.cursor()
        query = "SELECT RollNo, Name, Marks FROM students WHERE RollNo = %s"
        cursor.execute(query, (roll_no,))
        record = cursor.fetchone()
        if record:
            print("\n--- Student Record Found ---")
            print(f"Roll Number : {record[0]}")
            print(f"Name : {record[1]}")
            print(f"Marks : {record[2]}")
            print(f"Grade : {get_grade(record[2])}")
        else:
            print("No student found with the provided Roll Number.")
    except ValueError:
        print("Invalid input. Roll Number must be numeric.")
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def modify_marks():
    try:
        roll_no = int(input("\nEnter Roll Number to modify marks: "))
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Name, Marks FROM students WHERE RollNo = %s", (roll_no,))
        record = cursor.fetchone()
        if not record:
            print("No student found with the provided Roll Number.")
            return
        print(f"Student Name: {record[0]}")
        print(f"Current Marks: {record[1]}")
        print(f"Current Grade: {get_grade(record[1])}")
        while True:
            new_marks = int(input("Enter new Marks (0-100): "))
            if 0 <= new_marks <= 100:
                break
            print("Invalid input. Marks must be between 0 and 100.")
        query = "UPDATE students SET Marks = %s WHERE RollNo = %s"
        cursor.execute(query, (new_marks, roll_no))
        connection.commit()
        if cursor.rowcount > 0:
            print("Marks updated successfully.")
            print(f"New Grade: {get_grade(new_marks)}")
        else:
            print("Update failed.")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def view_all_students():
    try:
        print("\n--- All Student Records ---")
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT RollNo, Name, Marks FROM students ORDER BY RollNo")
        records = cursor.fetchall()
        if not records:
            print("No records found.")
            return
        print(f"{'Roll No':<10} {'Name':<20} {'Marks':<10} {'Grade':<8}")
        print("-" * 50)
        for row in records:
            grade = get_grade(row[2])
            print(f"{row[0]:<10} {row[1]:<20} {row[2]:<10} {grade:<8}")
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    setup_database()
    while True:
        print("\n====== Student Record Management System ======")
        print("1. Add Student")
        print("2. Remove Student by Roll No")
        print("3. Search Student by Roll No")
        print("4. Modify Marks")
        print("5. View All Students")
        print("6. Exit")
        print("============================================")
        choice = input("Enter your choice (1-6): ")
        if choice == '1': add_student()
        elif choice == '2': remove_student_by_roll_no()
        elif choice == '3': search_student_by_roll_no()
        elif choice == '4': modify_marks()
        elif choice == '5': view_all_students()
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()