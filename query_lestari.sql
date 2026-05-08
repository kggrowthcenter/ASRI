WITH progress_summary AS (
    SELECT
        cup.user_serial,
        cup.course_serial,
        MAX(cup.updated_at) AS last_update,
        COUNT(DISTINCT CASE
            WHEN cup.is_accomplished = 1
            THEN cup.course_content_serial
        END) AS accomplished,
        ROUND(SUM(cup.progress_duration), 0) AS duration
    FROM course_user_progress cup
    GROUP BY
        cup.user_serial,
        cup.course_serial
)

SELECT
    u.serial,
    u.email,
    u.full_name AS name,
    u.created_at AS regis_date,
    u.last_login,

    cu.created_at AS enroll_date,

    ps.last_update,

    c.title,
    c2.name AS category,

    COALESCE(ps.accomplished, 0) AS accomplished,
    COALESCE(ps.duration, 0) AS duration,

    pgm.status AS playlist_status,
    cu.partner_group_serial,

    CASE
        WHEN cu.partner_group_serial IS NOT NULL
            THEN 'Playlist Invitation'
        ELSE 'Organic'
    END AS registration_type

FROM users u

LEFT JOIN course_users cu
    ON cu.user_serial = u.serial

LEFT JOIN partner_group_members pgm
    ON pgm.user_serial = cu.user_serial
    AND pgm.partner_group_serial = cu.partner_group_serial

LEFT JOIN courses c
    ON c.serial = cu.course_serial

LEFT JOIN categories c2
    ON c2.serial = c.category_serial

LEFT JOIN progress_summary ps
    ON ps.user_serial = cu.user_serial
    AND ps.course_serial = cu.course_serial
;