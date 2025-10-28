SELECT
	u.serial,
	u.email, 
	u.full_name AS name,
	c.title AS'c.title',
	cs.title AS 'cs.title',
	cc.title As 'cc.title',
	cup.score,
    cup.created_at,
    cup.updated_at
FROM
	course_user_progress cup 
LEFT JOIN
	users u ON cup.user_serial = u.serial
LEFT JOIN
	course_contents cc ON cup.course_content_serial = cc.serial
LEFT JOIN
	course_sections cs ON cup.course_section_serial = cs.serial
LEFT JOIN
	courses c ON cup.course_serial = c.serial
WHERE
	cc.type = 'QUIZ'