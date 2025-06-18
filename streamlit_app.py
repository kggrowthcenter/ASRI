import streamlit as st
import streamlit_authenticator as stauth
from time import sleep
from data_processing import finalize_data
from navigation import make_sidebar
from datetime import datetime

# Set page
st.set_page_config(
    page_title="Lestari Academy Dashboard",
    page_icon="🍀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS: Hide sidebar & toggle button total
hide_sidebar_complete = """
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
"""

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

# LOGIN UI
st.title("🍀 Dashboard Asri")
authenticator.login('main')  # ⬅️ Lokasi 'main' aman (utama)
hide_nav_titles = """
    <style>
        [data-testid="stSidebarNav"] > div:first-child {
            display: none;
        }
    </style>
"""
st.markdown(hide_nav_titles, unsafe_allow_html=True)

# Authentication control
if st.session_state.get("authentication_status"):
    if not st.session_state.get("logged_in", False):
        st.session_state["logged_in"] = True
        st.success("Logged in successfully")
    
    make_sidebar()  # ✅ HANYA render sidebar di sini saat login berhasil

else:
    st.markdown(hide_sidebar_complete, unsafe_allow_html=True)  # Hide sidebar total
    if st.session_state.get("authentication_status") is False:
        st.error("Incorrect username or password.")
    elif st.session_state.get("authentication_status") is None:
        st.warning("Please enter your username and password to log in.")
