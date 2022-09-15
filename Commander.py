import streamlit as st
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from io import StringIO 
import os
# Initial Variables
x=0;
dfs = list()

st.title("Testing Platform for URA")
with st.sidebar:
    files = st.file_uploader("Please choose a CSV file", accept_multiple_files=True)
    for file in files:
        bytes_data =file.getvalue()
        st.write("filename:", file.name)
        
        stringio = StringIO(file.getvalue().decode("utf-8"))
        string_data = stringio.read()

        df= pd.read_csv(file)
        df['file'] = os.path.splitext(file.name)[0]
        dfs.append(df)

cnt=len(dfs)
################################# END ACQUIRE DATA ###############################

######## PLOT ############
fig = go.Figure()
while (x<cnt):
    
    fig.add_trace(go.Scatter(x=dfs[x]["Date"], y=dfs[x]["Close"],name=str(dfs[x].at[0,"file"])))       
    fig.update_layout(
    title="Stock Prices of Selected Stocks", xaxis_title="Date", yaxis_title="Close Price")
    x=x+1
    ## END while

st.plotly_chart(fig, use_container_width=True)    


x=0;
fig = go.Figure()
while (x<cnt):
    fig.add_trace(go.Bar(x=dfs[x]["Date"], y=dfs[x]["Volume"],name=str(dfs[x].at[0,"file"])))    
    fig.update_layout(
    title="Volume of Selected Stocks", xaxis_title="Date", yaxis_title="Volume")
    x=x+1
    ## END while
st.plotly_chart(fig, use_container_width=True)

################ End plot ############

st.header("Using st.image (citation included)")
image = Image.open(r'Images/Open_Access_colours_Venn.png')
st.image(image, caption='Image taken from: Introducing Volcanica: The first diamond open-access journal for volcanology ')
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
