# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 18:34:07 2022

@author: Andres
"""
import pandas as pd
import requests
## API GRAB

def ISU_Directory_lookup(CorrespondingA):

    ISU_api_key = "52c20b1f0eed1f636b39c682dd"
    OUR_API_URL = "https://apps.info.iastate.edu/api/v3.1/"+ISU_api_key+"/search/"+CorrespondingA
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
    
    if  parsed_response['status']== "success":
        status=parsed_response['status']
        
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
    return status,isstudent, department, department_char_code, title, classification,major


x=0
CorrespondingAs=[]
df= pd.read_csv('savedrecs.csv')
df = df[df["Document Type"] == "Article"] 
df = df.reset_index(drop=True)


# if one email split and search net ID
df["CA Last Name"] = df["Reprint Addresses"].str.split('(').str[0]
df["CA Last Name"] = df["CA Last Name"].str.split(';').str.get(-1)
df["CA Last Name"] = df["CA Last Name"].str.split(',').str[0]
df["CA Last Name"] = df["CA Last Name"].str.lower()
# add new column

df["Author Full Names"] = df["Author Full Names"].str.lower()
while x<len(df):
    string=df["CA Last Name"][x]
    string_in_string = r"({}, [a-zA-Z]+;|{}, [a-zA-Z]+|{} [a-zA-Z])".format(string,string,string)
    df["copy"]= df["Author Full Names"].str.extract(string_in_string)
    CorrespondingAs.append(df["copy"][x])
    x=x+1
    
CorrespondingAs = [item.replace(";", "") for item in CorrespondingAs]
CorrespondingAs = [item.replace(",", "") for item in CorrespondingAs]

## API GRAB

for CorrespondingA in CorrespondingAs:
#####Check if student
    status =ISU_Directory_lookup(CorrespondingA)[0]
    if  ISU_Directory_lookup(CorrespondingA)[0] == "success":
        
        if ISU_Directory_lookup(CorrespondingA)[1] == True:
           classification=ISU_Directory_lookup(CorrespondingA)[5]
           major=ISU_Directory_lookup(CorrespondingA)[6]
           print(f'{CorrespondingA} in {major}, is a { classification} student\n')
        else:
            dept = ISU_Directory_lookup(CorrespondingA)[2]
            dept_char_code = ISU_Directory_lookup(CorrespondingA)[3]
            title = ISU_Directory_lookup(CorrespondingA)[4]
            print(f'{CorrespondingA} in {dept} aka {dept_char_code}, is {title}\n ')
    else:
        print(f'Cannot Find {CorrespondingA} in Directory\n ')
    

    #print(department_char_code)

    #print ("In ISU Directory")

