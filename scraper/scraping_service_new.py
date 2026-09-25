# ------ imports ----- 
import re
import json
import os
import httpx
from datetime import datetime
from bs4 import BeautifulSoup
from constants import START_YEAR, MONTHS
# ---------------------


# Let's create a function to get active states and their respective codes for a month and year input

def get_state_codes(year: int, month: int) -> dict:
    """
    This function returns all the active state codes in the form of a dict for an input month and year.
    The output dict is of the format {state_code(string): (state_code(int), state_name),...}. 
    
    """
    state_req_count = 0

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
            state_req_count += 1

            # Pulling the response for live states 
            res = client.get('https://impds.nic.in/sale/liveStatesAjax')
            state_req_count += 1

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
    The output dict is of the format {district_code(string): district_name,...}. 
    """

    dist_req_count = 0

    header = {
                "referer": f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                "x-requested-with": 'XMLHttpRequest'}

    try:
        with httpx.Client(headers = header, timeout = 30) as client:
            # Establish connection to the server
            print(":D Trying to establish connection...")
            client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')
            dist_req_count += 1
        
    
            # Pulling the response for live states 
            res = client.get(f'https://impds.nic.in/sale/stateByCountryAjax?stateCode={state_code}')
            if res.status_code == 200:
                  print("✓ connection established! ")
            dist_req_count +=1
    
            # Filtering out the required data (state code and their respective names)
            print("Finding the required data.")
            data = re.findall(r"aria-label\=\"(.*?)\" onclick=\"stateData\('(\d+)'", res.text)
            if data:
                  print("data retrieved\n")
    
            # now the output dict
            output = {item[1]: (item[0]) for item in data}
    except Exception as e:
                print("error returnig the vbalues")
    return output
    


# Now let's make a function to store our phase 1 parameters: year, month, state code, district code
def save_params(year, month):
      """
      This function will call upon the get_state_codes and get_district_codes.
      The output will be a dict containing all the phase 1 params.
      The output will be stored in a single constants file.
      """

      # We need to only loop through till the current month
      # because we can't have future data
      date = datetime.now()
      current_year = date.year
      current_month = date.month

      state_count = 0
      district_count = 0

      req_sent = 0

      start_year = year
      master_data = {}

      for y in range(start_year, current_year + 1):
            master_data[y] = []

            actual_start_month = month if y == start_year else 1
            actual_max_month = current_month if y == current_year else 12

            for m in range(actual_start_month, actual_max_month + 1):
                  print(f'scraping state codes for year {y} and month {m}...')
                  
                  state_codes = get_state_codes(y, m)
                  state_count += len(state_codes)

                  # Let's make a temporary stoppage point for the state codes.
                  # This will help avoid another nested for loop

                  # Now we cooking
                  # We'll just go for district codes now

                  for state in state_codes:
                        district_codes = get_district_codes(y, m,  int(state))
                        district_count += len(district_codes)
                        req_sent += 1

                        for dist in district_codes:
                              row = {
                                    "Month" :  m,
                                    "state_code" : state,
                                    "state_name" : state_codes[state],
                                    "district_code" : dist,
                                    "district_name" : district_codes[dist]
                                    }
                              master_data[y].append(row)

      with open('district_codes.json', 'w', encoding = 'utf-8') as file:
            json.dump(master_data, file, indent = 4)
      print(f'Finshed scraping codes for {state_count} instances of states and {district_count} instances of districts.')
      print(f'Requests sent = {req_sent}')

      return "Success"


save_params(START_YEAR, month = 1)




            





    
        



