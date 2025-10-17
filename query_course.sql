SELECT
	c.title,
	COUNT(DISTINCT cc.serial)
FROM
	courses c
LEFT JOIN
	course_sections cs ON c.serial = cs.course_serial
LEFT JOIN
	course_contents cc ON cs.serial = cc.course_section_serial
GROUP BY 
	c.title;