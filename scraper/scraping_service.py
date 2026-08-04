import httpx
import os
import requests


r = 'https://impds.nic.in/sale/districtByCountryAjax?stateCode=585'
response = httpx.get(r)
print(response.json)