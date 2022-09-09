import streamlit as st
import pandas as pd
import plotly.express as px
data = pd.read_csv(r'C:\Users\Andres\Documents\GitHub\test\SPY.csv')
df = pd.DataFrame(data)
st.title("Test Graphs using Plotly")

fig = px.line(df, x="Date", y="Close", title="SPY Weekly Close Price, Year-To-Date Graph")
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(df, x='Date', y='Volume',title="Spy Weekly Volume Shares, Year-To_Date-Graph")
st.plotly_chart(fig, use_container_width=True)
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
