# -*- coding: utf-8 -*-
#Import 
import pandas as pd
import re
###
#Initial Variables
x=0
Corresponding_Authors=[]
#Dataframe Manipuation
df= pd.read_excel('Dimensions.xlsx') #Problems with using csv use excel
df = df[df["Publication Type"].str.contains("Article")] #Filtering

df = df.reset_index(drop=True)
df2=df.iloc[0:20,:] #Creating test Dataframe

df2["Dataset"] ="Dim"


while x<len(df2): #Main Look

    #Regex To find entries with (Iowa State University) and grab name
    string=re.findall("[a-zA-Z].+?(?= \(Iowa State University)|(?<=;).+?(?=\(Iowa State University\))",str(df2["Corresponding Authors"][x]))
    
    #Sometimes regex will find 2 entries per string and list. For now only grabbing first entry
    
    if len(string) ==0: #If no entry found (Likely no Corresponding Author Listed)
        name="Unknown"
        Corresponding_Authors.append(name)
         #END IF
    
    else: #Else grab first entry 
        name=string[0]
        if name.find(";") != -1: #If entry has semicolon then split on the right
            name=name.split(";")[1]
            Corresponding_Authors.append(name)
        ## END IF
        else:
            Corresponding_Authors.append(name)
        ## END ELSE


    
    
    x=x+1
    ## END WHILE
print(Corresponding_Authors)
df2["DOI"].to_csv("DOIs/Dim_DOIs.csv")