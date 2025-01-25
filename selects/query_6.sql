
    SELECT
        s.name AS student_name
    FROM
        students s
    JOIN
        groups g ON s.group_number = g.group_number
    WHERE
        g.group_number = 2;
    
    