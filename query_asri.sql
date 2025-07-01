select 
cp.created_at as tanggal_daftar,
cp.updated_at as last_update,
cp.serial as serial_cp,
cp.first_name as nama_pendaftar, 
cp.email as email,
cp.phone_number as no_tlp,
cp.`role` as role_pendaftar, 
cp.school_name, 
cp.school_address, 
cp.school_city, 
cp.school_district, 
cp.school_subdistrict, 
cp.school_province,
cpm.serial as serial_cpm,
cpm.`role` as role_peserta, 
cpm.grade as grade, 
cpm.full_name as peserta,
cpm.phone_number as no_tlp_student
from competition_participants cp 
left join competition_participant_members cpm on cpm.competition_participant_serial = cp.serial
