import streamlit as st
from time import sleep
import pandas as pd

# Build sidebar hanya jika user sudah login
def make_sidebar():
    if st.session_state.get("authentication_status"):  # ⛔ Pastikan sudah login
        with st.sidebar:
            st.page_link("pages/1_ASRI.py", label="🎓 Registration")
            st.page_link("pages/2_LESTARI.py", label="📚 Progress")
            if st.button("🚪 Log out", key="logout_button"):
                st.session_state.authentication_status = None
                st.session_state.username = None
                st.session_state.logged_in = False
                st.rerun()

# Fungsi logout terpisah (kalau butuh redirect khusus)
def logout():
    st.session_state.authentication_status = None
    st.session_state.username = None
    st.session_state.logged_in = False
    st.success("Logged out")
    sleep(0.5)
    st.switch_page("streamlit_app.py")

# Fungsi filter builder opsional
def make_filter(columns_list, df_asri):
    filter_columns = st.multiselect(
        'Filter the data (optional):',
        options=columns_list,
        format_func=lambda x: x.capitalize(),
        key="filter_columns_selector"
    )

    filtered_data = df_asri.copy()
    selected_filters = []

    for i, filter_col in enumerate(filter_columns):
        selected_filter_value = st.multiselect(
            f'Select {filter_col.capitalize()} to filter the data:',
            options=filtered_data[filter_col].dropna().unique(),
            key=f'filter_{filter_col}_{i}'
        )

        if selected_filter_value:
            filtered_data = filtered_data[filtered_data[filter_col].isin(selected_filter_value)]
            selected_filters.append(f"{filter_col.capitalize()}: {', '.join(selected_filter_value)}")

    return filtered_data, selected_filters
