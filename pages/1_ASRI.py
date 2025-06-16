from navigation import make_sidebar
import streamlit as st
import pandas as pd
import numpy as np
from data_processing import finalize_data
import altair as alt
import io


st.set_page_config(page_title="Akademi Sekolah Lestari (ASRI) Dashboard", layout="wide")


make_sidebar()


# Fetch data
df_asri, df_lestari, df_creds = finalize_data()

# Format datetime
if 'tanggal_daftar' in df_asri.columns:
    df_asri['tanggal_daftar'] = pd.to_datetime(df_asri['tanggal_daftar'])

# Title
st.title("🎓 Akademi Sekolah Lestari (ASRI) Dashboard")
st.write("📋 data registrasi untuk monitoring data pendaftar ASRI.")
st.divider()

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
selected_province = st.sidebar.selectbox("Provinsi", options=["Semua"] + sorted(df_asri['school_province'].dropna().unique().tolist()))
selected_role = st.sidebar.selectbox("Role Pendaftar", options=["Semua"] + sorted(df_asri['role_pendaftar'].dropna().unique().tolist()))
selected_date_range = st.sidebar.date_input("Rentang Tanggal Daftar", [])

# Filter logic
filtered_df = df_asri.copy()

if selected_province != "Semua":
    filtered_df = filtered_df[filtered_df['school_province'] == selected_province]

if selected_role != "Semua":
    filtered_df = filtered_df[filtered_df['role_pendaftar'] == selected_role]

if len(selected_date_range) == 2:
    start_date, end_date = pd.to_datetime(selected_date_range)
    filtered_df = filtered_df[
        (filtered_df['tanggal_daftar'] >= start_date) & 
        (filtered_df['tanggal_daftar'] <= end_date)
    ]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("👤 Jumlah Pendaftar", filtered_df['email'].nunique())
col2.metric("🏫 Jumlah Sekolah", filtered_df['school_name'].nunique())
col3.metric("👥 Jumlah Peserta", filtered_df['nama_terdaftar'].nunique())

# Chart 1: Pendaftar per Hari
st.subheader("📈 Jumlah Pendaftar per Hari")
if not filtered_df.empty:
    df_daily = filtered_df.groupby(filtered_df['tanggal_daftar'].dt.date).size().reset_index(name='jumlah_pendaftar')
    st.line_chart(df_daily.set_index('tanggal_daftar'))
else:
    st.info("Tidak ada data untuk filter yang dipilih.")

# Chart 2: Horizontal Bar Chart - Role dan Grade
st.subheader("📊 Distribusi Role & Grade")
col1, col2 = st.columns(2)

with col1:
    role_counts = filtered_df['role_pendaftar'].value_counts().reset_index()
    role_counts.columns = ['Role', 'Jumlah']
    role_chart = alt.Chart(role_counts).mark_bar().encode(
        x='Jumlah:Q',
        y=alt.Y('Role:N', sort='-x')
    ).properties(height=300, title='Role Pendaftar')
    st.altair_chart(role_chart, use_container_width=True)

with col2:
    grade_counts = filtered_df['grade'].dropna().value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Jumlah']
    grade_chart = alt.Chart(grade_counts).mark_bar().encode(
        x='Jumlah:Q',
        y=alt.Y('Grade:N', sort='-x')
    ).properties(height=300, title='Grade Peserta')
    st.altair_chart(grade_chart, use_container_width=True)

# Distribusi Provinsi dan Kota sebagai Dataframe
st.subheader("🗺️ Tabel Distribusi Wilayah")
col1, col2 = st.columns(2)

with col1:
    prov_counts = filtered_df['school_province'].value_counts().reset_index()
    prov_counts.columns = ['Provinsi', 'Jumlah']
    st.dataframe(prov_counts)

with col2:
    city_counts = filtered_df['school_city'].value_counts().reset_index()
    city_counts.columns = ['Kota', 'Jumlah']
    st.dataframe(city_counts)

# Expandable Data Table
with st.expander("📄 Lihat Data Pendaftar"):
    st.dataframe(filtered_df)

# Unduh data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Unduh Data CSV", data=csv, file_name="data_pendaftar_asri.csv", mime='text/csv')
