import httpx
import json
import re

def get_district_fps_data(state_code: str, month: int, year: int) -> dict:
    """
    Fetches all FPS data for a given district code in a single session.
    
    Returns:
        dict: A dictionary mapping FPS IDs to their response text/data.
    """
    header = {
        'referer': f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}',
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "x-requested-with": 'XMLHttpRequest'
    }

    all_fps_data = {}

    try:
        # Using a 'with' block keeps the SAME session open for all requests
        with httpx.Client(headers=header, timeout=30) as client:
            
            # Step 1: Establish session
            client.get(f'https://impds.nic.in/sale/stateUnautmated?month={month}&year={year}')
            
            # Step 2: Hit district endpoint (Server requires this to set internal state)
            r_dist = client.get(f'https://impds.nic.in/sale/districtByCountryAjax?stateCode={state_code}')
            
            # Extract FPS IDs using regex
            fps_ids = re.findall(r'"FPSName":\s*"(\d+)"', r_dist.text)
            
            if not fps_ids:
                print(f"No FPS IDs found for district {state_code}.")
                return all_fps_data

            # Step 3: Fetch data for each FPS ID using the established session
            for fps_id in fps_ids:
                r_fps = client.get('https://impds.nic.in/sale/fpsByCountryAjax', params={'stateCode': fps_id})
                
                # Fallback handler: NIC sites sometimes return malformed JSON or HTML snippets.
                # We will try to parse it as JSON, and fallback to plain text if it fails.
                try:
                    all_fps_data[fps_id] = r_fps.json()
                except json.JSONDecodeError:
                    all_fps_data[fps_id] = r_fps.text 
                    
    except Exception as e:
        print(f"Error during scraping session for district {state_code}: {e}")

    return all_fps_data