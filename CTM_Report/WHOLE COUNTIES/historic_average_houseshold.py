# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:15:15 2019

PROGRAM PURPOSE:
    Creates the followng graphics for the CTM:
        -Table 7: Historical Households and Average Household Sizes for
            XXXX County, 1980-2010
        -Figure 4: Trend in Average Household Size for XXXX County, 1980-2010

@author: slq584
"""
import pandas as pd
import matplotlib.pyplot as plt

import paths as p
import API_call as api
import population_growth as pop

"""
get_excel_data() PURPOSE:
    Get Number of Households and Average Household Size from Excel files
    containing data that predates the 2000s
"""
def get_excel_data(data, county, decade):
    
    #Dataframe to hold data
    df = pd.DataFrame()
    df = pd.read_excel(data)
    
    #Subset the row based on county
    subset_row = df[df['COUNTY'] == county]

    if(decade == 1980):
        #Assign information we are looking for to variables
        household_number = subset_row['C75001'].values[0]
        household_average = subset_row['Unnamed: 10'].values[0]
        household_average = round(household_average, 2)
    elif(decade == 1990):
        #Assign information we are looking for to variables
        household_number = subset_row['EUO001'].values[0]
        household_average = subset_row['Unnamed: 12'].values[0]
        household_average = round(household_average, 2)

    #Package these variables in a Dataframe since we need to return
    #more than one value
    data_needed = pd.DataFrame([{'Number': household_number,
                                'Average': household_average}])

    return data_needed

"""
table7_string_converter() PURPOSE:
    Convert string into a dictionary for later implementation.
    This function was made specifically for table 7.
"""
def table7_string_converter(string):
    li = list(string.split(","))
    #print(li)
    li.pop(6)
    #print(li)
    subli1 = li[:4]
    subli2 = li[4:]
    conversion = dict(zip(subli1,subli2))
    #print(conversion)
    return conversion
    
"""
make_table7() PURPOSE:
    Creates table 7 with data passed.
"""
def make_table7(county, county_data_2010, county_data_2000, county_data_2010_number,
                county_data_2000_number, county_data_1990, county_data_1980):
    
    #Assign data to variables for readability    
    household_average_2010 = county_data_2010['H012001']
    household_average_2000 = county_data_2000['H012001']
    
    number_2010 = county_data_2010_number['P020001']
    number_2000 = county_data_2000_number['P020001']
    
    
    #Put all data in a list so that the DataFrame declaration is readable
    values = [county_data_1980['Number'].values[0], county_data_1980['Average'].values[0],
              county_data_1990['Number'].values[0], county_data_1990['Average'].values[0], 
              number_2000, household_average_2000,
              number_2010, household_average_2010,]


    #Rename Columns and establish a MultiIndex
    columns = pd.MultiIndex.from_product([['1980', '1990', '2000', '2010'],
                                          ['Number', 'Avg. HH Size']])
    #Create DataFrame
    table7 = pd.DataFrame([values], columns=columns)
    
    #Rename Index, Index Name, and Establish Name
    table7 = table7.rename(index={0: county+ "County"})
    table7.index.name = 'Area'
    table7.name = 'Historical Households and Average Household Sizes for ' + county + " County, 1980-2010"
    
    return table7

   
"""
make_figure4() PURPOSE:
   Creates figure 4 with data passed. 
"""
def make_figure4(county, county_data_2010, county_data_2000, county_data_1990,
                 county_data_1980):
    
    #Assign data to variables for readability
    household_average_2010 = float(county_data_2010['H012001'])
    household_average_2000 = float(county_data_2000['H012001'])
    
    #Put all data in a list so that the DataFrame declaration is readable
    values = [float(county_data_1980['Average'].values[0]),
              float(county_data_1990['Average'].values[0]),
              household_average_2000, household_average_2010]
    
    #print(values)
    #print(float(county_data_1990['Average'].values[0]))
    
    #Rename Indices
    index = ['1980', '1990', '2000', '2010']
    
    #Create DataFrame
    figure4 = pd.DataFrame(values, index=index)
    
    #Plot Dataframe and make other aesthetic decisions
    ax = figure4.plot(kind= 'bar',
                      width= 0.3,
                      legend = False,
                      rot = 0,
                      color = ['darkgoldenrod','darkgoldenrod',
                               'darkgoldenrod','darkgoldenrod'])
    #ax.set_ylim(2.40, 2.80)
    ax.grid('off', which='major', axis='y')
    plt.suptitle("Figure 4. Trend in Average Household Size for " + county + " County 1980-2010")
    textvar = plt.figtext(0, .01, "Source: U.S. Census Bureau", ha='left')
    p.savepng(plt, county, "figure4")
    textvar.remove()
    return plt

"""
main() PURPOSE:
    Call all other functions and produce output.
""" 
def main(fips, county):
    
    #county = 'Lubbock'
    #fips = '303'
    
    figures = []
    
    #Fulfills the 'Number' Column of the Table
    county_data_2010_number = api.api_request(p.frankenstein(p.table_7_call_2010_number, fips))
    county_data_2000_number = api.api_request(p.frankenstein(p.table_7_call_2000_number, fips))
    
    #Fulfills the 'Avg. HH Size' Column of the Table
    county_data_2010 = api.api_request(p.frankenstein(p.table_7_call_2010, fips))
    county_data_2000 = api.api_request(p.frankenstein(p.table_7_call_2000, fips))
    
    #All necessary data prior to 2000
    county_data_1990 = get_excel_data(p.table7_excel_1990, county, 1990)
    county_data_1980 = get_excel_data(p.table7_excel_1980, county, 1980)
    
    
    county_data_2010 = table7_string_converter(pop.splitter(county_data_2010))
    county_data_2000 = table7_string_converter(pop.splitter(county_data_2000))
    county_data_2010_number = pop.string_converter("county", 
                                                   pop.splitter(county_data_2010_number))
    county_data_2000_number = pop.string_converter("county",
                                                   pop.splitter(county_data_2000_number))
    

    table7 = make_table7(county, county_data_2010, county_data_2000, county_data_2010_number,
                county_data_2000_number, county_data_1990, county_data_1980)
    figures.append(table7)
    
    figure4 = make_figure4(county, county_data_2010, county_data_2000, county_data_1990,
                 county_data_1980)
    figures.append(figure4)
    
    plt.close()
    plt.cla()
    
    """
    #Gets written to Excel
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Table 7')
    writer.sheets['Table 7'] = worksheet
    worksheet.write_string(0, 0, table7.name)
    
    table7.to_excel(writer, sheet_name='Table 7', startrow=1, startcol=0)
    """
    
    return figures
    

if __name__ == "__main__":
    #execute only if run as a script
    main()