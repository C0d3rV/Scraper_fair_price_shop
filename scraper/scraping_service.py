import httpx
import json
import re
from bs4 import BeautifulSoup

def parse_html_to_json(html_text: str):
    """
    Parses an HTML string, extracts tables, and converts them into a list of dictionaries.
    Falls back to basic text extraction if no tables are found.
    """
    soup = BeautifulSoup(html_text, 'lxml')
    tables = soup.find_all('table')
    
    # If no tables are found, return a dictionary with the raw cleaned text
    if not tables:
        clean_text = soup.get_text(separator=" ", strip=True)
        return {"raw_data": clean_text} if clean_text else {"error": "Empty response"}

    extracted_data = []
    
    for table in tables:
        # Extract headers (th)
        headers = [th.text.strip() for th in table.find_all(['th'])]
        table_data = []
        
        # Extract rows (tr) and cells (td)
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue
                
            row_data = [cell.text.strip() for cell in cells]
            
            # If headers exist and match the cell count, map them to a dictionary
            if headers and len(headers) == len(row_data):
                table_data.append(dict(zip(headers, row_data)))
            else:
                table_data.append(row_data)
                
        if table_data:
            extracted_data.extend(table_data)

    # Return as a single list if it's one table, or a dictionary wrapper
    return extracted_data


def get_district_fps_data(state_code: str, month: int, year: int) -> dict:
    """
    Fetches all FPS data for a given district code in a single session.
    
    Returns:
        dict: A dictionary mapping FPS IDs to their parsed response data (JSON/Dict).
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
                
                # Try JSON first. If it's malformed or returns HTML, pass it to the parser.
                try:
                    all_fps_data[fps_id] = r_fps.json()
                except json.JSONDecodeError:
                    all_fps_data[fps_id] = parse_html_to_json(r_fps.text)
                    
    except Exception as e:
        print(f"Error during scraping session for district {state_code}: {e}")

    return all_fps_data