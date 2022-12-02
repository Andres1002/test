#Main script file for looking up Corresponding Authors Using Web of Science Data
# Prints to count.csv and out.csv

import pandas as pd
import requests

def ISU_Directory_lookup(CorrespondingA):
    
    #API Grab
    ISU_api_key = "52c20b1f0eed1f636b39c682dd"
    OUR_API_URL = "https://apps.info.iastate.edu/api/v3.1/"+ISU_api_key+"/search/"+lookup[x]
    api_response = requests.get(OUR_API_URL)
    parsed_response = api_response.json()
    
    ##List Pre-allocation
    classification=[]
    major=[]
    department=[]
    department_char_code=[]
    title=[]
    status=[]
    isstudent=[]
    name=[]
    types=[]
    
    if  parsed_response['status']== "success": #If Person is on directory grab info
        status=parsed_response['status']
        name=parsed_response['data']['persons'][0]['name']
        if parsed_response['data']['persons'][0]['isStudent'] == True: #if person is student grab student info
            isstudent=parsed_response['data']['persons'][0]['isStudent']
            status=parsed_response['status']
            classification=parsed_response['data']['persons'][0]['classification']
            major=parsed_response['data']['persons'][0]["major"]
            types="Student"
        
        else:  #if person is faculty grab certain info
            status=parsed_response['status']
            department = parsed_response['data']['persons'][0]['addresses'][0]['department']
            department_char_code = parsed_response['data']['persons'][0]['addresses'][0]['departmentCharCode']
            title = parsed_response['data']['persons'][0]['title']
            types="Faculty"
    else: # could not find person in directory
        status="f"
        return status # return fail
    return status,isstudent, department, department_char_code, title, classification,major,name,types #return info

def CAParser(CorrespondingA):
    if  ISU_Directory_lookup(lookup[x])[0] == "success": #if person found in directory
        
        if ISU_Directory_lookup(lookup[x])[1] == True: #if student print and save student info
            classification=ISU_Directory_lookup(lookup[x])[5]
            major=ISU_Directory_lookup(lookup[x])[6]
            name=ISU_Directory_lookup(lookup[x])[7]
            CorrespondingAuthor.append(name)
            majordepraw.append(major)
            titlestu.append(classification)
            typetitle.append(ISU_Directory_lookup(lookup[x])[8])
            
        else: #else 2 then is Faculty and save faculty data
            dept = ISU_Directory_lookup(lookup[x])[2]
            dept_char_code = ISU_Directory_lookup(lookup[x])[3]
            title = ISU_Directory_lookup(lookup[x])[4]
            name=ISU_Directory_lookup(lookup[x])[7]
            CorrespondingAuthor.append(name)
            majordepraw.append(dept)
            titlestu.append(title)
            typetitle.append(ISU_Directory_lookup(lookup[x])[8])
    else: #else 1 if cannot find person get WoS guess Data
        CorrespondingAuthor.append(df["copy"][x])
    #replace WoS department Data with augmented data from dictionary 
        majordepraw.append(df["WoS Department"][x])
        typetitle.append("No Data")
        titlestu.append("No Data")
    return CorrespondingAuthor,majordepraw,titlestu

##List Pre-allocation
x=0
printcounter=0
y=0
lookup=[]
majordepraw=[]
titlestu=[]
CorrespondingAuthor=[]
typetitle=[]
collegeinfo=[]
 ## End List Pre-Allocation
#Read Data
df= pd.read_csv('savedrecs3.csv')
df = df[df["Document Type"].str.contains("Article")] #sort to only articles
df = df.reset_index(drop=True)
df2=pd.read_csv('Dictionary/dictionary.csv')
df3=pd.read_csv('Dictionary/DictionaryCollege.csv')

timer=(len(df)-x)*2
print(len(df),"Accepted Entries Found")
print('Estimated time is:',timer,'seconds')

######## String Manipulation #########
#split and search net ID and add new column
df["CA Last Name"] = df["Reprint Addresses"].str.split('(').str[0]
df["CA Last Name"] = df["CA Last Name"].str.split(';').str.get(-1)
df["CA Last Name"]= df["CA Last Name"].str.split(',').str[0]
df["CA Last Name"]= df["CA Last Name"].str.lower()
df["Author Full Names"] = df["Author Full Names"].str.lower()

# fill in empty emails if any
df['Email Addresses'] = df['Email Addresses'].fillna("")

#Guess Department with web of science Data
df["WoS Department"]= df["Addresses"].str.split('Iowa State Univ,').str[-1]
df["WoS Department"]= df["WoS Department"].str.split(', Ames').str[0]

######## END String Manipulation #########

while x<len(df):
    #name expander
    string=df["CA Last Name"][x]
    string_in_string = r"({}, [a-zA-Z- ]+;|{}, [a-zA-Z- ]+|{} [a-zA-Z- ])".format(string,string,string)
    df["copy"]= df["Author Full Names"].str.extract(string_in_string) #save into temp df
    
    if df["Email Addresses"][x] == "": #guard for no email entries
        a=False
        b=False
        v=False
    else:
        a=";" in df["Email Addresses"][x]
        b="@iastate.edu" in df["Email Addresses"][x]
        v=".edu" in df["Email Addresses"][x]
        #end else
        
    if a == False and b== True: #if one iastate email then look at isu directory
        lookup.append(df["Email Addresses"][x])
        CAParser(lookup[x])
        while y<len(df2):
            if df2["wosdept"][y] == majordepraw[x]:
                majordepraw[x] = df2["realdept"][y]
                break
            else:
                y=y+1
        y=0

        x=x+1
    #elseif false and false
        #api likely to turn false info
        #use WoS data
        
    else:
        # if one email split and search net ID
        # Guard for non iastate.edu emails
        
        if v==True and b==False: #if .edu but non isu email then use name expander
            lookup.append(df["copy"][x])

            #replace WoS department Data with augmented data from dictionary 
            majordepraw.append(df["WoS Department"][x])


            CorrespondingAuthor.append(df["copy"][x])
            titlestu.append("No Data")
            typetitle.append("No Data")
        else: #fallback if all else fails gmail accounts, yahoo acounts
            lookup.append(df["copy"][x])
            CAParser(lookup[x])
    
   
        while y<len(df2):
            if df2["wosdept"][y] == majordepraw[x]:
                majordepraw[x] = df2["realdept"][y]
                break
            else:
                y=y+1
        y=0


        x=x+1
    if (printcounter == 5):
        timer=(len(df)-x)*2
        print('Estimated time is:',timer,'seconds')
        printcounter = 0
    printcounter= 1+printcounter
    percentage=x/len(df)*100
    print("Checking Author",x,"/",len(df),"    Program is",format(percentage,'>1.2f'),"% Complete!",)
    
x=0

### Make new script for this ###

##########################################################

#turn datasets into new columns
df["Corresponding Author"] = CorrespondingAuthor
df["Department/Major"]=majordepraw
df["Title/Classification"]=titlestu
df["StudentOrFaculty"]=typetitle
######
# str method or replace (replace & with and before admitting to count)


###
#print to csv

## Cannot put in same dataframe index does not match
df['Department/Major'].value_counts().to_csv('Output/CountDept.csv') #count dept names
df["Title/Classification"].value_counts().to_csv('Output/CountTitle.csv') #count title names
df["StudentOrFaculty"].value_counts().to_csv('Output/CountClass.csv')
### Make new script for this ###
NAs=[]
while x<len(df):
    while y<len(df3):
        if df3['Department'][y] ==majordepraw[x]: #match dept
            collegeinfo.append(df3['College'][y]) #grab college info
            if  df3['College'][y]=="N.A.":
                NAs.append(majordepraw[x])
            
      
            x=x+1
            break #restart loop
        else:
            y=y+1 #else keep looking
    if y==len(df3): # if cant find notify user
        majordepraw.append(collegeinfo)
        ##replace with blank
        print("Error: Input College Data for:",majordepraw[x])
        majordepraw[x] = "Input Data"
        x=x+1
    y=0
    if len(majordepraw)== len(collegeinfo): #If all are accounted for print
        df["College"]=collegeinfo
        df["College"].value_counts().to_csv('Output/CountColl.csv')
        print("....Program Ended Sucessfully...")
    #print(department_char_code)
    
df.to_csv("Output/Corresponding Author Info.csv")
df4=pd.DataFrame()
df4["Non Applicable"]=pd.DataFrame(NAs)
df4.value_counts().to_csv("Output/Non Applicables.csv")

