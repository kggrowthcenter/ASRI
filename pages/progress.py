import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_id

df = fetch_data_id()
st.dataframe(df)