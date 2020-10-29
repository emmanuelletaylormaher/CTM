# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 09:48:48 2019

PROGRAM PURPOSE:
    Creates the following graphics for the CTM:
        -Table 3. Comparison of Recent Population Estimates and Growth Rates for xxxx County, 2010-2012
        -Table 4. Population projection and Percent Change for xxxx County
        -Figure 3. Population Projections for xxxx County through 2045

@author: slq584
"""
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.ticker import FuncFormatter

import pandas as pd

import paths as p
from API_call import api_request

import population_growth as pop



"""
get_population_TDC() PURPOSE:
    Grabs population from TDC .csv file, specified by FIPS code and year
    desired
"""
def get_population_TDC(data_TDC, year, fips):
    
    #the TDC dataset is MASSIVE. we need to subset the rows not only by
    #FIPS code, but by year as well. 
    subset_by_fips = data_TDC[data_TDC['FIPS']==fips]
    subset_by_year = subset_by_fips[subset_by_fips['year'] == year]
    #Get total projected population from the subset
    population = subset_by_year['total'].values[0]
    
    return population

"""
table3_string_converter() PURPOSE:
    Converts string into a dictionary and is thus, easier to manipulate.
    This string converter was made specfically for Table 3.
"""
def table3_string_converter(string):
    
        li = list(string.split(","))
        #print(li)
        li.pop(5)
        #print(li)
        li.pop(2)
        subli1 = li[:3]
        subli2 = li[3:]
        conversion = dict(zip(subli1,subli2))
        #print(conversion)
        return conversion
    
"""
base_year_data() PURPOSE:
    Provides data from the base year. Return data ideally is to be plugged into
    other functions.
"""    
def base_year_data(fips):
    called_data = api_request(p.frankenstein(p.table1_call_2010, fips))
    called_data = pop.string_converter('county', pop.splitter(called_data))
    #print(called_data)
    converted_data = float(called_data['P001001'])

    return converted_data
    
"""
make_table3() PURPOSE:
    Creates table 3.
"""   
def make_table3(data_ACS, data_TDC, year, fips):
    
    estimate = float(data_ACS['B01003_001E'])    
    population_change = estimate - base_year_data(fips)
    percent_change = pop.percent_growth(base_year_data(fips), estimate)
    compound_percent_change = pop.compound_percent_growth(base_year_data(fips), estimate, 2)
    
    estimate_TDC = get_population_TDC(data_TDC, year, float(fips))
    population_change_TDC = estimate_TDC - base_year_data(fips)
    percent_change_TDC = pop.percent_growth(base_year_data(fips), estimate_TDC)
    compound_percent_change_TDC = pop.compound_percent_growth(base_year_data(fips), estimate_TDC, 2)
    
    table3 = pd.DataFrame({ 'TDC': [estimate_TDC,
                                    population_change_TDC,
                                    percent_change_TDC,
                                    compound_percent_change_TDC],
                            'ACS': [estimate,
                                    population_change,
                                    percent_change,
                                    compound_percent_change]
            })
    
    #Gives Table 3 the "2012 Population Estimates" title
    table3.columns=pd.MultiIndex.from_product([[str(year)+" Population Estimates"],table3.columns])
    #Renames Indices
    table3 = table3.rename(index={0: "Population",
                     1: "Population Change Since 2010",
                     2: "Pct. Change Since 2010",
                     3: "Compound Annual Growth Rate Since 2010 (CAGR)"})
    return table3
    
"""
make_table4() PURPOSE:
    Creates table 4.
"""
def make_table4(data_TDC, fips, county):
    
    #quick converstion to float
    fips = float(fips)
    
    #Get data needed for DataFrame
    population_2010 = get_population_TDC(data_TDC, 2010, fips)
    population_2020 = get_population_TDC(data_TDC, 2020, fips)
    population_2030 = get_population_TDC(data_TDC, 2030, fips)
    population_2040 = get_population_TDC(data_TDC, 2040, fips)
    population_2045 = get_population_TDC(data_TDC, 2045, fips)
    
    #Put data in a tuple for readability
    rows = [population_2010, population_2020, pop.percent_growth(population_2010, population_2020),
            population_2030, pop.percent_growth(population_2020, population_2030),
            population_2040, pop.percent_growth(population_2030, population_2040),
            population_2045, pop.percent_growth(population_2040, population_2045),
            pop.compound_percent_growth(population_2010, population_2045, 35)]
    #Put tuple in DataFrame
    table4 = pd.DataFrame(rows)
    
    #Rename Indices
    table4 = table4.rename(index={0: "2010 Population",
                                  1: "2020 Population",
                                  2: "Percent Change 2010-2020",
                                  3: "2030 Population",
                                  4: "Percent Change 2020-2030",
                                  5: "2040 Population",
                                  6: "Percent Change 2030-2040",
                                  7: "2045 Population",
                                  8: "Percent Change 2040-2045",
                                  9: "CAGR between 2010-2045"})
    #Give table 4 a title
    table4.name = "Table 4. Population projections and Percent Change for " + county + " County."
    
    return table4

"""
make_figure3() PURPOSE:
    Creates figure 3.
"""
def make_figure3(data_TDC, fips, county):
    
    
    #quick converstion to float
    fips = float(fips)
    
    #Get data needed for DataFrame
    population_2010 = get_population_TDC(data_TDC, 2010, fips)
    population_2020 = get_population_TDC(data_TDC, 2020, fips)
    population_2030 = get_population_TDC(data_TDC, 2030, fips)
    population_2040 = get_population_TDC(data_TDC, 2040, fips)
    population_2045 = get_population_TDC(data_TDC, 2045, fips)
   
    """
    #Texas data
    tx_2010 = get_population_TDC(data_TDC, 2010, 0)
    tx_2020 = get_population_TDC(data_TDC, 2020, 0)
    tx_2030 = get_population_TDC(data_TDC, 2030, 0)
    tx_2040 = get_population_TDC(data_TDC, 2040, 0)
    tx_2045 = get_population_TDC(data_TDC, 2045, 0)
    """
    
    #labels = [2010, 2020, 2030, 2040, 2045]
    county_name = county + " County"
    
    #Declare data as a DataFrame
    figure3 = pd.DataFrame({"Year": [2010, 2020, 2030, 2040, 2045],
                            county_name : [population_2010, population_2020,
                                           population_2030, population_2040,
                                           population_2045]})
    #Put DataFrame into a plot
    
    plt.plot(figure3['Year'], figure3[county_name], linestyle='solid',
             marker='o', color='darkgoldenrod')
 
    
    #ax.set_ylim(0, .3)
    #ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.grid('off', which='major', axis='y')
    plt.suptitle("Figure 3. Population Projections for " + county + " County through 2045")
    darkgoldenrod_line = mlines.Line2D([], [], color='darkgoldenrod',
                                       marker='o', markersize=5,
                                       label=county_name)
    plt.legend(handles=[darkgoldenrod_line])
    textvar = plt.figtext(0, .01, "Source: Texas Demographic Center", ha='left')
    p.savepng(plt, county, "figure3")
    return plt
    
"""
main() PURPOSE:
    Make calls to other functions in this module.
"""
def main(fips, county):
    
    
    figures = []
    
    data_TDC = pd.read_csv(p.table3_excel, sep=r'\,|\t', engine='python')
    #Make call to API for data
    population_ACS = api_request(p.frankenstein(p.table_3_call, fips))
    
    data_ACS = table3_string_converter(pop.splitter(population_ACS))
    
    table3 = make_table3(data_ACS, data_TDC, 2012, fips)
    figures.append(table3)
    
    plt.close()
    
    table4 = make_table4(data_TDC, fips, county)    
    figures.append(table4)
    
    """
    print(table3)
    print(table4)
    """

    figure3 = make_figure3(data_TDC, fips, county)
    figures.append(figure3)
    
    return figures

if __name__ == "__main__":
    #execute only if run as a script
    main()