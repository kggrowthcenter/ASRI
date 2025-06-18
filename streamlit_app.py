import streamlit as st
import streamlit_authenticator as stauth
from data_processing import finalize_data
from navigation import render_sidebar
from datetime import datetime

st.set_page_config(
    page_title="Lestari Academy Dashboard",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Login UI
authenticator.login('main')

# Setelah login berhasil
if st.session_state.get("authentication_status"):
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = True
        st.success("Logged in successfully")
        st.session_state["page"] = "registration"

    render_sidebar()  # Sidebar navigasi

    # Routing manual
    if st.session_state["page"] == "registration":
        from screens import asri
        asri.show(df_asri)
    elif st.session_state["page"] == "progress":
        from screens import lestari
        lestari.show(df_lestari)
else:
    if st.session_state.get("authentication_status") is False:
        st.error("Incorrect username or password.")
    elif st.session_state.get("authentication_status") is None:
        st.warning("Please enter your username and password.")
