import streamlit as st
import pandas as pd
import psycopg
from dotenv import load_dotenv
import os

# Streamlit app for Crypto Prices Dashboard
# This app displays crypto prices over time with options to select metrics and visualize them.
# Requirements: streamlit, pandas, psycopg, python-dotenv






# st.title("📈 Crypto Prices Dashboard")

# # Load data from database or CSV
# load_dotenv()
# conn = psycopg.connect(os.getenv("DBCONN"))
# cur = conn.cursor()
# cur.execute("SELECT * FROM crypto_prices ORDER BY date")
# rows = cur.fetchall()
# columns = [desc.name for desc in cur.description]
# df = pd.DataFrame(rows, columns=columns)
# conn.close()

# df["date"] = pd.to_datetime(df["date"])
# df = df.sort_values("date")

# # 🎯 Auswahlmenü für Spalten
# options = ["open", "high", "low", "close", "volume"]
# selected_options = st.multiselect("📌 Select metrics to display:", options, default=["open", "close"])

# # 📋 Zeige Tabelle
# st.subheader("📋 Table: Crypto Prices Over Time")
# st.dataframe(df)

# # 📊 Zeige Diagramm
# if selected_options:
#     st.subheader("📊 Line Chart: Selected Metrics Over Time")
#     st.line_chart(df.set_index("date")[selected_options])
# else:
#     st.warning("⚠️ Please select at least one metric.")

# # 📈 Statistiken
# st.subheader("📊 Descriptive Statistics")
# st.write(df[selected_options].describe())



import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import psycopg
import os
from dotenv import load_dotenv

# Load secrets
load_dotenv()
conn = psycopg.connect(os.getenv("DBCONN"))
cur = conn.cursor()
cur.execute("SELECT * FROM crypto_prices ORDER BY date")
rows = cur.fetchall()
columns = [desc.name for desc in cur.description]
df = pd.DataFrame(rows, columns=columns)
cur.close()
conn.close()

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sidebar dropdown
st.sidebar.title("📌 Choose Data to Display")
selected = st.sidebar.multiselect("Select variables:", ["open", "close", "volume"], default=["close"])

# Plotting
fig = go.Figure()

for col in selected:
    if col == "volume":
        fig.add_trace(go.Scatter(x=df["date"], y=df[col],
                                 name=col.capitalize(),
                                 yaxis="y2",
                                 line=dict(color="orange", dash="dot")))
    else:
        fig.add_trace(go.Scatter(x=df["date"], y=df[col],
                                 name=col.capitalize()))

# Layout
fig.update_layout(
    title="📈 Crypto Prices Over Time",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Price (€)"),
    yaxis2=dict(title="Volume (BTC)", overlaying="y", side="right"),
    legend=dict(x=0, y=1.1, orientation="h"),
    height=500
)

st.plotly_chart(fig, use_container_width=True)






# # 🕯️ Candlestick Chart (Open-High-Low-Close)
# import plotly.graph_objects as go

# fig_candle = go.Figure(data=[
#     go.Candlestick(
#         x=df['date'],
#         open=df['open'],
#         high=df['high'],
#         low=df['low'],
#         close=df['close'],
#         name="OHLC"
#     )
# ])
# fig_candle.update_layout(
#     title="🕯️ Candlestick Chart (OHLC)",
#     xaxis_title="Date",
#     yaxis_title="Price (€)",
#     height=500
# )
# st.plotly_chart(fig_candle, use_container_width=True)


# # 📊 Moving Averages (7 and 30 days)
# df['MA_7'] = df['close'].rolling(window=7).mean()
# df['MA_30'] = df['close'].rolling(window=30).mean()

# st.line_chart(df.set_index('date')[['close', 'MA_7', 'MA_30']])




# # 📉 Daily % Change
# df['pct_change'] = df['close'].pct_change() * 100

# import plotly.express as px
# fig_pct = px.line(df, x='date', y='pct_change', title='📉 Daily % Change (%)')
# st.plotly_chart(fig_pct, use_container_width=True)



# 💰 Investment Simulation
st.sidebar.subheader("💸 Investment Simulator")
start_date = st.sidebar.date_input("Choose start date", value=df['date'].min().date())
investment_amount = st.sidebar.number_input("Investment amount (€)", min_value=100, value=1000)

start_price = df[df['date'].dt.date == start_date]['close'].values
end_price = df['close'].iloc[-1]

if len(start_price) > 0:
    gain = (end_price / start_price[0]) * investment_amount
    st.metric(label="📈 Current Value", value=f"€{gain:,.2f}", delta=f"{(end_price - start_price[0])/start_price[0]*100:.2f}%")
else:
    st.warning("No price data for selected date.")