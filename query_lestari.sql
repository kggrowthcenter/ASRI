SELECT 
  u.serial as serial,
  u.email AS email, 
  u.full_name AS name, 
  u.created_at AS regis_date,
  MAX(cu.created_at) AS enroll_date,
  MAX(cu.updated_at) AS last_update,
  c.title AS title, 
  c2.name AS category,
  ROUND(SUM(cup.progress_duration), 0) AS duration, 
  AVG(cup.progress_percentage) AS progress
FROM users u
LEFT JOIN course_users cu ON cu.user_serial = u.serial
LEFT JOIN courses c ON cu.course_serial = c.serial 
LEFT JOIN partner_groups pg ON cu.partner_group_serial = pg.serial
LEFT JOIN course_user_progress cup 
  ON cup.course_serial = cu.course_serial AND cup.user_serial = u.serial
LEFT JOIN categories c2 ON c2.serial = c.category_serial 
GROUP BY u.email, u.full_name, u.created_at, c.title, c2.name
ORDER BY regis_date DESC;
