import streamlit as st
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko
from io import StringIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import toml

# Function to connect to ID via SSH tunnel and fetch data
@st.cache_resource(ttl=86400)
def fetch_data_id():
    try:
        # Load the private key content from secrets for ID
        private_key_content = st.secrets["key_id"]["id_rsa_streamlit"]
        private_key_passphrase = st.secrets["ssh_id"].get("private_key_passphrase")
        
        # Create an RSA key object from the private key content for ID
        private_key_file = StringIO(private_key_content)
        private_key = paramiko.RSAKey.from_private_key(private_key_file, password=private_key_passphrase)

        with SSHTunnelForwarder(
            (st.secrets["ssh_id"]["host"], st.secrets["ssh_id"]["port"]),
            ssh_username=st.secrets["ssh_id"]["username"],
            ssh_pkey=private_key,
            remote_bind_address=(st.secrets["id"]["host"], st.secrets["id"]["port"]),
        ) as tunnel:
            connection_kwargs = {
                'host': '127.0.0.1',
                'port': tunnel.local_bind_port if tunnel.is_active else st.secrets["id"]["port"],
                'user': st.secrets["id"]["user"],
                'password': st.secrets["id"]["password"],
                'database': st.secrets["id"]["database"],
                'cursorclass': pymysql.cursors.DictCursor,
            }
            conn = pymysql.connect(**connection_kwargs)

            with open('query_asri.sql', 'r') as sql_file:
                query = sql_file.read()

            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"An error occurred while fetching data from ID: {e}")
        return pd.DataFrame()



