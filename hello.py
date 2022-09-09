import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

data = pd.read_csv(r'SPY.csv')
df = pd.DataFrame(data)
st.title("Test Graphs using Plotly")

fig = px.line(df, x="Date", y="Close", title="SPY Weekly Close Price, Year-To-Date Graph")
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(df, x='Date', y='Volume',title="Spy Weekly Volume Shares, Year-To_Date-Graph")
st.plotly_chart(fig, use_container_width=True)

image = Image.open(r'Open_Access_colours_Venn.PNG')

st.image(image, caption='Image taken from Introducing Volcanica: The first diamond open-access journal for volcanology ')
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
