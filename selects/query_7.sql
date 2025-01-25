
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

    