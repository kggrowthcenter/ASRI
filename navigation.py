import streamlit as st
from time import sleep
import pandas as pd

def make_sidebar():
    with st.sidebar:
        st.title("Sidebar")
        st.write("")
        st.write("")

        # Jika user sudah login
        if st.session_state.get("logged_in", False):
            st.page_link("pages/1_ASRI.py", label="Asri", icon="🎓")
            st.page_link("pages/2_LESTARI.py", label="Lestari", icon="🌎")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        else:
            # Kalau user belum login, tampilkan info (jika ingin)
            st.info("Please log in to access the sidebar.")

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")  # Arahkan kembali ke halaman login

