# ------ imports ----- 
import re
import json
import os
import httpx
from bs4 import BeautifulSoup
from constants import YEARS, MONTHS
# ---------------------


# Let's create a function to get active states and their respective codes for a month and year input

def get_state_codes(year: int, month: int) -> dict:
    """
    This function returns all the active state codes in the form of a dict for an input month and year.
    The output dict is of the format {state_code(string): (state_code(int), state_name),...}. 
    
    """

    header = {
                'referer': f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                "x-requested-with": 'XMLHttpRequest'}
    
    try:
        with httpx.Client(headers = header, timeout = 30) as client:
            # Establish connection to the server
            client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')

            # Pulling the response for live states 
            res = client.get('https://impds.nic.in/sale/liveStatesAjax')
            print(res.status_code)

            # Filtering out the required data (state code and their respective names)
            data = re.findall(r"stateData\('(\d+)'\)\"\>(.*?)\<", res.text)

            # now the output dict
            output = {item[0]: item[1] for item in data}
    except Exception as e:
            print("error returnig the vbalues")
    return output



def get_district_codes(year: int, month: int, state_code: int):
    """
    This function returns all the active district codes in the form of a dict for an input month and year.
    The output dict is of the format {district_code(string): (state_code(int), district_code(int), district_name),...}. 
    """

    header = {
                "referer": f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                "x-requested-with": 'XMLHttpRequest'}

    try:
        with httpx.Client(headers = header, timeout = 30) as client:
            # Establish connection to the server
            print("Trying to establish connection...")
            client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')
        
    
            # Pulling the response for live states 
            res = client.get(f'https://impds.nic.in/sale/stateByCountryAjax?stateCode={state_code}')
            if res.status_code == 200:
                  print("connection established!")
    
            # Filtering out the required data (state code and their respective names)
            print("Finding the required data.")
            data = re.findall(r"aria-label\=\"(.*?)\" onclick=\"stateData\('(\d+)'", res.text)
            if data:
                  print("data retrieved")
    
            # now the output dict
            output = {item[1]: (state_code, int(item[1]), item[0]) for item in data}
    except Exception as e:
                print("error returnig the vbalues")
    return output
    


# let's first run it for state codes. we'll write the stae code data to a file, then we'll do that for districts as well. 
# eventually, we'll change them tofunctions to retreive state and ist codes and compare them against our constants if tehy already exist.
# basically a eference dict so that we do not keep the state codes in memory all the time while execution.

master_data = {}
for year in YEARS:
    master_data[year] = {}
    for month in MONTHS:
            data = get_state_codes(year, month)
            print("data retreived")

            master_data[year][month] = data

            with open('constants1.py', 'w', encoding = 'utf-8') as file:
                  print("dumping json to file")
                  json.dump(master_data, file, indent = 4)


            print("state_codes added succesfully")
    
        



