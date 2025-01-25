
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
    