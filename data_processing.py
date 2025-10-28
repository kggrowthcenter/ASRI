import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_asri, fetch_data_lestari, fetch_data_course, fetch_creds, fetch_data_quiz

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
    df_course = fetch_data_course()       # total content per course
    df_quiz = fetch_data_quiz()
    df_creds = fetch_creds()

    # Merge df_lestari with df_course to get total contents per course
    df_lestari = df_lestari.merge(
        df_course.rename(columns={'title': 'title', 'COUNT(DISTINCT cc.serial)': 'total_content'}),
        on='title',
        how='left'
    )

    # Compute progress %
    df_lestari['progress'] = (df_lestari['accomplished'] / df_lestari['total_content']) * 100

    # ======================================================
    # ADDING ONLY PRE-TEST & POST-TEST SCORES + STATUS
    # ======================================================
    df_quiz = df_quiz.rename(columns={
        'u.email': 'email',
        'c.title': 'title',
        'cc.title': 'quiz_type',
        'cup.score': 'score',
        'u.full_name': 'name',
        'cup.created_at': 'created_at',
        'cup.updated_at': 'updated_at'
    })

    # Keep only Pre-Test and Post-Test
    df_quiz = df_quiz[df_quiz['quiz_type'].isin(['Pre-Test', 'Post-Test'])]

    # Add status column
    df_quiz['status'] = df_quiz.apply(
        lambda row: 'Not Retaken' if row['created_at'] == row['updated_at'] else 'Retaken',
        axis=1
    )

    # Pivot scores
    df_scores = (
        df_quiz.pivot_table(index=['email', 'title'], columns='quiz_type', values='score', aggfunc='max')
        .reset_index()
        .rename_axis(None, axis=1)
    )

    # Pivot status
    df_status = (
        df_quiz.pivot_table(index=['email', 'title'], columns='quiz_type', values='status', aggfunc='first')
        .reset_index()
        .rename_axis(None, axis=1)
    )
    df_status = df_status.rename(columns={'Pre-Test': 'Pre-Test Status', 'Post-Test': 'Post-Test Status'})

    # Merge scores and status
    df_quiz_final = df_scores.merge(df_status, on=['email', 'title'], how='left')

    # Merge into df_lestari
    df_lestari = df_lestari.merge(df_quiz_final, on=['email', 'title'], how='left')

    # Reorder columns: original + Pre-Test, Post-Test, Pre-Test Status, Post-Test Status
    cols = [c for c in df_lestari.columns if c not in ['Pre-Test', 'Post-Test', 'Pre-Test Status', 'Post-Test Status']] + \
           ['Pre-Test', 'Post-Test', 'Pre-Test Status', 'Post-Test Status']
    df_lestari = df_lestari[cols]

    return df_asri, df_lestari, df_creds





