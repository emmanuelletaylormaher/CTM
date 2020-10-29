# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:07:41 2019

PROGRAM PURPOSE:
    Creates the followng graphics for the CTM:
        -Figure 1: Population Growth in xxxx County [TIMEFRAME]
        -Table 1: Population Percent Change for xxx County and Texas, [TIMEFRAME]
        -Figure 2: Population Percent Change for xxx County and Texas by Decade, [TIMEFRAME]
        -Table 2: Historic Average Annual Compound Population Growth Rate by Decade for xxx
            County and Texas

@author: slq584
"""
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.ticker import FuncFormatter

import pylab as pl

import paths as p
from API_call import api_request

data = pd.DataFrame()
data = pd.read_excel(p.table1_excel)

"""
percent_growth() PURPOSE:
    Calculate a percentage growth between two years.
"""
def percent_growth(base_year, comparator):
    #Calculate percentage growth
    equation = (comparator - base_year)/base_year
    #Reformat into a percentage rounded at 2 decimal places
    result = "{0:.2%}".format(equation)
    return result

"""
compound_percent_growth() PURPOSE:
    Calculate the Average Annual Percentage Growth
"""
def compound_percent_growth(base_year, comparator, years):
    #Calculate compound percentage growth
    equation = pow((comparator/base_year), (1/years))-1
    #Reformat into a percentage rounded at 2 decimal places
    result = "{0:.2%}".format(equation)
    return result

"""
percent_string_to_float() PURPOSE:
    Undoes the string formatting of percent_growth(), thereby returning the
    argument passed to a float.
"""
def percent_string_to_float(string_percent):
    new_float = float(string_percent.strip("%"))/100
    return new_float
    

"""
splitter() PURPOSE:
    Take API string and get rid of superfluous characters
"""
def splitter(string):
    print("string in splitter:", string)
    #Get rid of extraenous brackets
    string = string.replace("[", "")
    print("change 1", string)
    string = string.replace("]", "")
    print("change 2", string)
    #Same thing goes for the quotation marks
    string = string.replace("\"", "")
    print("change 3", string)
    #As well as the newline
    string = string.replace("\n", "")
    print("change 4", string)
    print(type(string))
    print("test text ?????")

    return string
    
"""
string_converter() PURPOSE:
    Take string and convert information into a dictionary
"""
def string_converter(state_or_county,string):
    #take string and delimit it by commas
    #print("string to be converted: ",string)
    #variable checks state_or_county variable for clarification.
    #splitting of string occurs differently based on value
    if(state_or_county == 'state'):
        li = list(string.split(","))
        subli1 = li[:3]
        subli2 = li[3:]
        conversion = dict(zip(subli1,subli2))
        return conversion
    elif(state_or_county == 'county'):
        li = list(string.split(","))
        li.pop(6)
        subli1 = li[:4]
        subli2 = li[4:]
        conversion = dict(zip(subli1,subli2))
        return conversion
    else:
        print("ERROR WITH FIRST ARGUMENT PASSED TO FUNCTION")
        return None

"""
find_population(): PURPOSE:
    Find population data from excel file.
"""
def find_population(fips_county, fips_state, year, data):
    #Concatenate State and County FIPS codes and convert to integer for search
    fips_whole = int(str(fips_state)+str(fips_county))
    #Find population data based on fips_whole and year passed
    data_fipsrow = data.loc[data.FIPS==fips_whole, year]
    #Return value
    return data_fipsrow.values[0]


"""
make_figure1() PURPOSE:
    Create Figure 1.    
    
     NOTE: variable "reference_data" can be passed any relevant dataset derived
          from the API call. we simply use this data to refer to names of columns.
"""
def make_figure1(population_1970, population_1980, population_1990,
                 population_2000, population_2010, reference_data):
    #construct DataFrame containing passed variables
    figure1 = pd.DataFrame({
            'Year':['1970', '1980', '1990', '2000', '2010'],
            'Population':[population_1970, population_1980, population_1990,
                 population_2000, population_2010]})
    
    #Create plot based on DataFrame
    plt.plot(figure1['Year'], figure1['Population'], linestyle='solid',
             marker='o', color='darkgoldenrod')
    #Title of plot
    plt.suptitle("Figure 1. Population Growth in "+ reference_data['NAME'] + " 1970-2010.")
    
    #Aesthetic calibrations for readability
    #plt.ylim((0,300000))
    plt.grid(True)
    textvar = plt.figtext(0, .01, "Source: U.S. Census Bureau", ha='left')
    darkgoldenrod_line = mlines.Line2D([], [], color='darkgoldenrod',
                                       marker='o', markersize=5,
                                       label=reference_data['NAME'])
    plt.legend(handles=[darkgoldenrod_line])
    p.savepng(plt, reference_data['NAME'][:-7], "figure1")
    return plt

"""
make_table1() PURPOSE:
    Create table 1.
    
    NOTE: variable "reference_data" can be passed any relevant dataset derived
          from the API call. we simply use this data to refer to names of columns.
"""
def make_table1(state_population_2010, state_population_2000, state_population_1990,
                state_population_1980, state_population_1970, population_2010,
                population_2000, population_1990, population_1980, population_1970,
                reference_data):
    #construct DataFrame containing values based on prior variables
    #the Percent Population Change is calculated concurrently    
    table1 = pd.DataFrame({'1970-80':[percent_growth(population_1970, population_1980),
                                      percent_growth(state_population_1970, state_population_1980)],
                           '1980-90':[percent_growth(population_1980, population_1990),
                                      percent_growth(state_population_1980, state_population_1990)],
                           '1990-00':[percent_growth(population_1990, population_2000),
                                      percent_growth(state_population_1990, state_population_2000)],
                           '2000-10':[percent_growth(population_2000, population_2010),
                                      percent_growth(state_population_2000, state_population_2010)],
                           '1970-2010':[percent_growth(population_1970, population_2010),
                                        percent_growth(state_population_1970, state_population_2010)]})
    
    #Gives Table 1 the "Percent Growth" title
    table1.columns=pd.MultiIndex.from_product([["Percent Growth"],table1.columns])
    #Renames Indices
    table1 = table1.rename(index={0: reference_data['NAME'],
                     1: "State of Texas"})
    table1.name = "Table 1. Population Percent Change for "+reference_data['NAME']+" and Texas, 1970-2010."
    
    #county_name = reference_data['NAME']
    return table1

"""
make_figure2() PURPOSE:
    Create Figure 2.    
    
     NOTE: variable "reference_data" can be passed any relevant dataset derived
          from the API call. we simply use this data to refer to names of columns.
"""
def make_figure2(state_population_2010, state_population_2000, state_population_1990,
                state_population_1980, state_population_1970, population_2010,
                population_2000, population_1990, population_1980, population_1970,
                reference_data):
    
    #Get the only thing we need from the reference_data variable
    county_name = reference_data['NAME']
    
    #Since this figure relies on two sets of data, there are several lists
    #that hold the data for the respective datasets.
    #indices have been labeled appropriately
    county_population_percentages = [percent_string_to_float(
                                             percent_growth(population_1970, population_1980)),
                                     percent_string_to_float(
                                             percent_growth(population_1980, population_1990)),
                                     percent_string_to_float(
                                             percent_growth(population_1990, population_2000)),
                                     percent_string_to_float(
                                             percent_growth(population_2000, population_2010))]
    state_population_percentages = [percent_string_to_float(
                                            percent_growth(state_population_1970, state_population_1980)),
                                    percent_string_to_float(
                                            percent_growth(state_population_1980, state_population_1990)),
                                    percent_string_to_float(
                                            percent_growth(state_population_1990, state_population_2000)),
                                    percent_string_to_float(
                                            percent_growth(state_population_2000, state_population_2010))]
    
    #percent_growth() formats the percentages and returns a string.
    #the following for loops iterate through the lists and convert them back
    #to floats. otherwise, these values cannot be plotted

    
    #Indices for the figure
    index = ['1970-80', '1980-90', '1990-00', '2000-10' ]
    
    #This data is then plugged into a DataFrame
    figure2 = pd.DataFrame({county_name: county_population_percentages,
                           'State of Texas': state_population_percentages}, index=index)
    #Create a bar graph from DataFrame and reconfigure for readability
    ax = figure2.plot(kind= 'bar',
                      legend=True,
                      width= 0.75,
                      rot = 0,
                      color = ['darkgoldenrod', 'goldenrod',
                               'darkgoldenrod', 'goldenrod',
                               'darkgoldenrod', 'goldenrod',
                               'darkgoldenrod', 'goldenrod'])
    #ax.set_ylim(0, .3)
    ax.grid('off', which='major', axis='y')
    textvar = plt.figtext(0, .01, "Source: U.S. Census Bureau", ha='left')
    plt.suptitle("Figure 2. Population Percent Change for "+county_name+" and Texas by Decade, 1970-2010")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    p.savepng(plt, county_name[:-7], "figure2")
    return plt
"""
make_table2() PURPOSE:
    Create table 2.
    NOTE: variable "reference_data" can be passed any relevant dataset derived
          from the API call. we simply use this data to refer to names of columns.
"""
def make_table2(state_population_2010, state_population_2000, state_population_1990,
                state_population_1980, state_population_1970, population_2010,
                population_2000, population_1990, population_1980, population_1970,
                reference_data):
    #construct DataFrame containing values based on prior variables
    #the Percent Population Change is calculated concurrently    
    table2 = pd.DataFrame({'1970-80':[compound_percent_growth(population_1970, population_1980, 10),
                                      compound_percent_growth(state_population_1970, state_population_1980, 10)],
                           '1980-90':[compound_percent_growth(population_1980, population_1990, 10),
                                      compound_percent_growth(state_population_1980, state_population_1990, 10)],
                           '1990-00':[compound_percent_growth(population_1990, population_2000, 10),
                                      compound_percent_growth(state_population_1990, state_population_2000, 10)],
                           '2000-10':[compound_percent_growth(population_2000, population_2010, 10),
                                      compound_percent_growth(state_population_2000, state_population_2010, 10)],
                           '1970-2010':[compound_percent_growth(population_1970, population_2010, 40),
                                        compound_percent_growth(state_population_1970, state_population_2010, 40)]})
    
    #Gives Table 1 the "Percent Growth" title
    table2.columns=pd.MultiIndex.from_product([["Compound Average Annual Growth Rate"],
                                               table2.columns])
    #Renames Indices
    table2 = table2.rename(index={0: reference_data['NAME'],
                     1: "State of Texas"})
    table2.name = "Table 2. Historic Average Annual Compound Population Growth Rate by Decade for " + reference_data['NAME'] + " and Texas"  
    
    #county_name = reference_data['NAME']
    return table2

"""
main() PURPOSE:
    Make calls to other functions in this module.
"""
def main(fips):
    
    figures = []
    
    #variables containing state data
    state_data_2010 = api_request(p.table1_call_state_2010)
    print("this is the data after api requst: ",type(state_data_2010))
    state_data_2010 = string_converter('state', splitter(state_data_2010))
    state_population_2010 = float(state_data_2010['P001001'])
    
    state_data_2000 = api_request(p.table1_call_state_2000)
    print("TEST TEST TEST:", state_data_2000)
    state_data_2000 = string_converter('state', splitter(state_data_2000))
    state_population_2000 = float(state_data_2000['P001001'])

    state_population_1970 = find_population("000", 48, 1970, data)
    state_population_1980 = find_population("000", 48, 1980, data)
    state_population_1990 = find_population("000", 48, 1990, data)

    #variables containing census data
    data_2010 = api_request(p.frankenstein(p.table1_call_2010, fips))
    data_2010 = string_converter('county', splitter(data_2010))
    population_2010 = float(data_2010['P001001'])
    
    data_2000 = api_request(p.frankenstein(p.table1_call_2000, fips))
    data_2000 = string_converter('county', splitter(data_2000))
    population_2000 = float(data_2000['P001001'])

    population_1970 = find_population(data_2010['county'], data_2010['state'], 1970, data)
    population_1980 = find_population(data_2010['county'], data_2010['state'], 1980, data)
    population_1990 = find_population(data_2010['county'], data_2010['state'], 1990, data)


    figure1 = make_figure1(population_1970, population_1980, population_1990,
                 population_2000, population_2010, data_2010)
    
    figures.append(figure1)
    
    plt.close()
    
    table1 = make_table1(state_population_2010, state_population_2000, state_population_1990,
                state_population_1980, state_population_1970, population_2010,
                population_2000, population_1990, population_1980, population_1970,
                data_2010)
    
    figures.append(table1)
    
    figure2 = make_figure2(state_population_2010, state_population_2000, state_population_1990,
                state_population_1980, state_population_1970, population_2010,
                population_2000, population_1990, population_1980, population_1970,
                data_2010)
    
    plt.close()
    
    figures.append(figure2)
    
    table2 = make_table2(state_population_2010, state_population_2000, state_population_1990,
                state_population_1980, state_population_1970, population_2010,
                population_2000, population_1990, population_1980, population_1970,
                data_2010)
    
    figures.append(table2)

    """
    #Prints to Console
    figure1.show()
    print(table1)
    figure2.show()
    print(table2)

    
    #Gets written to Excel
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Results')
    writer.sheets['Results'] = worksheet
    worksheet.write_string(0, 0, table1.name)
    
    table1.to_excel(writer, sheet_name='Results', startrow=1, startcol=0)
    worksheet.write_string(table1.shape[0] + 4, 0, table2.name)
    table2.to_excel(writer,sheet_name='Results', startrow=table1.shape[0]+5, startcol=0)
    #figure1.to_excel('output.xlsx', sheet_name='figures', engine='xlsxwriter')
    writer.save()
    """
    
    return figures

if __name__ == "__main__":
    #execute only if run as a script
    main()