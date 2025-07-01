from navigation import make_sidebar, make_filter
import streamlit as st
import pandas as pd
import numpy as np
from data_processing import finalize_data
import altair as alt

st.set_page_config(page_title="Akademi Sekolah Lestari (ASRI) Dashboard", layout="wide")
# Cek login status

if st.session_state.get("authentication_status"):
    make_sidebar()
if not st.session_state.get("authentication_status"):
    st.error("⛔ You must log in to access this page.")
    st.stop()
# Fetch data
df_asri, _, _ = finalize_data()

if 'tanggal_daftar' in df_asri.columns:
    df_asri['tanggal_daftar'] = pd.to_datetime(df_asri['tanggal_daftar'])

# Title
st.title("🎓 Akademi Sekolah Lestari (ASRI) Dashboard")
st.write("📋 Data registrasi untuk monitoring data pendaftar ASRI.")
st.divider()

# Filter Sidebar
columns_list = ['school_name', 'school_city', 'school_province', 'role_pendaftar', 'role_terdaftar']
filtered_df, selected_filters = make_filter(columns_list, df_asri)

# Metrics
#col1, col2, col3 = st.columns(3)
#col1.metric("👤 Jumlah Pendaftar", filtered_df['email'].nunique())
#col2.metric("🏫 Jumlah Sekolah", filtered_df['school_name'].nunique())
#col3.metric("👥 Jumlah Peserta", filtered_df['nama_terdaftar'].nunique())

# Chart 1: Pendaftar per Hari
st.subheader("📈 Jumlah Pendaftar per Hari")
if not filtered_df.empty:
    df_daily = (
        filtered_df.groupby(filtered_df['tanggal_daftar'].dt.date)['email']
        .nunique()
        .reset_index(name='jumlah_pendaftar')
    )
    st.line_chart(df_daily.set_index('tanggal_daftar'))
else:
    st.info("Tidak ada data untuk filter yang dipilih.")


# Chart 2: Horizontal Bar Chart - Role dan Grade
st.subheader("📊 Distribusi Role & Grade")
col1, col2 = st.columns(2)

with col1:
    role_counts = (
        filtered_df.groupby('role_pendaftar')['email']
        .nunique()
        .reset_index()
        .rename(columns={'email': 'Jumlah', 'role_pendaftar': 'Role'})
    )
    role_chart = alt.Chart(role_counts).mark_bar().encode(
        x='Jumlah:Q',
        y=alt.Y('Role:N', sort='-x')
    ).properties(height=300, title='Role Pendaftar (unik email)')
    st.altair_chart(role_chart, use_container_width=True)

with col2:
    grade_counts = (
        filtered_df.dropna(subset=['grade'])
        .groupby('grade')['peserta']
        .nunique()
        .reset_index()
        .rename(columns={'peserta': 'Jumlah', 'grade': 'Grade'})
    )
    grade_chart = alt.Chart(grade_counts).mark_bar().encode(
        x='Jumlah:Q',
        y=alt.Y('Grade:N', sort='-x')
    ).properties(height=300, title='Grade Peserta')
    st.altair_chart(grade_chart, use_container_width=True)


# Distribusi Wilayah
st.subheader("🗺️ Tabel Distribusi Wilayah")
col1, col2, col3 = st.columns(3)

# --- Col1: Provinsi Sekolah, hitung jumlah sekolah ---
with col1:
    st.write("Provinsi Sekolah")
    prov_counts = filtered_df.groupby('school_province')['school_name'].nunique().reset_index()
    prov_counts.columns = ['Provinsi', 'Jumlah Sekolah']
    st.dataframe(prov_counts, height=220)

# --- Col2: Kota Sekolah, hitung jumlah sekolah ---
with col2:
    st.write("Kota Sekolah")
    city_counts = filtered_df.groupby('school_city')['school_name'].nunique().reset_index()
    city_counts.columns = ['Kota', 'Jumlah Sekolah']
    st.dataframe(city_counts, height=220)

# --- Col3: Sekolah, jumlah nama terdaftar per role ---
with col3:
    st.write("Nama Sekolah")
    school_roles = (
        filtered_df.groupby(['school_name', 'role_peserta'])['serial_cpm']
        .nunique()
        .reset_index()
        .pivot(index='school_name', columns='role_peserta', values='serial_cpm')
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    st.dataframe(school_roles, height=220)

df_pendaftar = filtered_df[pendaftar_cols]

# Expandable Data Tables
with st.expander("📄 Lihat Data Pendaftar"):
    pendaftar_cols = [
        'tanggal_daftar', 'nama_pendaftar', 'email', 'no_tlp',
        'role_terdaftar', 'school_name', 'school_address',
        'school_city', 'school_district', 'school_subdistrict', 'school_province'
    ]
    df_pendaftar = filtered_df[pendaftar_cols]
    st.dataframe(df_pendaftar)

with st.expander("📄 Lihat Data Peserta"):
    peserta_cols = ['role_peserta', 'grade', 'peserta', 'no_tlp_student', 'school_name']
    df_peserta = filtered_df[peserta_cols]
    st.dataframe(df_peserta)

# Button update data
if st.button("🔄 Update Data"):
    st.experimental_rerun()


# Unduh data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Unduh Data CSV", data=csv, file_name="data_pendaftar_asri.csv", mime='text/csv')
