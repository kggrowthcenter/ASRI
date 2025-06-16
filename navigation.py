# navigation.py
import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
import pandas as pd

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")
    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    with st.sidebar:
        st.title("Navigasi")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/1_ASRI.py", label="🎓 ASRI")
            st.page_link("pages/2_LESTARI.py", label="🌎 Lestari")
            st.divider()

            if st.button("🚪 Log out", key="logout_button"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            st.switch_page("streamlit_app.py")

def logout():
    st.session_state.logged_in = False
    st.success("Logged out")
    sleep(0.5)
    st.switch_page("streamlit_app.py")

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
