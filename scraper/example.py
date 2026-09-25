# First way

{
    'YEAR': {
        'month': (state_code, district_code)
    }
}


# Second way
{
    "year" : year,
    "month" : month,
    "state_code" : state_name,
    "district_code": district_name
}


# Third way
{
    'YEAR': (month, state_code, district_code)
}

  # In this method we keep sepearte dictionaries for the respective names of states and districts for their codes

states = {
    'state_code': state_name
}

district = {
    'district_code' : district_name
}



# Fourth way




===================================================
        PHASE 1: PARALLEL DISCOVERY (Async)
===================================================
[Year 2024 client1] ─┐
[Year 2025 client2] ─┼─> Scrape Active States -> Scrape Active Districts
[Year 2026 client3] ─┘
         │
         ▼
[ SAVE TO: district_master_list.json ]
(Close all Phase 1 clients)

===================================================
        PHASE 2: DEEP EXTRACTION (Iterative)
===================================================
Load 'district_master_list.json'
         │
         ▼
[ OPEN NEW CLIENT: FPS WORKER ]
For each District in Master List:
   ├─ Fetch FPS ID 1 ─> Fetch the respective data -> Save to DB/JSON
   ├─ Fetch FPS ID 2 ─> Fetch the respective data -> Save to DB/JSON
   └─ (Repeat until district is exhausted)




# district codes

{
       "Year" : 2020,
       "Month" : '2',
       "30": 'GOA',
       "756": 'NORTH GOA'
}