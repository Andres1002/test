import streamlit as st


import pandas as pd
data = pd.read_csv (r'SPY.csv')
df = pd.DataFrame(data)
close = df["Close"]
st.title("SPY Weekly, Year-To-Date Graph")
chart = st.line_chart(close)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")