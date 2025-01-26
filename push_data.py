import logging
from sqlite3 import Error
from create_connection import get_connection
from get_fake_data import main as prepared_data
from push_tables import main as create_tables


def push_data_in_database(students, teachers, teacher_subjects, student_grades, subjects, groups):
    with get_connection() as con:
        cur = con.cursor()
        try:

            sql_to_students = "INSERT INTO students (name, group_number) VALUES (?, ?)"
            cur.executemany(sql_to_students, students)
            logging.info(f"Data pushed into students table successfully.")

            sql_to_teachers = "INSERT INTO teachers (name) VALUES (?)"
            cur.executemany(sql_to_teachers, teachers)
            logging.info(f"Data pushed into teachers table successfully.")

            sql_to_subjects = "INSERT INTO subjects (subject_name) VALUES (?)"
            cur.executemany(sql_to_subjects, subjects)
            logging.info(f"Data pushed into subjects table successfully.")

            sql_to_groups = "INSERT INTO groups (group_number) VALUES (?)"
            cur.executemany(sql_to_groups, groups)
            logging.info(f"Data pushed into groups table successfully.")

            sql_to_grades = """
            INSERT INTO students_grades 
            (student_id, subject_id, teacher_id, grade, date)         
            VALUES (?, ?, ?, ?, ?)
            """
            cur.executemany(sql_to_grades, student_grades)
            logging.info(f"Data pushed into students_grades table successfully.")

            sql_to_teacher_subjects = """
            INSERT INTO teacher_subjects (teacher_id, subject_id) 
            VALUES (?, ?)
            """
            cur.executemany(sql_to_teacher_subjects, teacher_subjects)
            logging.info(f"Data pushed into teacher_subjects table successfully.")

            con.commit()
            logging.info("Data pushed into all tables successfully.")
            con.close()
        except Error as e:
            logging.error(f"Error pushing data into the database: {e}")
            con.rollback()


if __name__ == '__main__':
    students_grades, subjects_teachers, students, teachers, subjects, grades = prepared_data()
    create_tables()
    push_data_in_database(students, teachers, subjects_teachers, students_grades, subjects, grades)
