# -*- coding: utf-8 -*-
"""
Name: paths.py

PURPOSE OF PROGRAM: 
    Contains URLS for calls made to the US Census API.

Created on Wed Sep 25 09:04:10 2019

@author: slq584
"""

import pandas as pd


"""
frankenstein() PURPOSE:
    Concatenate a url to be used for an API call. Used to look up multiple
    counties.
    
    NOTE:   named "frankenstein" because frankly, a ridiculous name makes
            it easier to remember what it does.
"""
def frankenstein(first_half, county):
    concat = first_half + county + '&in=state:48&key='+census_api_key
    return concat

"""
acs_frankenstein() PURPOSE:
    Concatenate API call urls specifically for data in ACS.
"""
def acs_frankenstein(year, variable, county, acs):
    concat = "https://api.census.gov/data/" + year + "/acs/acs" + acs + "?get=NAME," + variable + "&for=county:" + county + "&in=state:48&key="+census_api_key
    return concat


"""
savepng() PURPOSE:
    Save the figure as a .png image for CTM usage.
"""
def savepng(figure, county, filename):
    figure.savefig("output/" + county + "/img/" +  filename + ".png", dpi=300, bbox_inches="tight")

"""

                            API KEY
"""
#this key belongs to emmanuelle (work-study fall 2019)
census_api_key = 'cdcdaf4093ecc26df8394fbc23ffdd540d7be796'

##############################################################################
"""
                        MPO.xlsx
"""
#this is the excel that countains the list of whole and partial counties
mpo = 'mpo.xlsx'


##############################################################################
"""
                            PATHS TO EXCEL FILES
"""
#Table 1. Population Percent Change for XXXX County and Texas, 1970-2010
table1_excel = 'TX_County_Population_1900_1990.xlsx'

#Table 3. Comparison of Recent Population Estimates and Growth Rates for
#XXXX County
table3_excel = '2018allcntytot.csv'

#Table 7. Historical Households and Average Household Sizes for XXXX County,
#1980-2010
table7_excel_1980 = 'nhgis0001_ds104_1980_TXcounty.xlsx'
table7_excel_1990 = 'nhgis0001_ds120_1990_TXcounty.xlsx'


##############################################################################

"""
                            API CALLS
"""
#Table 1. Population Percent Change for XXXX County and Texas, 1970-2010
#state
table1_call_state_2010 = 'https://api.census.gov/data/2010/dec/sf1?get=H001001,P001001&for=state:48&key='+census_api_key
table1_call_state_2000 = 'https://api.census.gov/data/2000/sf1?get=H001001,P001001&for=state:48&key='+census_api_key

#counties
table1_call_2010 = 'https://api.census.gov/data/2010/dec/sf1?get=P001001,NAME&for=county:'
table1_call_2000 = "https://api.census.gov/data/2000/sf1?get=P001001,NAME&for=county:"

######

#Table 3. Comparison of Recent Population Estimates and Growth Rates for
#xxxx County 2010-2014

table_3_call = 'https://api.census.gov/data/2012/acs/acs5?get=NAME,B01003_001E&for=county:'

######

#Table 5. Recent Trends in Group Quarters population for xxxx County

#2010
table_5_call_2010_total = 'https://api.census.gov/data/2010/dec/sf1?get=P029026,NAME&for=county:'
table_5_call_2010_correctional = 'https://api.census.gov/data/2010/dec/sf1?get=PCT020003,NAME&for=county:'
table_5_call_2010_juvenile = 'https://api.census.gov/data/2010/dec/sf1?get=PCT020010,NAME&for=county:'
table_5_call_2010_nursing = 'https://api.census.gov/data/2010/dec/sf1?get=P042005,NAME&for=county:'
table_5_call_2010_otherinstitutional = 'https://api.census.gov/data/2010/dec/sf1?get=PCT020015,NAME&for=county:'
table_5_call_2010_totalinstitutional = 'https://api.census.gov/data/2010/dec/sf1?get=P042002,NAME&for=county:'
table_5_call_2010_dorms = 'https://api.census.gov/data/2010/dec/sf1?get=P042008,NAME&for=county:'
table_5_call_2010_military = 'https://api.census.gov/data/2010/dec/sf1?get=P042009,NAME&for=county:'
table_5_call_2010_othernoninstitutional = 'https://api.census.gov/data/2010/dec/sf1?get=PCT020026,NAME&for=county:'
table_5_call_2010_totalnoninstitutional = 'https://api.census.gov/data/2010/dec/sf1?get=P029028,NAME&for=county:'


#####

#Table 7. Historical Households and Average Household Sizes for xxxx,
#1980-2010
table_7_call_2010_number = 'https://api.census.gov/data/2010/dec/sf1?get=P020001,NAME&for=county:'
table_7_call_2000_number = 'https://api.census.gov/data/2000/sf1?get=P020001,NAME&for=county:'

table_7_call_2010 = 'https://api.census.gov/data/2010/dec/sf1?get=H012001,NAME&for=county:'
table_7_call_2000 = 'https://api.census.gov/data/2000/sf1?get=H012001,NAME&for=county:'

#####

#Table 8. Recent Estimates of Number of Households for XXXX County
group_quarters_population_2012 = 'https://api.census.gov/data/2012/acs/acs5?get=B26001_001E,NAME&for=county:'

#####

#Table 10. Median Household Income for XXXX County and Texas 1970-2010
cpi = "CPI.xlsx"
nominal2000 = "https://api.census.gov/data/2000/sf3?get=HCT012001,NAME&for=county:"

#####
#Table 14. Historic Employment by Type for XXXX County, 1990-2010
basic_14 = 'employment_spreadsheets/Ellis basic.xls'
education_14 = 'employment_spreadsheets/Ellis Education.xls'
retail_14 = 'employment_spreadsheets/Ellis Retail Revised.xls'
service_14 = 'employment_spreadsheets/Ellis Service.xls'

#####

#Table 15. Estimated 2014 Employment Control Totals for XXXX County and the Laredo Metorpolitan Area Boundary
employee_data = "employment_spreadsheets/EMP_SUMMARY_County.xls"

#Table 16. Population to Employment Ratio Trend for XXXX County Based on TWC Employment, 2000-2015
employee_ratio_data = "employment_spreadsheets/MPO_County_EMP_POP_1998_2017.xlsx"