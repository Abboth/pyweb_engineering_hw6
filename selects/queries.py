import logging
import sqlite3
from sqlite3 import Error


def queries_sql(query):
    try:
        with sqlite3.connect("../database/college_data.sqlite") as con:
            query_count = 1
            for task in query:
                cur = con.cursor()
                cur.execute(task)
                logging.info("Query executed successfully")
                print(cur.fetchall())

                with open(f"query_{query_count}.sql", "w", encoding="utf-8") as file:
                    file.write(task)
                query_count += 1
            con.close()

    except Error as e:
        logging.error(f"Error executing query: {e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    get_max_avg_grades = """
    WITH student_avg_grades AS (
    SELECT
        sg.student_id,
        s.name AS student_name,
        ROUND(AVG(sg.grade)) AS average_grade
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    GROUP BY
        sg.student_id
)
SELECT
    student_name,
    average_grade
FROM
    student_avg_grades
ORDER BY
    average_grade DESC
LIMIT 5;

    """

    # Знайти студента із найвищим середнім балом з певного предмета.
    get_student_highest_grade_subject = """
    WITH student_highest_grade AS (
    SELECT 
        sg.student_id,
        s.name AS student_name,
        sg.subject_id,
        MAX(sg.grade) AS max_grade
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    WHERE
        sg.subject_id = 4
    ORDER BY
        sg.student_id, sg.subject_id
)
SELECT
    shg.student_name,
    shg.max_grade,
    sub.subject_name
FROM
    student_highest_grade as shg
JOIN
    subjects sub ON shg.subject_id = sub.id
LIMIT 1
    """

    #    Знайти середній бал у групах з певного предмета.
    get_avg_grade_group_subject = """
    WITH avg_grade_group_subject AS(
    SELECT
        sg.subject_id,
        g.group_number AS group_number,
        sg.student_id,
        ROUND(AVG(sg.grade)) AS avg_grade_group
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    JOIN
        groups g ON s.id = g.group_number
    WHERE
        sg.subject_id = 6
    GROUP BY
        g.group_number, sg.subject_id
    ORDER BY
        g.group_number
)
SELECT
    agg.group_number,
    agg.avg_grade_group,
    sub.subject_name
FROM
    avg_grade_group_subject as agg
JOIN
    subjects sub ON agg.subject_id = sub.id
    """

    # Знайти середній бал на потоці (по всій таблиці оцінок).
    get_total_avg_grade = """
    SELECT
        ROUND(AVG(sg.grade), 2)
    FROM
        students_grades sg;
    """

    # Знайти які курси читає певний викладач.
    get_courses_by_teacher = """
    SELECT
        ts.teacher_id,
        t.name AS teacher_name,
        sub.subject_name
    FROM
        teacher_subjects ts
    JOIN
        teachers t ON ts.teacher_id = t.id
    JOIN
        subjects sub ON ts.subject_id = sub.id
    WHERE
        ts.teacher_id = 2;
    """

    # Знайти список студентів у певній групі.

    get_students_by_group = """
    SELECT
        s.name AS student_name
    FROM
        students s
    JOIN
        groups g ON s.group_number = g.group_number
    WHERE
        g.group_number = 2;
    
    """

    # Знайти оцінки студентів у окремій групі з певного предмета.
    get_grades_by_group_subject = """
    SELECT
        s.name AS student_name,
        g.group_number,
        sub.subject_name,
        sg.grade
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    JOIN
        groups g ON s.group_number = g.group_number
    JOIN
        subjects sub ON sg.subject_id = sub.id 
    WHERE
        g.group_number = 2
        AND sub.id = 5;
        """

    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    get_avg_grade_by_teacher = """
    SELECT
        ROUND(AVG(sg.grade),1),
        t.name AS teacher_name,
        sub.subject_name
    FROM
        students_grades sg
    JOIN
        teachers t ON ts.teacher_id = t.id
    JOIN
        subjects sub ON sg.subject_id = sub.id
    JOIN
        teacher_subjects ts ON ts.subject_id = sub.id
    WHERE
        t.id = 1
    GROUP BY
        t.name,
        sub.subject_name
    """

    # Знайти список курсів, які відвідує студент.
    get_courses_by_student = """
    SELECT
        s.name AS student_name,
        sub.subject_name
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    JOIN
        subjects sub ON sg.subject_id = sub.id
    WHERE
        s.id = 1;
    """

    # Список курсів, які певному студенту читає певний викладач.
    get_courses_by_student_teacher = """
    SELECT
        s.name AS student_name,
        t.name AS teacher_name,
        sub.subject_name
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    JOIN
        teacher_subjects ts ON ts.teacher_id = t.id
    JOIN
        teachers t ON ts.teacher_id = t.id
    JOIN
        subjects sub ON sg.subject_id = sub.id
    WHERE
        s.id = 1
        AND t.id = 2;
    """

    # Середній бал, який певний викладач ставить певному студентові.
    get_avg_grade_by_teacher_to_student = """
    SELECT
        ROUND(AVG(sg.grade), 1) AS avg_grade,
        s.name AS student_name,
        t.name AS teacher_name
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    JOIN
        teachers t ON sg.teacher_id = t.id
    WHERE
        t.id = 1
        AND
        s.id = 4
    GROUP BY
        s.name,
        t.name;  
    """

    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    get_grades_by_group_subject_last_lesson = """
    SELECT
        s.name AS student_name,
        g.group_number,
        sub.subject_name,
        sg.grade AS grades
    FROM
        students_grades sg
    JOIN
        students s ON sg.student_id = s.id
    JOIN
        groups g ON s.group_number = g.group_number
    JOIN
        subjects sub ON sg.subject_id = sub.id
    WHERE
        sub.id = 1
        AND g.group_number = 1
        AND sg.date = (
        SELECT MAX(date) 
        FROM students_grades
        WHERE subject_id = 1);        
    """

    queries = [get_max_avg_grades,
               get_student_highest_grade_subject,
               get_avg_grade_group_subject,
               get_total_avg_grade,
               get_courses_by_teacher,
               get_students_by_group,
               get_grades_by_group_subject,
               get_avg_grade_by_teacher,
               get_courses_by_student,
               get_courses_by_student_teacher,
               get_avg_grade_by_teacher_to_student,
               get_grades_by_group_subject_last_lesson]

    queries_sql(queries)
