from create_connection import get_connection
from sqlite3 import Error
import logging

logging.basicConfig(level=logging.INFO)


def create_table(con, table_query):
    cur = con.cursor()
    try:
        cur.execute(table_query)
        con.commit()
    except Error as e:
        logging.info(f"Error creating table: {e}")


def main():
    try:
        with get_connection() as conn:
            tasks = [create_table(conn, teachers_table),
                     create_table(conn, students_table),
                     create_table(conn, subjects_table),
                     create_table(conn, teacher_subjects_table),
                     create_table(conn, students_grades),
                     create_table(conn, group_table),]

            logging.info("Tables created successfully.")
    except Error as e:
        logging.error(f"Error creating tables: {e}")


teachers_table = """
    CREATE TABLE IF NOT EXISTS teachers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """

students_table = """
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_number INTEGER NOT NULL,
        FOREIGN KEY (group_number) REFERENCES groups (group_number)
    );
    """

subjects_table = """
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT NOT NULL
    );
    """

teacher_subjects_table = """
    CREATE TABLE IF NOT EXISTS teacher_subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers (id),
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
    );
    """

students_grades = """
    CREATE TABLE IF NOT EXISTS students_grades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
        FOREIGN KEY (teacher_id) REFERENCES teachers (id)
    );
    """

group_table = """
CREATE TABLE IF NOT EXISTS groups(
        group_number INTEGER NOT NULL,
        FOREIGN KEY (group_number) REFERENCES students (group_number)
    );
    """
