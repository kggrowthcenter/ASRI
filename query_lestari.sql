select 
u.email as email, 
u.full_name as name, 
MAX(cu.created_at) as enroll_date, 
MAX(cu.updated_at) as last_update, 
c.title as title, 
c2.name as category,
ROUND(SUM(cup.progress_duration),0) as duration, 
AVG(cup.progress_percentage) as progress
from course_users cu
left join courses c on cu.course_serial = c.serial 
left join users u on cu.user_serial = u.serial 
left join partner_groups pg on cu.partner_group_serial = pg.serial
left join course_user_progress cup on cup.course_serial = c.serial and cup.user_serial = u.serial
left join categories c2 on c2.serial  = c.category_serial 
group by u.email, u.full_name, c.title, c2.name 
