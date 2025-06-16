import streamlit as st
from time import sleep
from navigation import make_sidebar
import streamlit_authenticator as stauth
from data_processing import finalize_data
import gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Asri Dashboard", page_icon="🍀")
# Hide sidebar completely while on login page
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
df_asri, df_lestari, df_creds = finalize_data()


# Credential extraction
def extract_credentials(df_creds):
    credentials = {
        "credentials": {
            "usernames": {}
        },
        "cookie": {
            "name": "growth_center",
            "key": "growth_2024",
            "expiry_days": 30
        }
    }
    for index, row in df_creds.iterrows():
        credentials['credentials']['usernames'][row['username']] = {
            'name': row['username'],
            'password': row['password'], 
            'email': row['email'],  
        }
    return credentials
# Extract credentials from df_creds
credentials = extract_credentials(df_creds)

# Setup auth
credentials = extract_credentials(df_creds)
authenticator = stauth.Authenticate(
    credentials['credentials'],
    credentials['cookie']['name'],
    credentials['cookie']['key'],
    credentials['cookie']['expiry_days'],
    auto_hash=False
)

# Login
st.title("🍀Dashboard Asri Login")
authenticator.login('main')

# Handle authentication status
if st.session_state.get('authentication_status'):
    st.session_state['logged_in'] = True  # Set session state for logged in
    st.success("Logged in successfully. Go to the Test Result in the sidebar.")
elif st.session_state.get('authentication_status') is False:
    st.error("Incorrect username or password.")
elif st.session_state.get('authentication_status') is None:
    st.warning("Please enter your username and password to log in.")
