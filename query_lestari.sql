SELECT
  u.serial AS serial,
  u.email AS email,
  u.full_name AS name,
  u.created_at AS regis_date,
  u.last_login AS last_login,
  MAX(cu.created_at) AS enroll_date,
  MAX(cu.updated_at) AS last_update,
  c.title AS title,
  c2.name AS category,
  ROUND(SUM(cup.progress_duration), 0) AS duration,
  AVG(cup.progress_percentage) AS progress,
  CASE
    WHEN cu.accomplished_at IS NULL THEN 'In Progress'
    ELSE 'Finished'
  END AS course_status,
  CASE
    WHEN c.serial = 'COURSE-000137' THEN 14276.7599182128
    WHEN c.serial = 'COURSE-000096' THEN 2919
    WHEN c.serial = 'COURSE-000085' THEN 2290
    WHEN c.serial = 'COURSE-000110' THEN 3288
    WHEN c.serial = 'COURSE-000141' THEN 3689
    WHEN c.serial = 'COURSE-X4S92F0RZM' THEN 15.448766708374
    WHEN c.serial = 'COURSE-PXS4RLNBU4' THEN 1852.23999023437
    WHEN c.serial = 'COURSE-3EOCVZW6OS' THEN 2071.35998153686
    WHEN c.serial = 'COURSE-UN09Y42LTX' THEN 1955.56000518798
    WHEN c.serial = 'COURSE-4FIK9YIX9A' THEN 2058.91996765136
    WHEN c.serial = 'COURSE-KTEA8IDKHT' THEN 1694.625
    WHEN c.serial = 'COURSE-8EF72DXFAH' THEN 1830.60000610351
    WHEN c.serial = 'COURSE-316JWHWZO4' THEN 2340.79995727539
  END AS total_duration,
  pgm.status AS playlist_status
FROM users u
LEFT JOIN course_user_progress cup ON u.serial = cup.user_serial
LEFT JOIN courses c ON cup.course_serial = c.serial
LEFT JOIN course_sections cs ON cup.course_section_serial = cs.serial
LEFT JOIN course_contents cc ON cup.course_content_serial = cc.serial
LEFT JOIN course_user_quiz_answers cuqa ON cuqa.course_content_serial = cup.course_content_serial AND cuqa.user_serial = cup.user_serial
LEFT JOIN course_users cu ON cu.course_serial = cup.course_serial AND cu.user_serial = cup.user_serial
LEFT JOIN partner_playlists pp ON cup.partner_playlist_serial = pp.serial
LEFT JOIN partner_group_members pgm ON cup.user_serial = pgm.user_serial AND cup.partner_group_serial = pgm.partner_group_serial
LEFT JOIN categories c2 ON c2.serial = c.category_serial
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
  pgm.status
ORDER BY regis_date DESC;
