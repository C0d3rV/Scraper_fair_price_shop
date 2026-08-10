from scraping_service import get_fps_data, get_fps_ids
from constants import STATE, Districts, Months, YEAR
import os

state_code = STATE["Goa"]
dist1 = Districts["North Goa"]
dist2 = Districts["South Goa"]
month = Months["March"]
year = YEAR

if __name__ == "__main__":
    fps_ids = get_fps_ids(state_code, month, year)

    path = os.path.getcwd()

    path_raw = os.path.join(path, "data/raw")
    