import streamlit as st
import streamlit_authenticator as stauth
from time import sleep
from data_processing import finalize_data
from navigation import make_sidebar
from datetime import datetime

st.set_page_config(page_title="Lestari Academy Dashboard", page_icon="🍀", layout="centered", initial_sidebar_state="collapsed")
# Sembunyikan sidebar, termasuk tombol toggle panahnya
hide_sidebar_complete = """
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
"""
st.markdown(hide_sidebar_complete, unsafe_allow_html=True)

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
# Make the sidebar visible only if logged in
if st.session_state.get("logged_in", False):
    make_sidebar()

st.title("🍀 Dashboard Asri")
authenticator.login('main')


# Handle authentication status
if st.session_state.get('authentication_status'):
    st.session_state['logged_in'] = True  # Set session state for logged in
    st.success("Logged in successfully. Go to the Dashboard in the sidebar.")
elif st.session_state.get('authentication_status') is False:
    st.error("Incorrect username or password.")
elif st.session_state.get('authentication_status') is None:
    st.warning("Please enter your username and password to log in.")

