import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
import plotly.graph_objects as go
# Initial Variables
x=0;

st.title("Testing Platform for URA")
with st.sidebar:
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)


############ ACQUIRE DATA ###################
path = r'C:\Users\Andres\Documents\GitHub\test\Stock CSVs'
files = Path(path).glob('*.csv')  # note .rglob to get subdirectories
dfs = list()
for f in files:
    data = pd.read_csv(f)
    data['file'] = f.stem
    dfs.append(data)
## end for
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
