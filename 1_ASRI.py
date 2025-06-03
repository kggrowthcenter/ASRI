import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_id

df = fetch_data_id()

if 'duration' in df.columns and 'progress' in df.columns:
    df['duration_jam'] = df['duration'] / 3600

    st.title("📊 Progress User")
    st.markdown("Halaman ini menampilkan **progress pembelajaran** pengguna serta durasi belajar mereka dalam **jam**.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah User", df['user_id'].nunique() if 'user_id' in df.columns else df.shape[0])
    col2.metric("Rata-rata Progress", f"{df['progress'].mean():.2f}%")
    col3.metric("Total Durasi (jam)", f"{df['duration_jam'].sum():.2f}")

    st.write("📄 Detail Data User")
    st.dataframe(df)

else:
    st.error("Data tidak memiliki kolom 'duration' atau 'progress'. Harap periksa sumber data.")

