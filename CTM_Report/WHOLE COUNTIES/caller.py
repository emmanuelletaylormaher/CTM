# -*- coding: utf-8 -*-
"""
Name: classTester.py

PURPOSE OF PROGRAM: 
    Create graphical output using Census data from the
    API.

Created on Fri Sep 20 10:41:18 2019

@author: slq584
"""

import os
import shutil
import xlsxwriter


#importing pandas to create dataframes
import pandas as pd

#import paths to API calls and other files
import paths as p

#import other modules
import population_growth as p_g                 #Figure 1, Table 1, Figure 2, Table 2
import population_trends as p_t                 #Table 3, Table 4, Figure 3
import group_quarters as g_q                    #Table 5
import historic_average_houseshold as h_a_h     #Table 7, Figure 4
import household_estimates as h_e               #Table 8, Table 9 
import median_household_income as m_h_i         #Table 10, Table 11
import employment_trends as e_t                 #Table 14, Figure 7, Table 15, Table 18

"""
main() PURPOSE:     
    Read imported Excel file, and convet into a DataFrame. 
    ask user for the name of county they would like to look up.            
"""
def main():
    #path variable that can easily be changed out
    #MUST be .xls or xlsx file
    path = p.mpo
    #Declaration of Counties Dataframe
    counties = pd.DataFrame()
    
    #read excel file specified in path and assign to
    #dataframe (only reading columns with information pertinent to counties DF)
    counties = pd.read_excel(path)
    
    #Get names of indexes for which the counties ARE NOT WHOLE
    #whole_counties = counties[counties['WHOLE/PARTIAL'] != 'WHOLE'].index
    #Drop Counties that meet this criteria
    #counties.drop(whole_counties, inplace=True)
    #reset index numbers
    #counties = counties.reset_index(drop=True)
   
    
    #declare county variable that will be assigned
    #a string value in the following while loop
    county = None   
    #loop will continue until county is assigned a value
    #or if user manually exits when prompted
    while(county == None):
        lookup = input("Please enter the name of the county:  ")
        county = county_finder(lookup, counties)
        if(county == None):
           try_again = input("Try again (Y/N)?  ")
           #exit while loop if user enters 'N'
           if try_again.upper() == 'N':
               break;
        else:
            fips = get_fips(counties, county)
            print("FIPS code is: ", fips)
            
            break;
            
    if(float(fips) < 100):
        fips = "0" + fips
    
    dirName = "output/" + county
    dirmaker(dirName)
    
   # Create a workbook and add a worksheet.
    workbook = pd.ExcelWriter(dirName + '/output.xlsx', engine='xlsxwriter')

    fips = str(fips)
    county = str(county)

    
    #Use fips to make call to main() functions of other modules
    
    #population_growth.py (Figure 1, Table 1, Figure 2, Table 2)
    part1 = p_g.main(fips)
    part1[1].to_excel(workbook, sheet_name = "Table1")
    part1[3].to_excel(workbook, sheet_name = "Table 2")
    
    #workbook.save()
    
    
    #population_trends.py (Table 3, Table  4, Figure 3)
    part2 = p_t.main(fips, county)
    part2[0].to_excel(workbook, sheet_name = "Table 3")
    part2[1].to_excel(workbook, sheet_name = "Table 4")
    
    #workbook.save()
    
    
    #group_quarters.py (Table 5)
    part3 = g_q.main(fips, county)
    part3[0].to_excel(workbook, sheet_name = "Table 5")
    
    #workbook.save()
        
    #historic_average_household.py (Table 7, Figure 4)
    part4 = h_a_h.main(fips, county)
    part4[0].to_excel(workbook, sheet_name = "Table 7")
    
    #workbook.save()
    
    #household_estimates.py (Table 8, Table 9)
    part5 = h_e.main(fips, county)
    part5[0].to_excel(workbook, sheet_name = "Table 8")
    #Table 9 is TBD
    
    #median_household_income.py (Table 10, Table 11)
    part6 = m_h_i.main(fips, county)
    part6[0].to_excel(workbook, sheet_name = "Table 10")
    part6[1].to_excel(workbook, sheet_name = "Table 11")
    
    #workbook.save()
    
    fips = str(fips)
    county = str(county)
    
    #employment_trends.py (Table 14, Figure 7, Table 15, Table16, Table17, Table 18)
    part7 = e_t.main(county)
    part7[0].to_excel(workbook, sheet_name = "Table 14")
    part7[2].to_excel(workbook, sheet_name = "Table 15")
    part7[3].to_excel(workbook, sheet_name = "Table 16")
    part7[4].to_excel(workbook, sheet_name = "Table 17")
    part7[5].to_excel(workbook, sheet_name = "Table 18")
   
   
    workbook.save()    
    print("Done")
  
    
"""
county_finder() PURPOSE:
    Search through Dataframe (var counties) to see if specified
    county (lookup) exists. If so, return a string from DataFrame (comparator).
    If not, return None.     
"""   
def county_finder(lookup, counties):
    #for loop to iterate through all rows of the DataFrame
    for index, row in counties.iterrows():
        county_name = row['NAME']    
        #comparator = county_name[:-7]
        #compare strings to see if lookup has a match
        if county_name.lower() == lookup.lower():
            print("Match Found!")
            return county_name
    #this code executes if no match was found whatsoever
    print("County Specified Not Found")
    return None

"""
get_fips() PURPOSE:
    Returns FIPS code that will be used to look up data in the API
    and other files.
"""
def get_fips(counties, county):
    #Add "County" to string for comparison
    concat = county
    #Subset rows based on concat match
    subset_row = counties[counties['NAME']==concat]
    #Get FIPS code
    fips = subset_row['FIPS_TEXT'].values[0]
    fips = str(int(fips))
    return fips

"""
consolidator() PURPOSE: 
    Takes all lists passed and creates One Large List
"""
def consolidator(master, dataset):
    
    for data in dataset:
        master.append(data)
        
    return master
            
            
"""
dirmaker() PURPOSE:
    Checks to see if directory exists. If so, directory gets deleted and remade.
"""
def dirmaker(path):
    if os.path.exists(path) == True:
        shutil.rmtree(path)
        
    os.mkdir(path)
    os.mkdir(path + "/img")
    
    
"""
table_writer() PURPOSE:
    Writes the Dataframe passed into an Excel sheet
"""
def table_writer(data, workbook, worksheet_name):
    
    data.to_excel(workbook, sheet_name = worksheet_name)
    workbook.save()
    print("done")


if __name__ == "__main__":
    #execute only if run as a script
    main()