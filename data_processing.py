import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_asri, fetch_data_lestari, fetch_data_course, fetch_creds

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
    df_lestari['last_login'] = pd.to_datetime(df_lestari['last_login'], utc=True).dt.tz_convert('Asia/Jakarta').dt.tz_localize(None)
    df_lestari['first_enroll'] = df_lestari.groupby('serial')['enroll_date'].transform('min')
    df_lestari = df_lestari[df_lestari['title'] != '99 Test Dummy Course']
    return df_lestari


@st.cache_data(ttl=1800)
def finalize_data():
    df_asri = finalize_data_asri()
    df_lestari = finalize_data_lestari()  # user activity
    df_course = fetch_data_course()      # total content per course
    df_creds = fetch_creds()

    # Merge df_lestari with df_course to get total contents per course
    df_lestari = df_lestari.merge(
        df_course.rename(columns={'title': 'title', 'COUNT(DISTINCT cc.serial)': 'total_content'}),
        on='title',
        how='left'
    )

    # Compute progress %
    df_lestari['progress'] = (df_lestari['accomplished'] / df_lestari['total_content']) * 100

    return df_asri, df_lestari, df_creds




