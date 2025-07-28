import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_asri, fetch_data_lestari, fetch_creds

@st.cache_data(ttl=1800)
def finalize_data_asri():
    df_asri = fetch_data_asri()
    df_asri['tanggal_daftar'] = pd.to_datetime(df_asri['tanggal_daftar'], utc=True).dt.tz_convert('Asia/Jakarta').dt.tz_localize(None)
    df_asri['last_update'] = pd.to_datetime(df_asri['last_update'], utc=True).dt.tz_convert('Asia/Jakarta').dt.tz_localize(None)
    return df_asri

@st.cache_data(ttl=1800)
def finalize_data_lestari():
    df_lestari = fetch_data_lestari()
    df_lestari['regis_date'] = pd.to_datetime(df_lestari['regis_date'], utc=True).dt.tz_convert('Asia/Jakarta').dt.tz_localize(None)
    df_lestari['enroll_date'] = pd.to_datetime(df_lestari['enroll_date'], utc=True).dt.tz_convert('Asia/Jakarta').dt.tz_localize(None)
    df_lestari['last_update'] = pd.to_datetime(df_lestari['last_update'], utc=True).dt.tz_convert('Asia/Jakarta').dt.tz_localize(None)
    df_lestari['first_enroll'] = df_lestari.groupby('serial')['enroll_date'].transform('min')
    return df_lestari

@st.cache_data(ttl=1800)
def finalize_data():
    df_asri = finalize_data_asri()
    df_lestari = finalize_data_lestari()
    df_creds = fetch_creds()

    return df_asri, df_lestari, df_creds
