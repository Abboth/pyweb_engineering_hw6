
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
    