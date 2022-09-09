import streamlit as st
import pandas as pd
import plotly.express as px
data = pd.read_csv ('SPY.csv')
df = pd.DataFrame(data)
close = df["Close"]
st.title("SPY Weekly, Year-To-Date Graph")
chart = st.line_chart(close)

fig = px.line(df, x="Date", y="Close", title='Life expectancy in Canada')
st.plotly_chart(fig, use_container_width=True)
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")