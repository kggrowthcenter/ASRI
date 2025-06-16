import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from data_processing import finalize_data
from navigation import make_sidebar

st.set_page_config(page_title="Lestari Academy Dashboard", layout="wide")

# Cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

make_sidebar()

# Fetch data
_, df_lestari, _ = finalize_data()

# Title
st.title("🌱 Lestari Academy Dashboard")
st.write("📚 Dashboard ini menampilkan data aktivitas pengguna selama pembelajaran.")
st.divider()

# Validasi kolom wajib
if 'duration' in df_lestari.columns and 'progress' in df_lestari.columns and 'email' in df_lestari.columns:
    df_lestari['duration_jam'] = df_lestari['duration'] / 3600  # Ubah detik ke jam

    # Ringkasan metrik
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Jumlah User", df_lestari['email'].nunique())
    col2.metric("📈 Rata-rata Progress", f"{df_lestari['progress'].mean():.2f}%")
    col3.metric("⏱️ Total Durasi Belajar", f"{df_lestari['duration_jam'].sum():.2f} jam")

    st.divider()

    # Top Durasi Belajar
    st.subheader("🏆 Top Durasi Belajar")
    top_durasi = df_lestari[['email', 'duration_jam']].copy()
    top_durasi = top_durasi.groupby('email').sum().reset_index().sort_values(by='duration_jam', ascending=False).head(10)
    top_durasi['duration_jam'] = top_durasi['duration_jam'].round(2)
    st.dataframe(top_durasi, use_container_width=True)

    # Top Progress Belajar
    st.subheader("📊 Top Progress Belajar")
    top_progress = df_lestari[['email', 'progress']].copy()
    top_progress = top_progress.groupby('email').mean().reset_index().sort_values(by='progress', ascending=False).head(10)
    top_progress['progress'] = top_progress['progress'].round(2)

    col1, col2 = st.columns(2)
    with col1:
        st.write("📧 Email")
        st.dataframe(top_progress[['email']])

    with col2:
        st.write("📈 Progress (%)")
        st.dataframe(top_progress[['progress']])

    st.divider()

    # Expandable Table
    with st.expander("📄 Lihat Data Detail"):
        st.dataframe(df_lestari)

    # Download
    csv = df_lestari.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh Data CSV", data=csv, file_name="data_user_lestari.csv", mime='text/csv')

else:
    st.error("Data tidak memiliki kolom 'duration', 'progress', atau 'email'. Harap periksa sumber data.")

