import streamlit as st
import sys
from csvparser import csvparser
import plotly.graph_objects as go
# Initial Variables
def barplotter(cnt,dfs):
    x=0;
    fig = go.Figure()
    while (x<cnt):
        fig.add_trace(go.Bar(x=dfs[x]["Date"], y=dfs[x]["Volume"],name=str(dfs[x].at[0,"file"])))    
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


################ End plot ############

