# ------ imports ----- 
import re
import json
import os
import httpx
from bs4 import BeautifulSoup
from constants import YEARS, MONTHS
# ---------------------


# Let's create a function to get active states and their respective codes for a month and year input

def get_state_codes(year: int, month: int) -> list:
    """
    This function returns all the active state codes in the form of a list
    """

    header = {
            'referer': f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            "x-requested-with": 'XMLHttpRequest'
        }

    state_codes = {}
    return 0

    # Now we establish client


# let's first try without the function

for year in YEARS:
    for month in MONTHS:
        header = {
                    'referer': f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    "x-requested-with": 'XMLHttpRequest'
                }

        try:
            with httpx.Client(headers = header, timeout = 60) as client:
                client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')

                res = client.get('https://impds.nic.in/sale/liveStatesAjax')

                #res = client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')
                print(res.status_code)

                print(re.findall(r"stateData\('(\d+)'\)\"\>(.*?)\<", res.text))


                # with open(f'{month}_{year}.txt', 'w', encoding = 'utf-8') as file:
                #      file.write(res.text)
        except Exception as e:
                print("error returnig the vbalues")



