import streamlit as st
import pandas as pd
import psycopg
from dotenv import load_dotenv
import os

# Load DB connection from .env
load_dotenv()
dbconn = os.getenv("DBCONN")

# Title
st.title("📊 Crypto Prices Dashboard")

# Connect to Supabase PostgreSQL
conn = psycopg.connect(dbconn)
cur = conn.cursor()

# Fetch data
cur.execute("SELECT * FROM crypto_prices ORDER BY date;")
rows = cur.fetchall()
columns = ["date", "open", "high", "low", "close", "volume"]

# Create DataFrame
df = pd.DataFrame(rows, columns=columns)

# Convert date to datetime for plotting
df["date"] = pd.to_datetime(df["date"])

# Show table
st.subheader("📋 Table: Crypto Prices Over Time")
st.dataframe(df)

# Line chart
st.subheader("📈 Line Chart: Open and Close Prices Over Time")
st.line_chart(df.set_index("date")[["open", "close"]])

# Stats
st.subheader("📊 Descriptive Statistics")
st.write(df[["open", "close", "high", "low", "volume"]].describe())

# Close DB connection
cur.close()
conn.close()
