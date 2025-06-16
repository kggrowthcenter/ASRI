from navigation import make_sidebar
import streamlit as st
import pandas as pd
import numpy as np
from data_processing import finalize_data
import altair as alt
import io


st.set_page_config(page_title="Lestari Academy Dashboard", layout="wide")


make_sidebar()



# Fetch data
df_asri, df_lestari, df_creds = finalize_data()

st.title("🎓 Lestari Academy Dashboard")
tab1 = st.tabs(["📊 Progress User"])

# Pastikan kolom 'duration' dan 'progress' ada
if 'duration' in df_lestari.columns and 'progress' in df_lestari.columns:
    # Ubah durasi dari detik ke jam
    df_lestari['duration_jam'] = df_lestari['duration'] / 3600

    st.markdown("Halaman ini menampilkan **progress pembelajaran** pengguna serta durasi belajar mereka dalam **jam**.")

    # Statistik ringkas
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah User", df_lestari['user_id'].nunique() if 'user_id' in df_lestari.columns else df_lestari.shape[0])
    col2.metric("Rata-rata Progress", f"{df_lestari['progress'].mean():.2f}%")
    col3.metric("Total Durasi (jam)", f"{df_lestari['duration_jam'].sum():.2f}")

    # Tampilkan data
    st.write("📄 Detail Data User")
    st.dataframe(df_lestari)

else:
    st.error("Data tidak memiliki kolom 'duration' atau 'progress'. Harap periksa sumber data.")
