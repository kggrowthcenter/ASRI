select u.email, u.full_name, MAX(cu.created_at), MAX(cu.updated_at), c.title, ROUND(SUM(cup.progress_duration),0), AVG(cup.progress_percentage)
from course_users cu
left join courses c on cu.course_serial = c.serial 
left join users u on cu.user_serial = u.serial 
left join partner_groups pg on cu.partner_group_serial = pg.serial
left join course_user_progress cup on cup.course_serial = c.serial and cup.user_serial = u.serial
group by u.email, u.full_name, c.title 