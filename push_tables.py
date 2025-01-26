import logging
import os
from create_connection import get_connection
from sqlite3 import Error

logging.basicConfig(level=logging.INFO)


def create_table(con, table_query, table_name):
    cur = con.cursor()
    try:
        if os.path.exists("./database/college_data.sqlite"):
            cur.execute(table_query)
            con.commit()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            result = cur.fetchone()
            if result:
                logging.info(f"{table_name} created successfully")
            else:
                raise Error
    except Error as e:
        logging.error(f"Error creating table {table_name}: {e}")
    except FileNotFoundError as e:
        logging.error(f"Database not exist yet: {e}")


def main():
    try:
        with get_connection() as conn:
            create_table(conn, teachers_table, "teachers")
            create_table(conn, students_table, "students")
            create_table(conn, subjects_table, "subjects")
            create_table(conn, teacher_subjects_table, "teacher_subjects")
            create_table(conn, students_grades, "students_grades")
            create_table(conn, group_table, "groups")

            logging.info("Tables created successfully.")
            conn.close()
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
