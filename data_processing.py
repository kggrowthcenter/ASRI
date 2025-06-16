import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_asri, fetch_data_lestari, fetch_creds

@st.cache_data(ttl=86400)
def finalize_data_asri():
    df_asri = fetch_data_asri()
    df_asri['tanggal_daftar'] = pd.to_datetime(df_asri['tanggal_daftar'], format="%Y-%m-%d").dt.date
    return df_asri

@st.cache_data(ttl=86400)
def finalize_data_lestari():
    df_lestari = fetch_data_lestari()
    df_lestari['last_update'] = pd.to_datetime(df_lestari['last_update'], format="%Y-%m-%d").dt.date
    return df_lestari

@st.cache_data(ttl=86400)
def finalize_data():
    df_asri = finalize_data_asri()
    df_lestari = finalize_data_lestari()
    df_creds = fetch_creds()

    return df_asri, df_lestari, df_creds
