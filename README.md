# CTM Report

CTM Report is a Python library dedicated to creating Control Total Memos (CTM)
using data from the United States Census API.

This version focuses specifically on counties and group quarters within the state of Texas.

## Installation

**PLEASE NOTE:** This software was written using Python 3.7.3. Using earlier versions of Python may not yield the intended results.

**Python MUST be installed on your computer before attempting to CTM Report**

For simplicity's sake, it is recommended to simply download this package from the repository web page:
![Imgur](https://i.imgur.com/bNYb2aY.png)

## Usage

**NOTE:** Any interactions with this library should happen solely through **caller.py**. Otherwise, the other modules should only be touched if sources for data and/or API variables need to be changed.

**IF EXECUTING FROM THE CONSOLE:**

Run the following code from your console:
`python caller.py`

The program will prompt you to input a county:
`Enter county name:`

Valid inputs:
    - "Lubbock"
    - "Travis"
    - "Ector"
    
Invalid inputs:
    - "lubbock"
    - "TRAVIS"
    - "Ector County"
    - any FIPS code
    
If the county specified is found: the program will process the request, create the corresponding tables and graphs, and will say the following once finished:
`Done`


### Output

**NOTE:** Within the **CTM_Report** directory, there **must** be a subdirectory called **output**. This is where all plots and tables will be written to. In the event that the **output** subdirectory does not exist, **THE CODE WILL THROW AN ERROR.**

Within the **output** subdirectory will be the outputs for each county that is called with this program. Each county will have their own subdirectory that will delete itself and recreate itself (and all of its contents) if the user chooses to call upon that county again within **caller.py**. **NOTE:** In regards to the county subdirectories: Sometimes this program may throw an error that explains that the "directory may not exist". This is perfectly normal and can be fixed by running the program and calling that same county again.

The contents of each county subdirectory are as follows:

- **output.xlsx**: An Excel file that contains all DataFrames converted into tables.
- **img/**: Yet another subdirectory containing the plots.

#### Plots

As mentioned, all plots (graphs, charts, non-tables) will be exported to the **img/** subdirectory for the respective county. These plots have been converted to PNG files and may be uploaded/pasted accordingly to the CTM.

## Structure

Different parts of this program have been divided into modules based on relevance
and overlap in API variables used.

As of **11/06/2019**, the following modules are:

- **population_growth.py**
    - Figure 1. Population Growth in XXXX County 1970-2010
    - Table 1.  Population Percent Change for XXXX County and Texas, 1970-2010
    - Figure 2. Population Percent Change for XXXX County and Texas by Decade, 1970-2010
    - Table 2.  Historic Average Annual Compound Population Growth Rate by Decade for XXXX County and Texas
    
- **population_trends.py**
    - Table 3.  Comparison of Recent Population Estimates and Growth Rates for XXXX County, 2010-2012
    - Table 4.  Population projections and Percent Change for XXXX County
    - Figure 3. Population Projections for XXXX County through 2045

- **group_quarters.py**
    - Table 5. Recent Trends in Group Quarters Population for XXXX County
    - Table 6. Projected Group Quarters Population for XXXX County **(undeveloped --> data under development)**
    
- **historic_average_household.py**
    - Table 7.  Historical Householes and Average Household Sizes for XXXX County, 1980-2010
    - Figure 4. Trend in Average Household Size for XXXX County 1980-2010
      
- **household_esimates.py**
    - Table 8. Recent Estimates of Number of Households for XXXX County
    - Table 9. Forecasts of Number of Householdes and Average Household Size for XXXX County **(undeveloped)**
          
- **median_household_income.py**
    - Table 10. Median Household Income for XXX County and Texas 1970-2010
    - Figure 5. Historic Median Household for Income XXXX County 1970-2010 in Nominal and Constant Dollars
    - Table 11. ACS 2012 Estimated Median Household Income for XXXX County in 2012 Dollars
    - Table 12. Projected Median Household Income in Constant 2014 and Nominal Dollars for XXXX County **(undeveloped --> data under development)**
    - Figure 6. Future Trends in Median Household Income for XXXX County 2010-2045 **(undeveloped --> data under development)**
    - Table 13. Suggested Forecast Year Median Household Income in Constant 2014 Dollars **(undeveloped --> data under development)**
      
- **employment_trends.py**
    - Table 14. Historic Employment by Type for XXXX County 
    - Figure 7. Historic Employment by Type for XXXX County, 1990-2005
    - Table 15. Estimated 2014 Employment Control Totals for XXXX County
    - Table 16. Population to Employment Ration Trend for XXXX County Based on TWC Employment 1995-2010
    - Table 17. Recent Population to Employment Ratio Trend for XXXX County Based on TWC Employment 2010-2014 
    - Table 18. Recent Trends in Employment by Type in XXXX County, 2010-2014
    -  **Tables 19 and 20 cannot be programmed.**
    - Table 21. Example Estimating 2045 Employment Using Values within Control Total Ranges using the 0.5 Migration Scenario. **(undeveloped)**
      
       
It is **not** necessary to call each individual module when producing the CTM.
Such is the job of **caller.py**, which is the only module that the user
should interact with.

## Data Being Used

### API Reference

Most data is derived from the United States Census API. As of **10/25/2019**,
the API key being used in this project belongs to Emmanuelle Maher--the IDSER
work-study student currently developing this code.

The current API key may be replaced in **paths.py**. The designated variable is
`census_api_key`.

For your own API key, refer to: https://api.census.gov/data/key_signup.html

### Other Data

For data that is otherwise unavailable from the API (primarily data from TDC and data prior to 2000),
we rely on several Excel Spreadsheeets. The aforementioned spreadsheets are referenced
accordingly in paths.py.

As of **10/25/2019**, these Excel Files are not visible on the respository as I have
designated all files with extension **.xls** and **.xlsx** to be ignored. This is subject to change.

#### Excel Data Formatting

In order for pandas to properly work with Excel Spreadhseets, the data must be
formatted in a way so that pandas can readily handle and access the information
we need.

The following shows some "poor formatting practices" in relation to pandas
(from a dataset that this software uses):

![Imgur](https://imgur.com/p1cPawx.png)

If and when excel files are added/replaced in **paths.py**, please make sure that
it looks something like this:

![Imgur](https://imgur.com/0KcQO6e.png)

**NOTE:** If replacing files in **paths.py**, ensure that the column names in the datasets
remain the same (case-sensitive) OR to change the code within the relevant functions.

**Frankly speaking, it is not recommended that you do the latter.**

## License

**Copyright 2019 IDSER**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.