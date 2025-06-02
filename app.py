import streamlit as st
import pandas as pd
import numpy as np
from fetch_data import fetch_data_id

df = fetch_data_id()
st.dataframe(df)

#nanti di buat 2 page ASRI
#1. Registrasi 
#2. Progress
#nanti ada page buat Lestari Academy
#2 tab : regis dan progress
