
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
    