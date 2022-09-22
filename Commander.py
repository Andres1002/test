import streamlit as st
import pandas as pd
from io import StringIO 
import os
from Plotter import barplotter, lineplotter
# Initial Variables
x=0;
dfs = list()
### Acquire Data ###
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
lineplotter(cnt,dfs)   

barplotter(cnt,dfs)


################ End plot ############

