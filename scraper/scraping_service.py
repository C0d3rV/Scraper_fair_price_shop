import httpx
import os
import requests
import json
import re


def get_fps_id(state_code: str, month: int, year: int) -> list:
    """
    Get FPS IDs for a given state code/district code.
    The source website use state_code param for both state and district codes, so we can use the same function for both. 

    Args:
        state_code (str): The state code for which to retrieve FPS IDs.
        month (int): The month for which to retrieve FPS IDs.
        year (int): The year for which to retrieve FPS IDs.

    Returns:
        list: A list of FPS IDs for the given state code.
    """
    # Implementation for retrieving FPS IDs

    header = {
    'referer': f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    "x-requested-with": 'XMLHttpRequest'
     }

    try:
        client = httpx.Client(headers=header, timeout=30)

    except Exception as e:
        print(f"Error creating HTTP client: {e}")
        return []

    # Step 1: establish session
    client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')

    # Step 2: get district data (contains FPS IDs in the embedded chart script)
    try:
        r = client.get(f'https://impds.nic.in/sale/districtByCountryAjax?stateCode={state_code}')
    except Exception as e:
        print(f"Invalid district code {state_code}: {e}")
        return []

    # Step 3: extract FPS IDs from the response text using regex
    fps_ids = re.findall(r'"FPSName":\s*"(\d+)"', r.text)
    return fps_ids


def get_fps_data(fps_id: str, month: int, year: int) -> dict:
    """
    Get FPS data for a given FPS ID.

    Args:
        fps_id (str): The FPS ID for which to retrieve data.
        month (int): The month for which to retrieve data.
        year (int): The year for which to retrieve data.

    Returns:
        dict: A dictionary containing the FPS data.
    """
    # Implementation for retrieving FPS data

    header = {
    'referer': f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    "x-requested-with": 'XMLHttpRequest'
     }

    try:
        client = httpx.Client(headers=header, timeout=30)
    except Exception as e:
        print(f"Error creating HTTP client: {e}")
        return {}

    # Step 1: establish session
    client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')

    # Step 2: get FPS data
    try:
        r = client.get('https://impds.nic.in/sale/fpsByCountryAjax', params={'stateCode': fps_id})
    except Exception as e:
        print(f"Error fetching FPS data for ID {fps_id}: {e}")
        return {}

    # Step 3: parse the response JSON and return the data
    return r.json()