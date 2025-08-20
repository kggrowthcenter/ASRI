import streamlit as st
import pandas as pd
import altair as alt
from data_processing import finalize_data
from navigation import make_sidebar
import datetime

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


min_date = df_lestari['enroll_date'].min().date()
max_date = df_lestari['enroll_date'].max().date()

# Tentukan default state
if "from_date" not in st.session_state:
    st.session_state.from_date = min_date
if "to_date" not in st.session_state:
    st.session_state.to_date = max_date

st.markdown("##### 📅 Filter Tanggal Enrollment")
start_date, end_date = st.date_input(
    "Rentang Tanggal",
    [st.session_state.from_date, st.session_state.to_date],  # ⬅️ bind ke session_state
    min_value=min_date,
    max_value=max_date
)

# Update session_state kalau user ubah manual di date_input
st.session_state.from_date = start_date
st.session_state.to_date = end_date

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Lifetime"):
        st.session_state.from_date = min_date
        st.session_state.to_date = max_date
with col2:
    if st.button("This Month"):
        today = datetime.datetime.now().date()
        st.session_state.from_date = datetime.date(today.year, today.month, 1)
        st.session_state.to_date = today
with col3:
    if st.button("📍 Today"):
        today = datetime.datetime.now().date()
        st.session_state.from_date = today
        st.session_state.to_date = today

# 🎯 Filter berdasarkan title
st.markdown("##### 📖 Filter Title")
all_titles = df_lestari['title'].dropna().unique().tolist()
selected_titles = st.multiselect(
    "Pilih Title", 
    options=all_titles, 
    default=[], 
    key="title_filter"
)

# Mask enroll_date (null tetap ikut)
mask = (
    (
        # enroll_date masuk rentang
        (df_lestari['enroll_date'].dt.date >= st.session_state.from_date) &
        (df_lestari['enroll_date'].dt.date <= st.session_state.to_date)
    )
    | (df_lestari['enroll_date'].isna())  # enroll_date kosong tetap ikut
    | (  # tambahan: regis_date juga difilter
        (df_lestari['regis_date'].dt.date >= st.session_state.from_date) &
        (df_lestari['regis_date'].dt.date <= st.session_state.to_date)
    )
)


if selected_titles:
    mask = mask & (df_lestari['title'].isin(selected_titles))

filtered_df = df_lestari[mask]





st.divider()
# Validasi kolom wajib
if all(col in filtered_df.columns for col in ['duration', 'progress', 'email']):
    
    # Ringkasan metrik
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Jumlah Registered", filtered_df['serial'].nunique())
    col2.metric("✍🏻 Jumlah Unq Enrollment", filtered_df[filtered_df['enroll_date'].notnull()]['serial'].nunique())
    col3.metric("📈 Rata-rata Progress", f"{filtered_df['progress'].mean():.2f}%")
    col4.metric("⏱️ Total Durasi Belajar", f"{filtered_df['duration_jam'].sum():.2f} jam")
    # ============================
    st.subheader("📊 Aktivitas Harian")

    with st.expander("📆 Tabel Harian"):

        # Pastikan dalam format date
        filtered_df['regis_date'] = pd.to_datetime(filtered_df['regis_date']).dt.date
        filtered_df['first_enroll'] = pd.to_datetime(filtered_df['first_enroll']).dt.date

        # Buat range tanggal lengkap dari rentang filter
        date_range = pd.date_range(start=start_date, end=end_date).date
        full_dates = pd.DataFrame({'Tanggal': date_range})

        # Agregasi jumlah pendaftar
        reg_df = filtered_df.groupby('regis_date')['serial'].nunique().reset_index()
        reg_df = reg_df.rename(columns={'regis_date': 'Tanggal', 'serial': 'jumlah_registered'})

        # Agregasi jumlah enrollment
        enroll_df = filtered_df.groupby('first_enroll')['serial'].nunique().reset_index()
        enroll_df = enroll_df.rename(columns={'first_enroll': 'Tanggal', 'serial': 'jumlah_enrollment'})

        # Gabungkan ke tanggal lengkap
        daily_summary = full_dates \
            .merge(reg_df, on='Tanggal', how='left') \
            .merge(enroll_df, on='Tanggal', how='left') \
            .fillna(0)

        # Pastikan integer
        daily_summary['jumlah_registered'] = daily_summary['jumlah_registered'].astype(int)
        daily_summary['jumlah_enrollment'] = daily_summary['jumlah_enrollment'].astype(int)

        st.dataframe(daily_summary)



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


















