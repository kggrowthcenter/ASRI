import streamlit as st
st.set_page_config(page_title="Akademi Sekolah Lestari (ASRI) Dashboard", layout="wide")
import pandas as pd
import numpy as np
from fetch_data import fetch_data_id

# Fetch data
df = fetch_data_id()

# Set page title
st.title("🎓 Akademi Sekolah Lestari (ASRI) Dashboard")

# Tabs
tab1, tab2 = st.tabs(["📝 Registration", "📊 Progress"])

# --- Registration Tab ---
with tab1:
    st.subheader("📝 Data Pendaftaran")
    if not df.empty:
        if 'user_id' in df.columns:
            st.metric("Jumlah User Terdaftar", df['user_id'].nunique())
        st.dataframe(df)
    else:
        st.warning("Data tidak ditemukan.")

# --- Progress Tab ---
with tab2:
    st.subheader("📊 Progress Pembelajaran")

    if 'duration' in df.columns and 'progress' in df.columns:
        df['duration_jam'] = df['duration'] / 3600

        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah User", df['user_id'].nunique() if 'user_id' in df.columns else df.shape[0])
        col2.metric("Rata-rata Progress", f"{df['progress'].mean():.2f}%")
        col3.metric("Total Durasi (jam)", f"{df['duration_jam'].sum():.2f}")

        st.write("📄 Detail Data Progress")
        st.dataframe(df)

    else:
        st.error("Data tidak memiliki kolom 'duration' atau 'progress'. Harap periksa sumber data.")
