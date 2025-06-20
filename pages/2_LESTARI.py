import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from data_processing import finalize_data
from navigation import make_sidebar

st.set_page_config(page_title="Lestari Academy Dashboard", layout="wide")

if st.session_state.get("authentication_status"):
    make_sidebar()

# Fetch data
_, df_lestari, _ = finalize_data()

# Title
st.title("🌱 Lestari Academy Dashboard")
st.write("📚 Dashboard ini menampilkan data aktivitas user selama pembelajaran.")
st.divider()

# Validasi kolom wajib
if all(col in df_lestari.columns for col in ['duration', 'progress', 'email']):
    df_lestari['duration_jam'] = df_lestari['duration'] / 3600  # Ubah detik ke jam

    # Ringkasan metrik
    #col1, col2, col3 = st.columns(3)
    #col1.metric("👥 Jumlah User", df_lestari['email'].nunique())
    #col2.metric("📈 Rata-rata Progress", f"{df_lestari['progress'].mean():.2f}%")
    #col3.metric("⏱️ Total Durasi Belajar", f"{df_lestari['duration_jam'].sum():.2f} jam")

    st.divider()

    # ============================
    # Top Title dan Top Category
    # ============================
    st.subheader("🏆 Aktivitas User")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📘 Top Title**")
        if 'title' in df_lestari.columns:
            top_title = (
                df_lestari.groupby('title')['email']
                .nunique()
                .reset_index(name='Jumlah Pengguna')
                .sort_values(by='Jumlah Pengguna', ascending=False)
                .head(10)
            )
            st.dataframe(top_title, use_container_width=True)
        else:
            st.warning("Kolom `title` tidak ditemukan.")

    with col2:
        st.markdown("**🗂️ Top Category**")
        if 'category' in df_lestari.columns:
            top_category = (
                df_lestari.groupby('category')['email']
                .nunique()
                .reset_index(name='Jumlah Pengguna')
                .sort_values(by='Jumlah Pengguna', ascending=False)
                .head(10)
            )
            st.dataframe(top_category, use_container_width=True)
        else:
            st.warning("Kolom `category` tidak ditemukan.")

    st.divider()

    # Expandable Table
    with st.expander("📄 Lihat Data Detail"):
        st.dataframe(df_lestari)

    # Download
    csv = df_lestari.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh Data CSV", data=csv, file_name="data_user_lestari.csv", mime='text/csv')

else:
    st.error("Data tidak memiliki kolom 'duration', 'progress', atau 'email'. Harap periksa sumber data.")
