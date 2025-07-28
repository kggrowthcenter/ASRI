import streamlit as st
import pandas as pd
import altair as alt
from data_processing import finalize_data
from navigation import make_sidebar

st.set_page_config(page_title="Lestari Academy Dashboard", layout="wide")

# Autentikasi
if st.session_state.get("authentication_status"):
    make_sidebar()
else:
    st.switch_page("streamlit_app.py")

# Fetch data
_, df_lestari, _ = finalize_data()

# Konversi durasi belajar
df_lestari['duration_jam'] = df_lestari['duration'] / 3600

# Filter tanggal berdasarkan enroll_date
st.title("🌱 Lestari Academy Dashboard")
st.write("📚 Dashboard ini menampilkan data aktivitas user selama pembelajaran.")
st.divider()

min_date = df_lestari['enroll_date'].min().date()
max_date = df_lestari['enroll_date'].max().date()

st.subheader("📅 Filter Tanggal Enrollment")
start_date, end_date = st.date_input("Rentang Tanggal", [min_date, max_date])

filtered_df = df_lestari[
    (df_lestari['enroll_date'] >= pd.to_datetime(start_date)) &
    (df_lestari['enroll_date'] <= pd.to_datetime(end_date))
].copy()

# Validasi kolom wajib
if all(col in filtered_df.columns for col in ['duration', 'progress', 'email']):
    
    # Ringkasan metrik
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Jumlah Registered", filtered_df['serial'].nunique())
    col2.metric("✅ Jumlah Enrollment", filtered_df[filtered_df['enroll_date'].notnull()]['serial'].nunique())
    col3.metric("📈 Rata-rata Progress", f"{filtered_df['progress'].mean():.2f}%")
    col4.metric("⏱️ Total Durasi Belajar", f"{filtered_df['duration_jam'].sum():.2f} jam")

    # ============================
    # Top Title dan Top Category
    # ============================
    st.subheader("🏆 Aktivitas User")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📘 Top Title**")
        if 'title' in filtered_df.columns:
            top_title = (
                filtered_df.groupby('title')['email']
                .nunique()
                .reset_index(name='Jumlah Pengguna')
                .sort_values(by='Jumlah Pengguna', ascending=False)
                .head(10)
            )
            st.dataframe(top_title, use_container_width=True, hide_index=True)
        else:
            st.warning("Kolom `title` tidak ditemukan.")

    with col2:
        st.markdown("**🗂️ Top Category**")
        if 'category' in filtered_df.columns:
            top_category = (
                filtered_df.groupby('category')['email']
                .nunique()
                .reset_index(name='Jumlah Pengguna')
                .sort_values(by='Jumlah Pengguna', ascending=False)
                .head(10)
            )
            st.dataframe(top_category, use_container_width=True, hide_index=True)
        else:
            st.warning("Kolom `category` tidak ditemukan.")

    # ============================
    # Tabel Harian First Enroll
    # ============================
    st.subheader("📊 Aktivitas Harian Berdasarkan First Enroll")
    with st.expander("📆 Tabel Harian"):
        filtered_df['first_enroll'] = pd.to_datetime(filtered_df['first_enroll']).dt.date
        daily_summary = filtered_df.groupby('first_enroll').agg(
            jumlah_registered=('serial', 'nunique'),
            jumlah_enrollment=('first_enroll', 'nunique')
        ).reset_index().rename(columns={'first_enroll': 'Tanggal'})
        st.table(daily_summary)

    # ============================
    # Tabel Detail dan Unduh
    # ============================
    st.divider()
    with st.expander("📄 Lihat Data Detail"):
        st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh Data CSV", data=csv, file_name="data_user_lestari.csv", mime='text/csv')

else:
    st.error("Data tidak memiliki kolom 'duration', 'progress', atau 'email'. Harap periksa sumber data.")
