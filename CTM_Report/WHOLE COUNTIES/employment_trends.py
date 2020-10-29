# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:20:13 2019

PROGRAM PURPOSE:
    Creates the followng graphics for the CTM:
        - Table 14. Historic Employment by Type for XXXX County 
        - Figure 7. Historic Employment by Type for XXXX County, 1990-2010 2014 Base Year Employment Control Totals 
        - Table 15. Estimated 2014 Employment Control Totals for XXXX County
        - Table 16. Population to Employment Ration Trend for XXXX County Based on TWC Employment 1995-2010 
        - Table 17. Recent Population to Employment Ratio Trend for XXXX County Based on TWC Employment 2010-2014 
        - Table 18. Recent Trends in Employment by Type in XXXX County, 2010-2014 
        - Tables 19 and 20 cannot be programmed.
        - Table 21. Example Estimating 2045 Employment Using Values within Control Total Ranges using the 0.5 Migration Scenario. **(undeveloped)**

@author: slq584
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tickformat
import numpy as np

import paths as p
import API_call as api

"""
employee_total() PURPOSE:
    Calculate the total number of employed individuals (across different
    types of employment) for years prior to 2014
"""
def employee_total(year, county, paths):
    
    total = 0 
    
    for value in paths.values():
        data = pd.read_excel(value)
        #Locate data by county and year
        data = data.loc[data.County == county]
        data = data.loc[data.Year == year]
        #Create a running total of the row's values summed up
        total += data["Quarterly Employment"].values[0]
        
    return total

"""
find_population(): PURPOSE:
    Find the population within a specific excel sheet
"""
def find_population(county, year):
    
    print("placeholder")

"""
summation(): PURPOSE:
    Creates a column of totals which are the summations of the row's values.
"""
def summation(paths, starting_year, stopping_year, county, iteration):
    #Declare return column
    return_column = []
    
    #For loop with each year being one  that the table will show data for
    for year in range(starting_year, stopping_year+1, iteration):
    
        #Resets every time we begin a new row of th column
        row_total = 0

        #Goes through every key of paths (each value being a path to an
        #Excel file)
        for value in paths.values():
            data = pd.read_excel(value)
            #Locate data by county and year
            data = data.loc[data.County == county]
            data = data.loc[data.Year == year]
            #Create a running total of the row's values summed up
            row_total += data["Quarterly Employment"].values[0]
        
        #Add finalized row summation as the line in the column    
        return_column.append("{:.0f}".format(row_total))
        
    return return_column

"""
table14_columns() PURPOSE:
    Creates individual columns for number portion of make_table14() thereby 
    minimizing repetitive code
"""
def table14_columns(path, starting_year, stopping_year, county):
    #Declare return column
    return_column = []
    
    #For loop with each year being one  that the table will show data for
    for year in range(starting_year, stopping_year+1, 5):
        
        data = pd.read_excel(path)
        #Locate data by county and year
        data = data.loc[data.County == county]
        data = data.loc[data.Year == year]
        #Add desired value to the column line
        return_column.append("{:.0f}".format(data["Quarterly Employment"].values[0]))
        
    return return_column

"""
table14_percentage_columns() PURPOSE:
    Creates individual columns for percentage portion of make_table14()
"""
def table14_percentage_columns(paths, key, starting_year, stopping_year, county, formatting):
    
    #Call to summation() to create a column of totals that will be used for
    #calculations
    total_column = summation(paths, starting_year, stopping_year, county, 5)
    
    #To increment within the for loop
    index = 0
    
    #Declare return column
    return_column = []
    
    #For loop with each year being one  that the table will show data for   
    for year in range(starting_year, stopping_year+1, 5):
        
        #Key determines which file the function will read from paths[]
        data = pd.read_excel(paths[key])
        
        #Locate data by county and year
        data = data.loc[data.County == county]
        data = data.loc[data.Year == year]
        
        #Calculate the percentage
        percentage = float(data["Quarterly Employment"].values[0])/float(total_column[index])

        index += 1
        
        if formatting == "Y":
            return_column.append("{0:.2%}".format(percentage))
        elif formatting == "N":
            return_column.append(100*percentage)
        
        
    return return_column
    
"""
table18_columns() PURPOSE:
    Creates individual columns for make_table18() thereby minimizing repetitive
    code
"""
def table18_columns(path, starting_year, stopping_year, column, county):
    
    #Declare return list
    return_column = []
    
    #Each loop iteration is a row within the column
    for year in range(starting_year, stopping_year):
        #Switch to appropriate worksheet
        data = pd.read_excel(path, sheet_name="Processed")
        #Locate data based on MPO and year specified
        data = data.loc[data.COUNTY == county]
        data = data.loc[data.YEAR == year]
        #Conditional statements based on data column name to determine whether
        #or not formatting is necessary
        if column[0] == "%":
            return_column.append("{0:.2%}".format(data[column].values[0]))
        else:
            return_column.append(data[column].values[0])
        
    return return_column

"""
figure7_bargroups() PURPOSE:
    Returns a list of percentages of types of employment contingent on year
"""
def figure7_bargroups(paths, column_year, starting_year, stopping_year, county):
    
    keys = ["Basic", "Retail", "Service", "Education"]
    return_column = []
    
    total_column = summation(paths, starting_year, stopping_year, county, 5)
    index = 0
    
    for key in keys:
        
        #Key determines which file the function will read from paths[]
        data = pd.read_excel(paths[key])
        
        #Locate data by county and year
        data = data.loc[data.County == county]
        data = data.loc[data.Year == column_year]
        
        #Calculate the percentage
        percentage = float(data["Quarterly Employment"].values[0])/float(total_column[index])

        return_column.append(100*percentage)
        
    return return_column

"""
print_100() PURPOSE:
    Print an entire column of "100%"s because these don't require calculation.
"""
def print_100(starting_year, stopping_year, iteration):
    
    #Declare return list    
    return_column = []
    
    #Each loop iteration is a row within the column
    for year in range(starting_year, stopping_year, iteration):
        return_column.append("100%")
        
    return return_column

"""
year_column() PURPOSE:
    create a column of years for plotting purposes.
"""
def year_column(starting_year, stopping_year):
    
    #Declare return column
    return_column = []
    
    #Create a list of every 5 from starting_year to stopping_year
    for year in range(starting_year, stopping_year+1, 5):
        return_column.append(year)

    return return_column

"""
make_table14() PURPOSE:
    Create table 14.
"""
def make_table14(paths, county, starting_year, stopping_year):
    
    #There are two parts to Table 8: The Number and Percent Values. 
    #For all Intents and Purposes we declare them separately
    numbers = pd.DataFrame({"Basic": table14_columns(paths["Basic"], starting_year, stopping_year, county),
                            "Retail": table14_columns(paths["Retail"], starting_year, stopping_year, county),
                            "Service": table14_columns(paths["Service"], starting_year, stopping_year, county),
                            "Education": table14_columns(paths["Education"], starting_year, stopping_year, county),
                            "Total": summation(paths, starting_year, stopping_year, county, 5)})
    
    percentage = pd.DataFrame({"Basic": table14_percentage_columns(paths, "Basic", starting_year, stopping_year, county, "Y"),
                               "Retail": table14_percentage_columns(paths, "Retail", starting_year, stopping_year, county, "Y"),
                               "Service": table14_percentage_columns(paths, "Service", starting_year, stopping_year, county, "Y"),
                               "Education": table14_percentage_columns(paths, "Education", starting_year, stopping_year, county, "Y"),
                               "Total": print_100(starting_year, stopping_year+1, 5)})
    
    #Declare what's essentially a blank row dedicated to the title of each
    #table subsection
    line = pd.DataFrame({"Basic": " ", "Retail": " ", "Service": " ", "Education": " ", "Total": " "}, index=[0])
    
    #Add the blank row to the top of each subtable
    numbers = pd.concat([line, numbers.iloc[0:]], sort=True).reset_index(drop=True)
    percentage = pd.concat([line, percentage.iloc[0:]], sort=True).reset_index(drop=True)
    
    #Concatenate accordingly and rename indices
    table14 = pd.concat([numbers, percentage], sort=False).reset_index(drop=True)
    
    table14= table14.rename(index={0: "Number", 1: starting_year, 2: starting_year+5,
                                   3: starting_year+10, 4: starting_year+15, 
                                   5: " ", 6: "Percent", 7: starting_year, 8: starting_year+5,
                                   9: starting_year+10, 10: starting_year+15})
    
    table14.name = "Table 14. Historic Employment by Type for "+county+" County, "+str(starting_year)+"-"+str(stopping_year-1) 
    
    return table14

"""
make_figure7() PURPOSE:
    Create figure 7.
"""   
def make_figure7(paths, county, starting_year, stopping_year):
    
    #Returns a list of years to be added to DataFrame
    #(this is needed for plotting purposes; establishes the x axis)
    years = year_column(starting_year, stopping_year)
    
    #Get dataframe(Of Percentages) (Same data as table 14)
    """
    percentage = pd.DataFrame({"Basic": table14_percentage_columns(paths, "Basic", starting_year, stopping_year, county, "N"),
                               "Retail": table14_percentage_columns(paths, "Retail", starting_year, stopping_year, county, "N"),
                               "Service": table14_percentage_columns(paths, "Service", starting_year, stopping_year, county, "N"),
                               "Education": table14_percentage_columns(paths, "Education", starting_year, stopping_year, county, "N"),
                               "Year": years})
    
    #Declare Axes
    ax = plt.gca()
    
    #Plot lines accordingly
    percentage.plot(kind='line', x="Year", y="Basic", ax=ax)
    percentage.plot(kind='line', x="Year", y="Retail", ax=ax)
    percentage.plot(kind='line', x="Year", y="Service", ax=ax)
    percentage.plot(kind='line', x="Year", y="Education", ax=ax)
    
    #Other aesthetic toggling
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.ylim(0, 50)
    plt.xlim(1985, 2010)
    plt.grid(axis='y', linestyle='-', linewidth='.5')
    
    #In order to get the y-ticks to be formatted correctly
    #We need to get the ticks and iterate through them to adjust
    vals = ax.get_yticks()
    
    for x in range(0, vals.size):
        vals[x] = x/10
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
    """
    
    barWidth = 0.20
    
    data_1990 = figure7_bargroups(paths, 1990, starting_year, stopping_year, county)
    data_1995 = figure7_bargroups(paths, 1995, starting_year, stopping_year, county)
    data_2000 = figure7_bargroups(paths, 2000, starting_year, stopping_year, county)
    data_2005 = figure7_bargroups(paths, 2005, starting_year, stopping_year, county)
    
    r1 = np.arange(len(data_1990))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    
    plt.bar(r1, data_1990, width=barWidth, color = "darkgoldenrod", edgecolor='white', label="Basic")
    plt.bar(r2, data_1995, width=barWidth, color='darkorange', edgecolor='white', label="Retail")
    plt.bar(r3, data_2000, width=barWidth, color='navajowhite', edgecolor='white', label="Service")
    plt.bar(r4, data_2005, width=barWidth, color='goldenrod', edgecolor='white', label="Education")
    
    plt.xticks([r + barWidth for r in range(len(data_1990))], ["Basic", "Retail", "Service", "Education"])
    
    plt.grid(axis="y")
    plt.legend(["1990", "1995", "2000", "2005"])
    plt.gca().yaxis.set_major_formatter(tickformat.PercentFormatter())
    
    plt.suptitle("Figure 7. Historic Employment by Type for " + county + " County, " + str(starting_year) + "-" + str(stopping_year))
    
    textvar = plt.figtext(0, .01, "Source: Texas Workforce Commission", ha='left')
    p.savepng(plt, county, "figure7")
    return plt

"""
make_table15() PURPOSE:
    Create table 15.
"""
def make_table15(county, year, path):
    #Read in Excel file
    data = pd.read_excel(path, sheet_name="Processed")

    #Locate desired row based on Year and MPO
    data = data.loc[data.YEAR == year]
    data = data.loc[data.COUNTY == county]
    

    
   #Put values into table
    table15 = pd.DataFrame({ "Basic": [data['BASIC'].values[0]],
                            "Retail": [data['RETAIL'].values[0]],
                            "Service": [data['SERVICE'].values[0]],
                            "Education": [data['EDUCATION'].values[0]],
                            "Total Employment": [data['TOTAL_EMP'].values[0]]})
    #Rename accordingly
    table15 = table15.rename(index={0: county+" County"})
    table15.name = "Estimated "+str(year)+" Employment Control Totals for "+county+" County"
    return table15

"""
make_table16() PURPOSE:
    Create table 16.
"""
def make_table16(county, starting_year, stopping_year):
    
    years = []
    
    #List of all years to be included in table
    for year in range(starting_year, stopping_year+1, 5):
        years.append(year)
    
    #Get data needed from employment spreadsheet
    data = pd.read_excel(p.employee_ratio_data)
    #Concatenating for lookup purposes
    stwing = county + " County, TX"
    
    columns = []
    
    #Fill columns with pertinent data for each year
    for year in years:
        column = []
        
        row = data.loc[data.County_Name == stwing]
        row = row.loc[row.Year == year]
        
        employment = row["EMP_QCEW"].values[0]
        population = row["Pop"].values[0]        
        ratio = "{0:.0%}".format(row["Emp_Pop"].values[0])
        
        column.extend([employment, population, ratio])
        columns.append(column)
        
        
    table16 = pd.DataFrame()
    
    #Put data in DataFrame
    for index in range(len(years)):
        column = columns[index]
        table16.insert(index, years[index], column, True)
    
    table16 = table16.rename(index={0: "TWC Employment",
                                    1: "Population",
                                    2: "Employment/Population"})
    table16.name = "Population to Employment Ratio Trend for "+ county + " County based on TWC Employment "+ str(starting_year) + "-" + str(stopping_year)
    return table16
      

"""
make_table17() PURPOSE:
    Create table 17.
"""
def make_table17(county, starting_year, stopping_year):
    
    years = []
    
    #List of all years to be included in table
    for year in range(starting_year, stopping_year+1, 1):
        years.append(year)
    
    #Get data needed from employment spreadsheet
    data = pd.read_excel(p.employee_ratio_data)
    #Concatenating for lookup purposes
    stwing = county + " County, TX"
    
    columns = []
    
    #Fill columns with pertinent data for each year
    for year in years:
        column = []
        
        row = data.loc[data.County_Name == stwing]
        row = row.loc[row.Year == year]
        
        employment = row["EMP_QCEW"].values[0]
        population = row["Pop"].values[0]        
        ratio = "{0:.0%}".format(row["Emp_Pop"].values[0])
        
        column.extend([employment, population, ratio])
        columns.append(column)
        
        
    table17 = pd.DataFrame()
    
    #Put data in DataFrame
    for index in range(len(years)):
        column = columns[index]
        table17.insert(index, years[index], column, True)
    
    table17 = table17.rename(index={0: "TWC Employment",
                                    1: "Population",
                                    2: "Employment/Population"})
    table17.name = "Recent Population to Employment Ratio Trend for "+ county + " County based on TWC Employment "+ str(starting_year) + "-" + str(stopping_year)
    return table17


"""
make_table18() PURPOSE:
    Create table 18.
"""
def make_table18(county, path):
    
    #Declare starting and stopping years that will be displayed as rows
    starting_year = 2014
    stopping_year = starting_year + 5
    
    #There are two parts to Table 8: The Number and Percent Values. 
    #For all Intents and Purposes we declare them separately
    numbers = pd.DataFrame({ "Basic": table18_columns(path, starting_year, stopping_year, "BASIC", county),
                               "Retail": table18_columns(path, starting_year, stopping_year, "RETAIL", county),
                               "Service": table18_columns(path, starting_year, stopping_year, "SERVICE", county),
                               "Education": table18_columns(path, starting_year, stopping_year, "EDUCATION", county),
                               "Total": table18_columns(path, starting_year, stopping_year, "TOTAL_EMP", county)})
   
    percent = pd.DataFrame({ "Basic": table18_columns(path, starting_year, stopping_year, "% BASIC", county),
                               "Retail": table18_columns(path, starting_year, stopping_year, "% RETAIL", county),
                               "Service": table18_columns(path, starting_year, stopping_year, "% SERVICE", county),
                               "Education": table18_columns(path, starting_year, stopping_year, "% EDUCATION", county),
                               "Total": print_100(starting_year, stopping_year,1)})
    
    #Declare what's essentially a blank row dedicated to the title of each
    #table subsection
    line = pd.DataFrame({"Basic": " ", "Retail": " ", "Service": " ", "Education": " ", "Total": " "}, index=[0])
    
    #Add the blank row to the top of each subtable
    numbers = pd.concat([line, numbers.iloc[0:]]).reset_index(drop=True)
    percent = pd.concat([line, percent.iloc[0:]]).reset_index(drop=True)
    #Concatenate accordingly and rename indices
    table18 = pd.concat([numbers, percent]).reset_index(drop=True)
    
    table18= table18.rename(index={0: "Number", 1: starting_year, 2: starting_year+1,
                                   3: starting_year+2, 4: starting_year+3, 5: starting_year+4,
                                   6: "Percent", 7: starting_year, 8: starting_year+1,
                                   9: starting_year+2, 10: starting_year+3, 11: starting_year+4})
    
    table18.name = "Table 18. Recent Trends in Employment by Type in "+county+" County, "+str(starting_year)+"-"+str(stopping_year-1) 
    return table18
            
    
def main(county):
    
    #county = "Lubbock"

    path = p.employee_data
    data = pd.read_excel(path)

    paths= {"Basic": p.basic_14, "Retail": p.retail_14, "Service": p.service_14, "Education": p.education_14}
    
    figures = []

    if(county == "Burnet"):
        table14 = pd.DataFrame()
        figure7 = None
    else:
        table14 = make_table14(paths, county, 1990, 2005)
        plt.close()
        plt.cla()
    
        figure7 = make_figure7(paths, county, 1990, 2005)

    figures.append(table14)
    
    
    figures.append(figure7)
    
    
    table15 = make_table15(county, 2014, path)
    figures.append(table15)
    

    table16 = make_table16(county, 2000, 2015)
    figures.append(table16)

    
    table17 = make_table17(county, 2015, 2017)
    figures.append(table17)

    table18 = make_table18(county, path)
    figures.append(table18)

    """
    print(table14)
    figure7.show()
    print(table15)
    print(table18)
    """
    
    return figures
    
    
    
if __name__ == "__main__":
    #execute only if run as a script
    main()