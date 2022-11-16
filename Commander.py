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

def barplotter(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["Unnamed: 0"], y=df["Department/Major"]))    
    fig.update_layout(
    title="Volume of Selected Stocks", xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(fig, use_container_width=True)
    
sys.path.append(r'C:\Users\Andres\Documents\GitHub\test\Functions')


### Acquire Data ###
st.title("Testing Platform for URA")
st.header("Corresponding Authors by Department")
files = st.file_uploader("Upload Department Info", type={"csv", "txt"}, key="2")
df= pd.read_csv(files)
st.write(files)


################################# END ACQUIRE DATA ###############################

######## PLOT ############

barplotter(df)

######### Department ###########3

#Try a dummy csv or an if statment before this

fig=px.pie(df,values="Department/Major", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)
################ End plot ############


df.loc[df['Department/Major'] < 3, 'Unnamed: 0'] = 'Outliers'
fig=px.pie(df,values="Department/Major", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)
######################################
##################### College #########
st.header("Corresponding Authors by College")
files3 = st.file_uploader("Upload College Info", type={"csv", "txt"}, key="1")
df3=pd.read_csv(files3)
st.write(df3)

fig=px.pie(df3,values="College", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)
##########################################
########## Student or Faculty ##########
st.header("Corresponding Authors by Classification")
files2 = st.file_uploader("Upload Student/Faculty Info", type={"csv", "txt"}, key="3")
df2= pd.read_csv(files2)
st.write(df2)
#Try a dummy csv or an if statment before this

fig=px.pie(df2,values="StudentOrFaculty", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)
########## Titles #######
st.header("Corresponding Authors by Title")
files4 = st.file_uploader("Upload Title Info", type={"csv", "txt"}, key="4")
df4= pd.read_csv(files4)
st.write(df4)
fig=px.pie(df4,values="Title/Classification", names="Unnamed: 0")
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, use_container_width=False)
################ End plot ############