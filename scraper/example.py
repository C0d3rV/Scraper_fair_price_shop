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