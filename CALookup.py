#Main script file for looking up Corresponding Authors Using Web of Science Data
# Prints to count.csv and out.csv

import pandas as pd
import requests
import re
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

def ISU_Directory_lookupDIM(CorrespondingA):
    
    #API Grab
    ISU_api_key = "52c20b1f0eed1f636b39c682dd"
    OUR_API_URL = "https://apps.info.iastate.edu/api/v3.1/"+ISU_api_key+"/search/"+dimname
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
    DOI=[]

    
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

def CAParserWoS(CorrespondingA):
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

def CAParserDim(CorrespondingA):
    if  ISU_Directory_lookupDIM(dimname)[0] == "success": #if person found in directory
        
        if ISU_Directory_lookupDIM(dimname)[1] == True: #if student print and save student info
            classification=ISU_Directory_lookupDIM(dimname)[5]
            major=ISU_Directory_lookupDIM(dimname)[6]
            name=ISU_Directory_lookupDIM(dimname)[7]
            CorrespondingAuthor.append(name)
            majordepraw.append(major)
            titlestu.append(classification)
            typetitle.append(ISU_Directory_lookupDIM(dimname)[8])
            
        else: #else 2 then is Faculty and save faculty data
            dept = ISU_Directory_lookupDIM(dimname)[2]
            dept_char_code = ISU_Directory_lookupDIM(dimname)[3]
            title = ISU_Directory_lookupDIM(dimname)[4]
            name=ISU_Directory_lookupDIM(dimname)[7]
            CorrespondingAuthor.append(name)
            majordepraw.append(dept)
            titlestu.append(title)
            typetitle.append(ISU_Directory_lookupDIM(dimname)[8])
    else: #else 1 if cannot find person get WoS guess Data
        CorrespondingAuthor.append(dimname)
    #replace WoS department Data with augmented data from dictionary 
        majordepraw.append("No Data")
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
NAs=[]
dualfunded=[]
DOIRefine=[]
KnownDOIs=[]
dataset=[]
dfdim=pd.DataFrame()
df4=pd.DataFrame()
df5=pd.DataFrame()
dfmaster=pd.DataFrame(columns=['Dataset'])
Dim_CAs=[]
DOI=[]
 ## End List Pre-Allocation
#Read Data
############ DATA IMPORTATION #######################
dfraw= pd.read_excel('WoS_ISU_2021.xlsx') #Problems with using csv use excel

df=dfraw.iloc[0:20,:] #Creating test Dataframe
df = df[df["Document Type"].str.contains("Article")] #sort to only articles
df = df.reset_index(drop=True)

df["Dataset"] ="WoS"
df2=pd.read_csv('Dictionary/dictionary.csv')
df3=pd.read_csv('Dictionary/DictionaryCollege.csv')



dfdimraw= pd.read_excel('Dimensions.xlsx') #Problems with using csv use excel
dfdim=dfdimraw.iloc[0:20,:]
dfdim = dfdim[dfdim["Publication Type"].str.contains("Article")] #Filtering
dfdim = dfdim.reset_index(drop=True)


dfdim["Dataset"] ="Dim"

##########################


timer=(len(df)-x+len(dfdim))*2
print(len(df)+len(dfdim),"Accepted Entries Found")
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
## NAME EXPANDER ##
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
        CAParserWoS(lookup[x])
        dataset.append("WoS")
        KnownDOIs.append(df["DOI"][x])
        DOI.append(df["DOI"][x])
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
            dataset.append("WoS")
            titlestu.append("No Data")
            typetitle.append("No Data")
            KnownDOIs.append(df["DOI"][x])
            DOI.append(df["DOI"][x])
        else: #fallback if all else fails gmail accounts, yahoo acounts
            lookup.append(df["copy"][x])
            CAParserWoS(lookup[x])
            dataset.append("WoS")
            DOI.append(df["DOI"][x])
            KnownDOIs.append(df["DOI"][x])
    
   
        while y<len(df2):
            if df2["wosdept"][y] == majordepraw[x]:
                majordepraw[x] = df2["realdept"][y]
                break
            else:
                y=y+1
        y=0


        x=x+1
    if (printcounter == 5):
        timer=(len(df)-x+len(dfdim))*2
        print('Estimated time is:',timer,'seconds')
        printcounter = 0
    printcounter= 1+printcounter
    percentage=x/(len(df)+len(dfdim))*100
    print("Checking Author",x,"/",len(df)+len(dfdim),"    Program is",format(percentage,'>1.2f'),"% Complete!",)
##DOI Capture ##
df["DOI"].to_csv("DOIs/WoS_DOIs.csv")
y=0
## DOI Matching ##

while y<len(dfdim["DOI"]): # Try DataFrame.isin(values)

    if dfraw['DOI'].eq(dfdim["DOI"][y]).any()== False:
        DOIRefine.append(dfdim["DOI"][y])
        string=re.findall("[a-zA-Z].+?(?= \(Iowa State University)|(?<=;).+?(?=\(Iowa State University\))",str(dfdim["Corresponding Authors"][y]))
        if len(string) ==0: #If no entry found (Likely no Corresponding Author Listed)
            dimname="Unknown"
            Dim_CAs.append(dimname)
             #END IF
        
        else: #Else grab first entry 
            dimname=string[0]
            if dimname.find(";") != -1: #If entry has semicolon then split on the right
                dimname=dimname.split(";")[1]
                Dim_CAs.append(dimname)
                CAParserDim(dimname)
                dataset.append("Dim")
                DOI.append(dfdim["DOI"][y])
            ## END IF
            else:
                Dim_CAs.append(dimname)
                CAParserDim(dimname)
                dataset.append("Dim")
                DOI.append(dfdim["DOI"][y])
            ## END ELSE
        y=y+1
        
        #clear string variable
    else:
        y=y+1
        
        
    
    



##########################################################

#turn datasets into new columns
dfmaster=pd.DataFrame(columns=['Dataset',"Corresponding Author","Department/Major","Title/Classification","StudentOrFaculty","DOI"])
dfmaster["Corresponding Author"] = CorrespondingAuthor
dfmaster["Title/Classification"]=titlestu
dfmaster["StudentOrFaculty"]=typetitle
dfmaster["Dataset"]=dataset
dfmaster["DOI"]=DOI
dfmaster['Department/Major']=majordepraw
dfmaster.to_csv("Output/MasterList.csv")
######
# str method or replace (replace & with and before admitting to count)


###
#print to csv

## Cannot put in same dataframe index does not match
dfmaster['Department/Major'].value_counts().to_csv('Output/CountDept.csv') #count dept names
dfmaster["Title/Classification"].value_counts().to_csv('Output/CountTitle.csv') #count title names
dfmaster["StudentOrFaculty"].value_counts().to_csv('Output/CountClass.csv')
#####
y=0
x=0
while x<len(df):
    
    #deparment to college correction
    while y<len(df3):
        if df3['Department'][y] ==majordepraw[x]: #match dept
            collegeinfo.append(df3['College'][y]) #grab college info
            if  df3['College'][y]=="N.A.":
                NAs.append(majordepraw[x])
            if df3['College'].str.contains("/")[y]== True:
                dualfunded.append(df3['College'][y])
      
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
        print("....WoS Lookup Ended Sucessfully...")
    #print(department_char_code)
    
df.to_csv("Output/Corresponding Author Info.csv")
# Guard for no dualfunded/NAs
if len(NAs)>0: 
    df4["Non Applicable"]=pd.DataFrame(NAs)
    df4.value_counts().to_csv("Output/Non Applicables.csv")
if len(dualfunded)>0:
    df5["Dual Funded"]=pd.DataFrame(dualfunded)
    df5.value_counts().to_csv("Output/Dual Funded Departments.csv")



#00) investigate repeated Dim_CAs
#0) instead of shortned WOS DOI run all and compare to dimensions data
#2) Run dimensions name lookup on DOI Refine
#3) Create Custom Dataframe to prepare merge of Dimensions and WoS Data
#3) DOI, Journal Name, CA
######
# Trigger Author lookup 
    

