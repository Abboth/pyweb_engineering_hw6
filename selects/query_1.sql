
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

    