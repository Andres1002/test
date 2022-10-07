# -*- coding: utf-8 -*-




import pandas as pd
import requests
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
netids=[]
lookup=[]
df= pd.read_csv('savedrecs.csv')
df = df[df["Document Type"] == "Article"] 
df = df.reset_index(drop=True)
while x<len(df):
    a=";" in df["Email Addresses"][x]
    b="@iastate.edu" in df["Email Addresses"][x]
    if a == False and b== True:
        lookup.append(df["Email Addresses"][x])
        x=x+1
        
    else:
        # if one email split and search net ID
        df["CA Last Name"] = df["Reprint Addresses"].str.split('(').str[0]
        df["CA Last Name"] = df["CA Last Name"].str.split(';').str.get(-1)
        df["CA Last Name"]= df["CA Last Name"].str.split(',').str[0]
        df["CA Last Name"]= df["CA Last Name"].str.lower()
        # add new column

        df["Author Full Names"] = df["Author Full Names"].str.lower()
        string=df["CA Last Name"][x]
        string_in_string = r"({}, [a-zA-Z]+;|{}, [a-zA-Z]+|{} [a-zA-Z])".format(string,string,string)
        df["copy"]= df["Author Full Names"].str.extract(string_in_string)
        lookup.append(df["copy"][x])
    
        #CorrespondingAs = [item.replace(";", "") for item in CorrespondingAs]
        #CorrespondingAs = [item.replace(",", "") for item in CorrespondingAs]
        x=x+1

## API GRAB

for looku in lookup:
    status =ISU_Directory_lookup(lookup)[0]
    if  ISU_Directory_lookup(lookup)[0] == "success":
            
        if ISU_Directory_lookup(lookup)[1] == True:
            classification=ISU_Directory_lookup(lookup)[5]
            major=ISU_Directory_lookup(lookup)[6]
            print(f'{looku} in {major}, is a { classification} student\n')
        else:
            dept = ISU_Directory_lookup(lookup)[2]
            dept_char_code = ISU_Directory_lookup(lookup)[3]
            title = ISU_Directory_lookup(lookup)[4]
            print(f'{looku} in {dept} aka {dept_char_code}, is {title}\n ')
    else:
        print(f'Cannot Find {looku} in Directory\n ')
    

    #print(department_char_code)

    #print ("In ISU Directory")