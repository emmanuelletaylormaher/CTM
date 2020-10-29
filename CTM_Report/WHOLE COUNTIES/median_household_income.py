# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:46:17 2019

@author: slq584
"""

import pandas as pd
import numpy as num
import matplotlib.pyplot as plt

import paths as p
import API_call as api
import population_growth as pop
import population_trends as popt

"""

"""
def get_nominal(county, base_year, fips):
    #Read file for data prior to 2000
    income_data = pd.read_excel("Historical_Median_Income_TXcounties1969-89.xlsx")    
    income_data = income_data.loc[income_data['Name'] == county]
    
    #Only a figure for the base year is needed.
    #Source of this data is determined by these conditional statements looking
    #For both County Specified and Base Year
    if(base_year == float(2000)):
        if(county == "State of Texas"):
            nominal = api.api_request("https://api.census.gov/data/2000/sf3?get=HCT012001,NAME&for=state:48&key=" + p.census_api_key)
            nominal = pop.string_converter("state", pop.splitter(nominal))
        else:
            nominal = api.api_request(p.frankenstein(p.nominal2000, fips))
            nominal = pop.string_converter("county", pop.splitter(nominal))
        nominal = float(nominal["HCT012001"])
    elif(base_year < float(2000)):
        nominal = income_data[base_year].values[0]
    else:
        if(county == "State of Texas"):
            nominal = api.api_request("https://api.census.gov/data/"+ str(base_year) +"/acs/acs1?get=NAME,B19013_001E&for=state:48&key=" + p.census_api_key)
            nominal = pop.string_converter("state", pop.splitter(nominal))
        else:
            nominal = api.api_request(p.acs_frankenstein(str(base_year), "B19013_001E", fips, "1"))
            if(nominal is None):
                return None
            else:
                nominal = popt.table3_string_converter(pop.splitter(nominal))
        nominal = float(nominal["B19013_001E"])
        
    return nominal
    
"""
get_constant() PURPOSE:
    Gets the constant value of the median household income.
"""
def get_constant(nominal, cpi):
    if(nominal == None):
        return None
    else:
        return nominal-(nominal * num.absolute(cpi))


"""
get_cpi() PURPOSE:
    Gets the CPI to calculate the constant value
"""
def get_cpi(year, base_year):
    #Read file containing CPI values (used regardless of dates specified)
    cpi_data = pd.read_excel(p.cpi)
    
    #Get CPI values for both the base year and year (used in calculation)
    base_year_cpi = cpi_data.loc[cpi_data['Year'] == base_year]
    base_year_cpi = base_year_cpi["Avg"].values[0]
    
    year_cpi = cpi_data.loc[cpi_data['Year'] == year]
    year_cpi = year_cpi["Avg"].values[0]
    
    #Calculate cpi
    cpi = (year_cpi-base_year_cpi)/base_year_cpi
    return cpi

"""
inflator() PURPOSE:
    Calculates Nominal Dollar Amount for year specified.
    
    NOTE: Base Year for calculations is currently 1970
    
"""
def table10_columns(county, year, base_year, fips):
    
    #Get nominal value
    nominal = get_nominal(county, base_year, fips)
    
    #Calculate Constant Dollars Based on Nominal Data
    cpi = get_cpi(year, base_year)
    #print("nominal: ", nominal, " cpi: ", cpi, "base year: ", base_year)
    constant = get_constant(nominal, cpi)
    
    if(nominal != None):
        nominal = '${:,.0f}'.format(nominal)
        constant = '${:,.0f}'.format(constant)
    else:
        nominal = None
        constant = None
    
    
    return [constant, nominal]
    
"""
make_table10() PURPOSE:
    Make table 10.
"""
def make_table10(fips, county):
    
    #Create two separate DataFrames for County and State Data
    county_table = pd.DataFrame({"1970": table10_columns(county, 1970, 1970, fips),
                                 "1980": table10_columns(county, 1970, 1980, fips),
                                 "1990": table10_columns(county, 1970, 1990, fips),
                                 "2000": table10_columns(county, 1970, 2000, fips),
                                 "2010": table10_columns(county, 1970, 2010, fips)})
    
    
    texas_table = pd.DataFrame({"1970": table10_columns("State of Texas", 1970, 1970, fips),
                                 "1980": table10_columns("State of Texas", 1970, 1980, fips),
                                 "1990": table10_columns("State of Texas",1970, 1990, fips),
                                 "2000": table10_columns("State of Texas", 1970, 2000, fips),
                                 "2010": table10_columns("State of Texas", 1970, 2010, fips)})

    
    #Declare what's essentially a blank row dedicated to the title of each
    #table subsection
    line = pd.DataFrame({"1970": " ", "1980": " ", "1990": " ", "2000": " ", "2010": " "}, index=[0])
    
    #Add the blank row to the top of each subtable
    county_table = pd.concat([line, county_table.iloc[0:]], sort=True).reset_index(drop=True)
    texas_table = pd.concat([line, texas_table.iloc[0:]], sort=True).reset_index(drop=True)
    
    #Concatenate accordingly and rename indices
    table10 = pd.concat([county_table, texas_table], sort=False).reset_index(drop=True)
    table10.name = "Table 10. Median Household Income for " + county + " County and Texas 1970-2010"
    county_name = county + " County"
    table10 = table10.rename(index={0: county_name, 1: "Constant Dollars",
                                    2: "Nominal Dollars", 3: "Texas", 4: "Constant Dollars",
                                    5: "Nominal Dollars"})
    
    return table10

"""
make_figure5() PURPOSE:
    Make figure 5. 
"""
def make_figure5(fips, county):
    
    nominal = []
    constant = []
    
    base_years = [1970, 1980, 1990, 2000, 2010]
    year = 1970
    
    #Make nominal and constant columns using loops
    for yr in base_years:
        nominal.append(get_nominal(county, yr, fips))
        
    for value in range(len(base_years)):
        cpi = get_cpi(year, base_years[value])
        const = get_constant(nominal[value], cpi)
        constant.append(get_constant(nominal[value], cpi))
        
    figure5 = pd.DataFrame({"Nominal": nominal, "Constant": constant})
    plt.plot(base_years, 'Nominal', data=figure5, marker='o', color='darkgoldenrod')
    plt.plot(base_years, "Constant", data=figure5, marker='o', color='goldenrod')
    plt.legend()
    plt.suptitle("Figure 5. Historic Median Household for Income " + county + " County 1970-2010 in Nominal and Constant Dollars")
    
    textvar = plt.figtext(0, .01, "Source: U.S. Census Bureau", ha='left')
    
    ax = plt.axes()
    ax.yaxis.grid(True)
    
    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)
    
    
    p.savepng(plt, county, "figure5")
    return plt
    
"""
make_table11() PURPOSE:
    Make table 11.
"""
def make_table11(fips, county, year):
    
    #calls to api
    estimate_data = api.api_request(p.acs_frankenstein(year, "B19013_001E", fips, "1"))
    
    if(estimate_data is None):
        table11 = pd.DataFrame({"Lower Limit": ["No Data"],
                                "Estimate": ["No Data"],
                                "Upper Limit": ["No Data"]})
        return table11
    
    estimate_data = popt.table3_string_converter(pop.splitter(estimate_data))
    margin = api.api_request(p.acs_frankenstein(year, "B19013_001M", fips, "1"))
    margin = popt.table3_string_converter(pop.splitter(margin))
    
    #perform calculations (as needed) and reformat data into currency
    estimate = "${:,.0f}".format(float(estimate_data["B19013_001E"]))
    lower_limit = "${:,.0f}".format(float(estimate_data["B19013_001E"])-float(margin["B19013_001M"]))
    upper_limit = "${:,.0f}".format(float(estimate_data["B19013_001E"])+float(margin["B19013_001M"]))
    
    #create table 11
    table11 = pd.DataFrame({"Lower Limit": [lower_limit],
                            "Estimate": [estimate],
                            "Upper Limit": [upper_limit]})
    #Rename index and define titles
    table11 = table11.rename(index={0: "One-Year ACS"})
    table11.columns=pd.MultiIndex.from_product([[ year + " Median Household Income Range"],
                                               table11.columns])
    table11.name = "Table 11. ACS " + year + " Estimated Median Household Incom for Lubbock County in " + year + " Dollars."
    return table11




def main(fips, county):
 
    #fips = "303"
    #county = "Lubbock"
    
    
    figures = []
    
    table10 = make_table10(fips, county)
    figures.append(table10)
    
    table11 = make_table11(fips, county, "2012")
    figures.append(table11)
    
    plt.close()
    plt.cla()
    
    make_figure5(fips, county)
    
    
    return figures

    
    

if __name__ == "__main__":
    #execute only if run as a script
    main()