import streamlit as st
import streamlit_authenticator as stauth
from data_processing import finalize_data
from datetime import datetime
from time import sleep

# SET PAGE CONFIG
st.set_page_config(page_title="Asri Dashboard", page_icon="🍀", layout="centered")

# HIDE SIDEBAR
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Load data
df_asri, df_lestari, df_creds = finalize_data()

# Extract credentials
def extract_credentials(df_creds):
    credentials = {
        "credentials": { "usernames": {} },
        "cookie": {
            "name": "growth_center",
            "key": "growth_2024",
            "expiry_days": 30
        }
    }
    for _, row in df_creds.iterrows():
        credentials['credentials']['usernames'][row['username']] = {
            'name': row['username'],
            'password': row['password'],
            'email': row['email'],
        }
    return credentials

credentials = extract_credentials(df_creds)

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials['credentials'],
    credentials['cookie']['name'],
    credentials['cookie']['key'],
    credentials['cookie']['expiry_days'],
    auto_hash=False
)

# Login UI
st.title("🍀 Dashboard Asri Login")
# Hapus stauth, ganti dengan ini:
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    row = df_creds.loc[df_creds['username'] == username]
    if not row.empty and password == row.iloc[0]['password']:
        st.session_state.logged_in = True
        st.success("Login sukses!")
        st.experimental_rerun()
    else:
        st.error("Username/password salah!")

