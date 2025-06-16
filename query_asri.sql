select 
cp.created_at as tanggal_daftar,
cp.first_name as nama_pendaftar, 
cp.email as email,
cp.`role` as role_pendaftar, 
cp.school_name, 
cp.school_address, 
cp.school_city, 
cp.school_district, 
cp.school_subdistrict, 
cp.school_province,
cpm.`role` as role_terdaftar, 
cpm.grade, 
cpm.full_name as nama_terdaftar
from competition_participants cp 
left join competition_participant_members cpm on cpm.competition_participant_serial = cp.serial
