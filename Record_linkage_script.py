"""
Created on Apr 6, 2016
This script uses FSRIO data and USPTO data to match records in these two data sets
Matches are found by calculating the distance between strings using jellyfish.jaro_winkler 

@author: psirma
"""
#Necessary packages for running this code 
import pprint 
import pandas as pd
import os
import csv
import datetime
import re
import jellyfish
import math
import sys
from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


#Defining working directory
path = 'H:/CSSIP/Data/FSRIO_Patents'  

#1) 

#Opening the data 
fsrio_db = pd.read_csv(path+'/FSRIO Institutions.csv' )
# print fsrio_db['INSTITUTION_NAME'].isnull().values.any()
fsrio_db = fsrio_db[pd.notnull(fsrio_db['INSTITUTION_NAME'])]
print "***FSRIO Data *****"
print fsrio_db.head()
print len(fsrio_db['INSTITUTION_NAME'].unique())

#Declaring an empty list to append clean Insitution_name data
new_columm = []
for e in fsrio_db['INSTITUTION_NAME']: 

    #Cleaning Institution_Name string column before start finding matches 
    e = e.upper()  #change to capital letters
    
    #removing common words that might lead to irrelevant matches
    e = re.sub(r'\bUNIVERSITY OF\b', '',e )
    e = re.sub(r'\bUNIVERSITY\b', '',e )
    e = re.sub(r'\bEASTERN\b', '',e )
    e = re.sub(r'\bDEPARTMENT OF\b', '',e )
    e = re.sub(r'\bMEDICAL SCHOOL\b', '',e )
    e = re.sub(r'\bSCHOO\bL', '',e )
    e = re.sub(r'\bDEPARTMENT\b', '',e )
    e = re.sub(r'\bHEALTH\b', '',e )
    e = re.sub(r'\bFOR\b', '',e )
    e = re.sub(r'\bSTATE\b', '',e )
    e = re.sub(r'\bOF\b', '',e )
    e = re.sub(r'\bSERVICES\b', '',e )
    e = re.sub(r'\bSERVICE\b', '',e )
    e = re.sub(r'\bCOUNTY\b', '',e )
    e = re.sub(r'\bFOOD\b', '',e )
    e = re.sub(r'\bFOOD SAFETY\b', '',e )
    e = re.sub(r'\bPROGRAM\b', '',e )
    e = re.sub(r'\bAREA\b', '',e )
    e = re.sub(r'\bRESEARCH\b', '',e )
    e = re.sub(r'\bCENTER\b', '',e )
    e = re.sub(r'\bSOCIAL\b', '',e )
    e = re.sub(r'\bCOLLEGE\b', '',e )
    e = re.sub(r'\bHOSPITAL\b', '',e )
    e = re.sub(r'\bPLAIN EXPERIMENT STATION\b', '',e )
    e = re.sub(r'\bSCHOOL OF PUBLIC HEALTH\b', '',e )
    e = re.sub(r'\bFOUNDATION FOR THE ADVANCEMENT OF MILITARY MEDICINE\b', '',e )
    e = re.sub(r'\bINSTITUTE OF TECHNOLOGY\b', '',e )
    e = re.sub(r'\bCORPORATION\b', '',e )
    e = re.sub(r'\bMEDICAL CENTER\b', '',e )
    e = re.sub(r'\bTECH UNIVERSITY\b', '',e )
    e = re.sub(r'\bLABORATORY\b', '',e )
    e = re.sub(r'\bINC\b', '',e )
    e = re.sub(r'\bLLC\b', '',e )
    e = re.sub(r'\bLTD\b', '',e )
    e = re.sub(r'\bAGRICULTURE\b', '',e )
    e = re.sub(r'\bAND\b', '',e )
    e = re.sub(r'\bENVIRONMENTAL\b', '',e )
    e = re.sub(r'\bISLAND\b', '',e )
    e = re.sub(r'\bSAFETY\b', '',e )
    e = re.sub(r'\bPUBLIC\b', '',e )
    e = re.sub(r'\bENVIRONMENTAL\b', '',e )
    e = re.sub(r'\bTECHNOLOGY\b', '',e )
    e = re.sub(r'\bTECH\b', '',e )
    e = re.sub(r'\bIVY\b', '',e )
    e = re.sub(r'\bENVIRONMENTAL\b', '',e )
    e = re.sub(r'\bTECHNOLOGIES\b', '',e )
    e = re.sub(r'\bMEDICINE\b', '',e )
    e = re.sub(r'\bNATIONAL\b', '',e )
    e = re.sub(r'\bADVANCED\b', '',e )
    e = re.sub(r'\bINSTITUTE\b', '',e )
    e = re.sub(r'\bDEVELOPMENT\b', '',e )
    e = re.sub(r'\bMEDICAL\b', '',e )
    e = re.sub(r'\bGENERAL\b', '',e )
    e = re.sub(r'\bMEDICAL\b', '',e )
    e = re.sub(r'\bNATIONAL\b', '',e )
    e = re.sub(r'\bFOUNDATION\b', '',e )
    e = re.sub(r'\bSCHOOL\b', '',e )
    e = re.sub(r'\bENVIRONMENT\b', '',e )
    e = re.sub(r'\bEDUCATION\b', '',e )
    e = re.sub(r'\bNORTHERN\b', '',e )
    
    #Removing special characters and white spaces
    e = re.sub('-', '', e)
    e = re.sub('/', ' ', e)
    e = re.sub("'", '', e)
    e = re.sub(",", '', e)
    e = re.sub(":", ' ', e)
    e = re.sub("\.", ' ', e)
    e = re.sub('  +', ' ', e)
    e = e.strip().strip('"').strip("'")
    e = re.sub(r'\s+', ' ', e)
    
    #converting strings to unicode 
    e = unicode( e  , 'utf8' , 'replace')

    #Append clean data into new_column lis t
    new_columm.append(e) 


print new_columm
#Adding a new_column into fsrio_db 
fsrio_db['new_column'] = new_columm
print 
print fsrio_db['new_column'].head()

#2)

#Openning USPTO Data 
uspto_db = pd.read_csv(path+'/USPTO Instittuions2.csv')
print "*****USPTO Data ****"
print uspto_db.head()
print len(uspto_db['organization'].unique()) 
uspto_db = uspto_db[pd.notnull(uspto_db['organization'])]

#Declaring new_columns_2 list to append cleaned organization values 
new_column_2 = []

#Cleaning organization column before matching 
for e in uspto_db['organization']: 
    e = e.upper()

    
    #removing common words that might lead to irrelevant matches    
    e = re.sub(r'\bUNIVERSITY OF\b', '',e )
    e = re.sub(r'\bUNIVERSITY\b', '',e )
    e = re.sub(r'\bEASTERN\b', '',e )
    e = re.sub(r'\bDEPARTMENT OF\b', '',e )
    e = re.sub(r'\bMEDICAL SCHOOL\b', '',e )
    e = re.sub(r'\bSCHOO\bL', '',e )
    e = re.sub(r'\bDEPARTMENT\b', '',e )
    e = re.sub(r'\bHEALTH\b', '',e )
    e = re.sub(r'\bFOR\b', '',e )
    e = re.sub(r'\bSTATE\b', '',e )
    e = re.sub(r'\bOF\b', '',e )
    e = re.sub(r'\bSERVICES\b', '',e )
    e = re.sub(r'\bSERVICE\b', '',e )
    e = re.sub(r'\bCOUNTY\b', '',e )
    e = re.sub(r'\bFOOD\b', '',e )
    e = re.sub(r'\bFOOD SAFETY\b', '',e )
    e = re.sub(r'\bPROGRAM\b', '',e )
    e = re.sub(r'\bAREA\b', '',e )
    e = re.sub(r'\bRESEARCH\b', '',e )
    e = re.sub(r'\bCENTER\b', '',e )
    e = re.sub(r'\bSOCIAL\b', '',e )
    e = re.sub(r'\bCOLLEGE\b', '',e )
    e = re.sub(r'\bHOSPITAL\b', '',e )
    e = re.sub(r'\bPLAIN EXPERIMENT STATION\b', '',e )
    e = re.sub(r'\bSCHOOL OF PUBLIC HEALTH\b', '',e )
    e = re.sub(r'\bFOUNDATION FOR THE ADVANCEMENT OF MILITARY MEDICINE\b', '',e )
    e = re.sub(r'\bINSTITUTE OF TECHNOLOGY\b', '',e )
    e = re.sub(r'\bCORPORATION\b', '',e )
    e = re.sub(r'\bMEDICAL CENTER\b', '',e )
    e = re.sub(r'\bTECH UNIVERSITY\b', '',e )
    e = re.sub(r'\bLABORATORY\b', '',e )
    e = re.sub(r'\bINC\b', '',e )
    e = re.sub(r'\bLLC\b', '',e )
    e = re.sub(r'\bLTD\b', '',e )
    
    e = re.sub(r'\bAGRICULTURE\b', '',e )
    e = re.sub(r'\bAND\b', '',e )
    e = re.sub(r'\bENVIRONMENTAL\b', '',e )
    e = re.sub(r'\bISLAND\b', '',e )
    e = re.sub(r'\bSAFETY\b', '',e )
    e = re.sub(r'\bPUBLIC\b', '',e )
    e = re.sub(r'\bENVIRONMENTAL\b', '',e )
    e = re.sub(r'\bTECHNOLOGY\b', '',e )
    e = re.sub(r'\bTECH\b', '',e )
    e = re.sub(r'\bIVY\b', '',e )
    e = re.sub(r'\bENVIRONMENTAL\b', '',e )
    e = re.sub(r'\bTECHNOLOGIES\b', '',e )
    e = re.sub(r'\bMEDICINE\b', '',e )
    e = re.sub(r'\bNATIONAL\b', '',e )
    e = re.sub(r'\bADVANCED\b', '',e )
    e = re.sub(r'\bINSTITUTE\b', '',e )
    e = re.sub(r'\bDEVELOPMENT\b', '',e )
    e = re.sub(r'\bMEDICAL\b', '',e )
    e = re.sub(r'\bGENERAL\b', '',e )
    e = re.sub(r'\bMEDICAL\b', '',e )
    e = re.sub(r'\bNATIONAL\b', '',e )
    e = re.sub(r'\bFOUNDATION\b', '',e )
    e = re.sub(r'\bSCHOOL\b', '',e )
    e = re.sub(r'\bENVIRONMENT\b', '',e )
    e = re.sub(r'\bEDUCATION\b', '',e )
    e = re.sub(r'\bNORTHERN\b', '',e )

    #Removing special characters and white spaces
    e = re.sub('-', '', e)
    e = re.sub('/', ' ', e)
    e = re.sub("'", '', e)
    e = re.sub(",", '', e)
    e = re.sub(":", ' ', e)
    e = re.sub("\.", ' ', e)

    e = re.sub('  +', ' ', e)
    e = e.strip().strip('"').strip("'")
    e = re.sub(r'\s+', ' ', e)

    #converting strings to unicode 
    e = unicode( e  , 'utf8' , 'replace')
   
    #Append clean data into new_column_2 list
    new_column_2.append(e) 
    
uspto_db['new_column_2'] = new_column_2
print uspto_db['new_column_2'].head()


#3)
#Creating a fuzzy match function to link records in the 2 data sets 
def fuzzy_string_comparator( string_1_IN, string_2_IN ):
    '''
    string_1_IN : input string No.1
    string_2_IN : input string No.2
    ******
    match_level_OUT: output distance between string_1_IN and string_2_IN 
    '''
    
    # return reference
    match_level_OUT = -1

    # Check if they are all strings
    if ( ( type( string_1_IN ) != str ) or ( type( string_2_IN ) != str ) ):
        
        match_level_OUT = 0
    
    #-- END check to see if strings are actually strings. --#
    
    # declare variables
    cleaned_string_1 = ""
    cleaned_string_2 = ""
    distance = -1
    
    # string 1 
    cleaned_string_1 = string_1_IN.upper()
    # string 2
    cleaned_string_2 = string_2_IN.upper()

    # Calculate Jaro-Winkler distance after converting two strings into capital characters.
    distance = jellyfish.jaro_winkler( cleaned_string_1, cleaned_string_2 )
    

    # According to different thresholds, return the match level
    if distance >= 0.92:

        match_level_OUT = 2

    elif distance >= 0.85:
    
        match_level_OUT = 1

    else:
    
        match_level_OUT = 0
        
    ### END SOLUTION
    
    return match_level_OUT

print "==>Function fuzzy_string_comparator() is created at" ,  str(datetime.datetime.now()) + "."
print


#4)
#Parsing fuzzy_string_comparator() into the new_column and new_column_2

#declaring the output file 
df = []
#Staring Record Linkage 
#Using nested loop to go through every record in the two data files
for index, row in  fsrio_db.iterrows():   
    
    name =  row['new_column']  #name is the Institution_name in FSRIO data 
    fsrio_ID =  row['ID']    #Institution ID
    
    for i, dt in uspto_db.iterrows():
        org = dt['new_column_2']  #org is the organization name in USPTO data
        uspto_ID = dt['id']   #Organization ID
        score = fuzzy_string_comparator(name, org)
        
        #Writing the final data if the Jaro-Wrinkler distance is > 0.85
        if score != 0:
            print
            df.append([fsrio_ID , row['INSTITUTION_NAME'] , dt['organization'] ,uspto_ID , score ])
            data = pd.DataFrame(df)
            print data.tail() 
            data.to_csv(path+'/fuzzy_match_btn_fsrio_uspto.csv') #Exporting the csv the final data set 

     
print 
print "***********  The End    *************"




