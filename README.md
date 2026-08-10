# IMPDS FPS Data Scraper

A small Python scraper for collecting **Fair Price Shop (FPS) data** from the IMPDS portal and storing the raw responses in a structured folder format.

The main idea is pretty simple:

**State/District → FPS IDs → FPS data → JSON files**

The scraper goes through the required IMPDS endpoints, maintains the same session while making the requests, handles both JSON and HTML responses, and saves the collected data locally.

## What it does

For each month and district configured in the project, the scraper:

1. Opens the IMPDS page to establish a session.
2. Requests the FPS/district information.
3. Extracts the available FPS IDs.
4. Fetches the data for every FPS.
5. Tries to parse the response as JSON.
6. If the response isn't valid JSON, parses the HTML instead.
7. Saves each FPS response as a separate `.json` file.

The output is organized like this:

```text
data/
└── raw/
    ├── 2026-01/
    │   ├── district_1/
    │   │   ├── 12345.json
    │   │   ├── 12346.json
    │   │   └── ...
    │   └── district_2/
    │       └── ...
    ├── 2026-02/
    │   └── ...
    └── ...
```

This makes it easier to work with the raw data later instead of dumping everything into one huge file.

## Project Structure

```text
.
├── main.py
├── scraping_service.py
├── constants.py
├── data/
│   └── raw/
└── README.md
```

### `scraping_service.py`

Contains the actual scraping logic.

The main function is:

```python
get_district_fps_data(state_code, month, year)
```

It handles the session, requests, FPS ID extraction, and response parsing.

There is also:

```python
parse_html_to_json(html_text)
```

which is used when an endpoint returns HTML instead of proper JSON.

### `constants.py`

Contains the configuration used by the scraper, mainly:

* `YEAR`
* `Months`
* `Districts`

So the months and districts don't need to be hardcoded inside the scraping logic.

### `main.py`

This is the entry point.

It loops through all configured months and districts, calls the scraper, and writes the returned data to the appropriate directories.

## Requirements

Python 3.9+ should be enough.

Install the required packages:

```bash
pip install httpx beautifulsoup4 lxml
```

## Configuration

Before running the scraper, configure `constants.py`.

For example:

```python
YEAR = 2026

Months = {
    "January": 1,
    "February": 2,
    "March": 3
}

Districts = {
    "District Name": "district_code"
}
```

The scraper will use these values to decide what data to collect.

## Running the scraper

Run:

```bash
python main.py
```

The script will print its progress while it works:

```text
--> Fetching all data for District Name (January 2026)...
    Fetched data for 120 FPS shops.
    Saved 120 files to data/raw/2026-01/district_name
```

## Response Handling

The IMPDS endpoints don't always return data in exactly the same format.

The scraper therefore tries JSON first:

```python
r_fps.json()
```

If that fails, the response is passed to the HTML parser.

For HTML responses, tables are extracted and converted into dictionaries whenever headers are available.

If there are no tables, the scraper falls back to cleaned text:

```json
{
    "raw_data": "..."
}
```

So instead of immediately throwing away a response just because it isn't valid JSON, the scraper tries to preserve the useful data.

## Why the same session is used

The scraper intentionally keeps one `httpx.Client` open while processing a district.

The IMPDS server expects some state to be established through the earlier requests, so the flow is:

```text
Open session
    ↓
Open IMPDS page
    ↓
Request district/FPS information
    ↓
Extract FPS IDs
    ↓
Request each FPS using the same session
```

Using a new session for every request can break this flow, so the scraper keeps the connection/session alive for the complete district-level operation.

## Error Handling

There are a few basic safeguards in place:

* No FPS IDs → skip that district.
* Invalid JSON → try HTML parsing.
* Empty HTML response → return an error object.
* Unexpected scraping errors → print the district and continue.

The goal here is to make the scraper reasonably tolerant of the slightly messy responses that can come back from the portal.

## Output

Each FPS gets its own JSON file:

```text
data/raw/2026-03/district_name/12345.json
```

The filename is the FPS ID, so the source of each file is easy to identify.

The raw data is intentionally kept separate from the scraping code. This also means any later cleaning, transformation, analysis, or database loading can be done as a separate step.

## Tech Used

* **Python**
* **HTTPX** for HTTP requests
* **BeautifulSoup** for HTML parsing
* **lxml** as the HTML parser
* **Regex** for extracting FPS IDs
* **JSON** for storing the collected data

## Notes

This project is focused on **data collection**, not data analysis.

The files inside `data/raw/` should be treated as raw scraped data. Any cleaning or transformation can be performed in a separate pipeline so that the original responses remain available if something needs to be checked later.
