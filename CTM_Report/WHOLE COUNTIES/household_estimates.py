# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:43:51 2019

@author: slq584
"""
import pandas as pd

import API_call as api
import paths as p
import population_trends as p_t
import population_growth as pop


"""
make_table8() PURPOSE:
    Create table 8
    
    NOTE: As of 1/14/2020 data is incomplete. Still needing 
    Number of Households data (and thereby avg HH) for TDC
    is still under development
"""
def make_table8(data_TDC, fips, county, year):
    
    # TDC data
    population_tdc = p_t.get_population_TDC(data_TDC, int(year), int(fips))
    
    gq_tdc = pop.splitter(api.api_request(p.frankenstein(p.table_5_call_2010_total, fips)))
    gq_tdc = pop.string_converter("county", gq_tdc)
    gq_tdc = gq_tdc['P029026']
    
    hh_population_tdc = population_tdc - int(gq_tdc)
    
    number_hh_tdc = " "
    avg_hh_tdc = " "
    
    # Census data
    
    population_acs = pop.splitter(api.api_request(p.acs_frankenstein("2014", "B01003_001E", fips, "5")))
    population_acs = p_t.table3_string_converter(population_acs)
    population_acs = population_acs["B01003_001E"]
    
    gq_acs = pop.splitter(api.api_request(p.acs_frankenstein("2014", "B26001_001E", fips, "5")))
    gq_acs = p_t.table3_string_converter(gq_acs)
    gq_acs = gq_acs["B26001_001E"]
    
    hh_population_acs = pop.splitter(api.api_request(p.acs_frankenstein("2014", "B25008_001E", fips, "5")))
    hh_population_acs = p_t.table3_string_converter(hh_population_acs)
    hh_population_acs = hh_population_acs["B25008_001E"]
    
    number_hh_acs = pop.splitter(api.api_request(p.acs_frankenstein("2014", "B11016_001E", fips, "5")))
    number_hh_acs = p_t.table3_string_converter(number_hh_acs)
    number_hh_acs = number_hh_acs["B11016_001E"]
    
    avg_hh_acs = pop.splitter(api.api_request(p.acs_frankenstein("2014", "B25010_001E", fips, "5")))
    avg_hh_acs = p_t.table3_string_converter(avg_hh_acs)
    avg_hh_acs = avg_hh_acs["B25010_001E"]
    
    table8 = pd.DataFrame({"TxSDC": ["Estimate", year, population_tdc, gq_tdc,
                                     hh_population_tdc, number_hh_tdc, avg_hh_tdc],
                           "Census": ["ACS", year, population_acs, gq_acs,
                                      hh_population_acs, number_hh_acs, avg_hh_acs]})
    table8 = table8.rename(index={0: " ", 1: " ", 2: "Total Population",
                                  3: "Group Quarters Population", 4: "Population in Households",
                                  5: "Number of Households", 6: "Average Household Size"})
    
    table8.name = "Table 8. Recent Estimates of Number of Households for " + county + " County"
    
    return table8
    
    
    
    

def main(fips, country):
    
    fips = "303"
    county = "Lubbock"
    
    figures = []
    
    data_TDC = pd.read_csv(p.table3_excel, sep=r'\,|\t', engine='python')
    
    table8 = make_table8(data_TDC, fips, county, "2014")
    
    figures.append(table8)
    
    return figures
    
    
if __name__ == "__main__":
    #execute only if run as a script
    main()