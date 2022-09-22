import streamlit as st
import sys
from plots import barplotter, lineplotter
from csvparser import csvparser
# Initial Variables
sys.path.append(r'C:\Users\Andres\Documents\GitHub\test\Functions')


### Acquire Data ###
st.title("Testing Platform for URA")
with st.sidebar:
    files = st.file_uploader("Please choose a CSV file", accept_multiple_files=True)
    dfs,df = csvparser(files)


cnt=len(dfs)
################################# END ACQUIRE DATA ###############################

######## PLOT ############
lineplotter(cnt,dfs)   

barplotter(cnt,dfs)


################ End plot ############

