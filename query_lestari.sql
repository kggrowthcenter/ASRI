SELECT 
  u.serial as serial,
  u.email AS email, 
  u.full_name AS name, 
  u.created_at AS regis_date,
  u.last_login AS last_login,
  MAX(cu.created_at) AS enroll_date,
  MAX(cup.updated_at) AS last_update,
  c.title AS title, 
  c2.name AS category,
  COUNT(DISTINCT CASE WHEN cup.is_accomplished = 1  
                        THEN cup.course_content_serial END) AS accomplished,
  ROUND(SUM(cup.progress_duration), 0) AS duration,
  pgm.status AS playlist_status,
  pgm.partner_group_serial 
FROM partner_group_members pgm
LEFT JOIN users u ON u.serial = pgm.user_serial 
LEFT JOIN course_users cu ON cu.user_serial = u.serial AND pgm.partner_group_serial = cu.partner_group_serial 
LEFT JOIN courses c ON cu.course_serial = c.serial 
LEFT JOIN course_user_progress cup ON cup.course_serial = cu.course_serial AND cup.user_serial = u.serial
LEFT JOIN categories c2 ON c2.serial = c.category_serial 
LEFT JOIN partner_playlists pp ON cup.partner_playlist_serial = pp.serial
GROUP BY
  u.serial,
  u.email,
  u.full_name,
  u.created_at,
  u.last_login,
  c.title,
  c2.name,
  cu.accomplished_at,
  c.serial,
  pgm.status,
  pgm.partner_group_serial
  
 UNION ALL
 
 
 SELECT 
  u.serial as serial,
  u.email AS email, 
  u.full_name AS name, 
  u.created_at AS regis_date,
  u.last_login AS last_login,
  MAX(cu.created_at) AS enroll_date,
  MAX(cup.updated_at) AS last_update,
  c.title AS title, 
  c2.name AS category,
  COUNT(DISTINCT CASE WHEN cup.is_accomplished = 1 
                        THEN cup.course_content_serial END) AS accomplished,
  ROUND(SUM(cup.progress_duration), 0) AS duration,
  pgm.status AS playlist_status,
  pgm.partner_group_serial 
FROM users u
LEFT JOIN course_users cu ON cu.user_serial = u.serial
LEFT JOIN courses c ON cu.course_serial = c.serial 
LEFT JOIN course_user_progress cup ON cup.course_serial = cu.course_serial AND cup.user_serial = u.serial
LEFT JOIN categories c2 ON c2.serial = c.category_serial 
LEFT JOIN partner_playlists pp ON cup.partner_playlist_serial = pp.serial
LEFT JOIN partner_group_members pgm ON cu.user_serial = pgm.user_serial AND cu.partner_group_serial = pgm.partner_group_serial
WHERE pgm.user_serial is NULL
GROUP BY
  u.serial,
  u.email,
  u.full_name,
  u.created_at,
  u.last_login,
  c.title,
  c2.name,
  cu.accomplished_at,
  c.serial,
  pgm.status,
  pgm.partner_group_serial