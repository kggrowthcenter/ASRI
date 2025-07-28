import streamlit as st
from time import sleep
import pandas as pd

# Build sidebar hanya jika user sudah login
def make_sidebar():
    with st.sidebar:
        st.title("Sidebar")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/1_ASRI.py", label="🎓 Registration")
            st.page_link("pages/2_LESTARI.py", label="📚 Progress")

            st.write("")
            st.write("")
            # Button to refresh all cached data
            if st.sidebar.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()

            if st.button("🚪 Log out"):
                logout()
            if st.button("Log out"):
                logout()

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
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
