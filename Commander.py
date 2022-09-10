import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image
data = pd.read_csv(r'Stock CSVs/SPY.csv')
df = pd.DataFrame(data)
st.title("Test Graphs using Plotly")

st.header("Using px.line and st.plotly_chart")
fig = px.line(df, x="Date", y="Close", title="SPY Weekly Close Price, Year-To-Date Graph")
st.plotly_chart(fig, use_container_width=True)

st.header("Using px.bar and st.plotly_chart")
fig = px.bar(df, x='Date', y='Volume',title="Spy Weekly Volume Shares, Year-To_Date-Graph")
st.plotly_chart(fig, use_container_width=True)

st.header("Using st.image (citation included)")
image = Image.open(r'Images/Open_Access_colours_Venn.png')

st.image(image, caption='Image taken from: Introducing Volcanica: The first diamond open-access journal for volcanology ')
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
