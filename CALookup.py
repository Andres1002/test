# -*- coding: utf-8 -*-




import pandas as pd
import requests
from openpyxl import load_workbook
def ISU_Directory_lookup(CorrespondingA):

    ISU_api_key = "52c20b1f0eed1f636b39c682dd"
    OUR_API_URL = "https://apps.info.iastate.edu/api/v3.1/"+ISU_api_key+"/search/"+looku
    api_response = requests.get(OUR_API_URL)
    parsed_response = api_response.json()
    ### CHECK IF STUDENT
    classification=[]
    major=[]
    department=[]
    department_char_code=[]
    title=[]
    status=[]
    isstudent=[]
    name=[]
    
    if  parsed_response['status']== "success":
        status=parsed_response['status']
        name=parsed_response['data']['persons'][0]['name']
        if parsed_response['data']['persons'][0]['isStudent'] == True:
            isstudent=parsed_response['data']['persons'][0]['isStudent']
            status=parsed_response['status']
            classification=parsed_response['data']['persons'][0]['classification']
            major=parsed_response['data']['persons'][0]["major"]
        
        else:
            status=parsed_response['status']
            department = parsed_response['data']['persons'][0]['addresses'][0]['department']
            department_char_code = parsed_response['data']['persons'][0]['addresses'][0]['departmentCharCode']
            title = parsed_response['data']['persons'][0]['title']
    else:
        status="f"
        return status
    return status,isstudent, department, department_char_code, title, classification,major,name
x=0

CorrespondingAs=[]
netids=[]
lookup=[]
majordep=[]
titlestu=[]
CorrespondingAuthor=[]
df= pd.read_csv('savedrecs.csv')
df = df[df["Document Type"] == "Article"] 
df = df.reset_index(drop=True)
while x<len(df):
    #look for .edu first
    a=";" in df["Email Addresses"][x]
    b="@iastate.edu" in df["Email Addresses"][x]
    v=".edu" in df["Email Addresses"][x]
    if a == False and b== True:
        lookup.append(df["Email Addresses"][x])
        x=x+1
    #elseif false and false
        #api likely to turn false info
        #use WoS data
        
    else:
        # if one email split and search net ID
        df["CA Last Name"] = df["Reprint Addresses"].str.split('(').str[0]
        df["CA Last Name"] = df["CA Last Name"].str.split(';').str.get(-1)
        df["CA Last Name"]= df["CA Last Name"].str.split(',').str[0]
        df["CA Last Name"]= df["CA Last Name"].str.lower()
        # add new column

        df["Author Full Names"] = df["Author Full Names"].str.lower()
        string=df["CA Last Name"][x]
        string_in_string = r"({}, [a-zA-Z- ]+;|{}, [a-zA-Z- ]+|{} [a-zA-Z- ])".format(string,string,string)
        df["copy"]= df["Author Full Names"].str.extract(string_in_string)
        # Guard for non iastate.edu emails
        if v==True and b==False:
            print(f'Cannot Find {df["copy"][x]} in Directory\n ')
            df["WoS Department"]= df["Addresses"].str.split('Iowa State Univ,').str[-1]
            df["WoS Department"]= df["WoS Department"].str.split(', Ames').str[0]
            CorrespondingAuthor.append(df["copy"][x])
            majordep.append(df["WoS Department"][x])
            titlestu.append("")
        else:
            lookup.append(df["copy"][x])
    
        #CorrespondingAs = [item.replace(";", "") for item in CorrespondingAs]
        #CorrespondingAs = [item.replace(",", "") for item in CorrespondingAs]
        x=x+1

## API GRAB
count=0;
for looku in lookup:
    status =ISU_Directory_lookup(lookup)[0]
    if  ISU_Directory_lookup(lookup)[0] == "success":
            
        if ISU_Directory_lookup(lookup)[1] == True:
            classification=ISU_Directory_lookup(lookup)[5]
            major=ISU_Directory_lookup(lookup)[6]
            name=ISU_Directory_lookup(lookup)[7]
            print(f'{name} in {major}, is a { classification} student\n')
            CorrespondingAuthor.append(name)
            majordep.append(major)
            titlestu.append(classification)
            
            
        else:
            dept = ISU_Directory_lookup(lookup)[2]
            dept_char_code = ISU_Directory_lookup(lookup)[3]
            title = ISU_Directory_lookup(lookup)[4]
            name=ISU_Directory_lookup(lookup)[7]
            print(f'{name} in {dept} aka {dept_char_code}, is {title}\n ')
            CorrespondingAuthor.append(name)
            majordep.append(dept)
            titlestu.append(title)
    else:
        print(f'Cannot Find {looku} in Directory\n ')
        CorrespondingAuthor.append(looku)
        majordep.append(df["WoS Department"][count])
        titlestu.append("")
    count=count+1;

df["Corresponding Author"] = CorrespondingAuthor
df["Department/Major"]=majordep
df["Title/Classification"]=titlestu
## Cannot put in same dataframe index does not match


df.to_csv("out.csv")
df['Department/Major'].value_counts().to_csv('Count.csv')
    #print(department_char_code)

    #print ("In ISU Directory")
    #df value_counts look up
    
