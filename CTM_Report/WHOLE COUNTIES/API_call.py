# -*- coding: utf-8 -*-
"""
Name: API_call.py

PURPOSE OF PROGRAM:
    Make call to the US Census Bureau API and check to see if request is
    successful.
    
Created on Mon Sep 23 10:14:09 2019

@author: slq584
"""
import paths as p
import requests

"""
api_request() PURPOSE:
    Check to see if call to API is successful.
"""
def api_request(census_api_url):
    #Header for API Call
    headers = {'Content-Type': 'applicatoin/json',
           'Authorization': 'Bearer {0}'.format(p.census_api_key)}
    #Make request to the API
    response = requests.get(census_api_url, headers=headers)
    
    if response.status_code == 200:
        #print('Request to API successful')
        return response.text;
    elif response.status_code == 404:
        print('Not Found.')
        return None;
    else:   #Any other status code will be printed
        print('API status code: ', response.status_code)