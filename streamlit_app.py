import streamlit as st
import streamlit_authenticator as stauth
from time import sleep
from data_processing import finalize_data
from navigation import make_sidebar
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
    page_title="Lestari Academy Dashboard",
    page_icon="🍀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔥 Hapus seluruh sidebar (saat login screen) & title bawaan sidebar
#hide_sidebar_total = """
    #<style>
        #[data-testid="stSidebar"] { display: none !important; }
        #[data-testid="collapsedControl"] { display: none !important; }
    #</style>
#"""
# 🔥 Hapus judul "streamlit app", "ASRI", "LESTARI" di sidebar
#hide_sidebar_nav_title = """
    #<style>
        #[data-testid="stSidebarNav"] > div:first-child {
            #display: none !important;
        #}
    #</style>
#"""
#st.markdown(hide_sidebar_nav_title, unsafe_allow_html=True)

# Load data
df_asri, df_lestari, df_creds = finalize_data()

# Extract credentials
def extract_credentials(df_creds):
    credentials = {
        "credentials": {"usernames": {}},
        "cookie": {
            "name": "growth_center",
            "key": "growth_2024",
            "expiry_days": 30,
        },
    }
    for _, row in df_creds.iterrows():
        credentials["credentials"]["usernames"][row["username"]] = {
            "name": row["username"],
            "password": row["password"],
            "email": row["email"],
        }
    return credentials

credentials = extract_credentials(df_creds)

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials["credentials"],
    credentials["cookie"]["name"],
    credentials["cookie"]["key"],
    credentials["cookie"]["expiry_days"],
    auto_hash=False,
)

# ⛔ Jangan tampilkan sidebar kalau belum login
#if not st.session_state.get("authentication_status"):
    #st.markdown(hide_sidebar_total, unsafe_allow_html=True)

if st.session_state.get("logged_in", False):
    make_sidebar()

# Halaman utama
st.title("🍀 Dashboard Asri")
authenticator.login('main')

# ✅ Jika sudah login, tampilkan sidebar custom
if st.session_state.get('login_success_message', False):
    st.success("✅ **Logged in successfully! Go to the sidebar on the left!**")

    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWFmYTFua3huM21lZmx5dWR2dXEwOHFwMHFzbTNja3N6emlqYzBoYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Z9UdKXe7bD8i4/giphy.gif" 
                 alt="Run to Sidebar" width="300">
            <p style="font-size: 18px; color: green;"><strong>👉 Ayo ke sidebar sekarang!</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )





# 🔴 Feedback salah login
elif st.session_state.get("authentication_status") is False:
    st.error("Incorrect username or password.")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password to log in.")
