import os
import json
from constants import YEAR, Months, Districts
from scraping_service import get_district_fps_data

def main():
    for month_name, month_num in Months.items():
        # Formats month as 2-digit string (e.g., 3 -> "2026-03")
        folder_year_month = f"{YEAR}-{month_num:02d}"

        for district_name, district_code in Districts.items():
            # Formats district name (e.g., "North Goa" -> "north_goa")
            folder_district = district_name.lower().replace(" ", "_")

            # Construct path and create nested directories
            target_dir = os.path.join("data", "raw", folder_year_month, folder_district)
            os.makedirs(target_dir, exist_ok=True)

            print(f"--> Fetching all data for {district_name} ({month_name} {YEAR})...")
            
            # Fetch all FPS data for this district in one go
            district_data = get_district_fps_data(str(district_code), month_num, YEAR)
            print(f"    Fetched data for {len(district_data)} FPS shops.")

            # Save each shop's data to its respective file
            saved_count = 0
            for fps_id, data in district_data.items():
                file_path = os.path.join(target_dir, f"{fps_id}.json")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    # If it's valid JSON (dict), save properly formatted
                    if isinstance(data, dict) or isinstance(data, list):
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    else:
                        # If the server returned HTML text, save as a raw string
                        f.write(data)
                        
                saved_count += 1

            print(f"    Saved {saved_count} files to {target_dir}")

if __name__ == "__main__":
    main()