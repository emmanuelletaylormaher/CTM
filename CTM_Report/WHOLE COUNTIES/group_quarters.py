# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 09:02:25 2019

PROGRAM PURPOSE:
    Creates the following graphics for the CTM:
        -Table 5. Recent Trends in Group Quartres for XXXX County

@author: slq584
"""
import pandas as pd

import API_call as api
import paths as p
import population_growth as pop
import population_trends as poptrends


"""
group_quarters_array() PURPOSE:
    Create a list containing values for each row of data needed in table 5.
    Allows for readability when declaring DataFrame in make_table5().
"""
def group_quarters_array(fips):
    #Make calls to the API
    #2010
    total_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_total, fips))
    correctional_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_correctional, fips))
    juvenile_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_juvenile, fips))
    nursing_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_nursing, fips))
    other_institutional_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_otherinstitutional, fips))
    total_institutional_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_totalinstitutional, fips))
    dorms_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_dorms, fips))
    military_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_military, fips))
    other_noninstitutional_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_othernoninstitutional, fips))
    total_noninstitutional_2010 = api.api_request(p.frankenstein(p.table_5_call_2010_totalnoninstitutional, fips))
    
    #Turn these requests into something readable
    total_2010 = pop.string_converter("county", pop.splitter(total_2010))
    correctional_2010 = pop.string_converter("county", pop.splitter(correctional_2010))
    juvenile_2010 = pop.string_converter("county", pop.splitter(juvenile_2010))
    nursing_2010 = pop.string_converter("county", pop.splitter(nursing_2010))
    other_institutional_2010 = pop.string_converter("county", pop.splitter(other_institutional_2010))
    total_institutional_2010 = pop.string_converter("county", pop.splitter(total_institutional_2010))
    dorms_2010 = pop.string_converter("county", pop.splitter(dorms_2010))
    military_2010 = pop.string_converter("county", pop.splitter(military_2010))
    other_noninstitutional_2010 = pop.string_converter("county", pop.splitter(other_noninstitutional_2010))
    total_noninstitutional_2010 = pop.string_converter("county", pop.splitter(total_noninstitutional_2010))


    #Make an array

    group_quarter_data = [total_2010["P029026"], correctional_2010["PCT020003"],
                          juvenile_2010["PCT020010"], nursing_2010["P042005"],
                          other_institutional_2010["PCT020015"], 
                          total_institutional_2010["P042002"],
                          dorms_2010["P042008"], military_2010["P042009"],
                          other_noninstitutional_2010["PCT020026"],
                          total_noninstitutional_2010["P029028"]]

    return group_quarter_data 

"""
totals_only_array() PURPOSE:
    Returns a list that contains the total group quarter population in the
    first index and empty strings for the remaining indices.
    
    NOTE: The API request is made to the ACS 1-Year Database.
"""
def table_5_other_columns(fips, year):
    #Make API call and reformat to be a useable dictionary
    data = api.api_request(p.acs_frankenstein(year, "B26001_001E", fips, "1"))
    
    if (data is None):
        percent_of_population = "No Data"
        total = "No Data"
    else:
        county_population = api.api_request(p.acs_frankenstein(year, "B01001_001E", fips, "1"))
        county_population = poptrends.table3_string_converter(pop.splitter(county_population))
        
        group_quarters_total = poptrends.table3_string_converter(pop.splitter(data))
        
        total = group_quarters_total["B26001_001E"]
        percent_of_population = "{0:.2%}".format(float(group_quarters_total["B26001_001E"])/float(county_population["B01001_001E"]))
    
    #Create List that abides by the format of table 5's rows
    totals_only_array = [total, " ", " ", " ", " ", " ", " ", " ", 
                         " ", " ", percent_of_population]
    return totals_only_array

"""
make_table5() PURPOSE:
    Creates table 5.
"""
def make_table5(fips, county):
    group_quarter_data = group_quarters_array(fips)
    column_2 = table_5_other_columns(fips, "2011")
    column_3 = table_5_other_columns(fips, "2012")
    
    data_2010 = api.api_request(p.frankenstein(p.table1_call_2010, fips))
    
    data_2010 = pop.string_converter("county", pop.splitter(data_2010))
    total_population_2010 = float(data_2010["P001001"])
    
    percent_of_population_2010 = "{0:.2%}".format(float(group_quarter_data[0])/total_population_2010)
    
    
    group_quarter_data.append(percent_of_population_2010)
    
    table5 = pd.DataFrame({"2010": group_quarter_data,
                           "2011": column_2,
                           "2012": column_3})
    table5 = table5.rename(index={0: "Total",
                         1: "Correctional Institutions",
                         2: "Juvenile Institutions",
                         3: "Nursing Homes",
                         4: "Other Institutions",
                         5: "Total Institutional",
                         6: "College Dorms",
                         7: "Military Quarters",
                         8: "Other Non-Institutional",
                         9: "Total Non-Institutional",
                         10: "Percent of Total Population"})
    table5.name = "Recent Trends in Group Quarters Population for " + county + " County"
    
    return table5
"""
main() PURPOSE:
    Display Table 5 and Table 6.
"""
def main(fips, county):
    
    #fips = "303"
    #county = "Lubbock"

    figures = []
    
    table5 = make_table5(fips, county)
    figures.append(table5)
    
    return figures
    
    
    
    
if __name__ == "__main__":
    #execute only if run as a script
    main()