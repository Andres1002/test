import streamlit as st
import sys
import plotly.graph_objects as go
import pandas as pd
import os
import plotly.express as px
# Initial Variables
def csvparser(files):
    dfs = list()
    df=pd.DataFrame()
    for file in files:
        st.write("filename:", file.name)
        df= pd.read_csv(file)
        df['file'] = os.path.splitext(file.name)[0]
        dfs.append(df)
    return dfs,df

def barplotter(cnt,dfs):
    x=0;
    fig = go.Figure()
    while (x<cnt):
        fig.add_trace(go.Bar(x=df["Unnamed: 0"], y=df["Department/Major"]))    
        fig.update_layout(
            title="Volume of Selected Stocks", xaxis_title="Date", yaxis_title="Volume")
        x=x+1
    ## END while
    st.plotly_chart(fig, use_container_width=True)
    
sys.path.append(r'C:\Users\Andres\Documents\GitHub\test\Functions')


### Acquire Data ###
st.title("Testing Platform for URA")
with st.sidebar:
    files = st.file_uploader("Please choose a CSV file", accept_multiple_files=True)
    dfs,df = csvparser(files)


cnt=len(dfs)
################################# END ACQUIRE DATA ###############################

######## PLOT ############

barplotter(cnt,dfs)
fig=px.pie(df,values="Department/Major", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)
################ End plot ############

df.loc[df['Department/Major'] < 3, 'Unnamed: 0'] = 'Outliers'
fig=px.pie(df,values="Department/Major", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)

