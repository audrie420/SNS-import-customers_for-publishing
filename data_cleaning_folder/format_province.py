from thefuzz import fuzz
from thefuzz import process
import pandas as pd


# for testing purposes
# import cust_API_requests
from pprint import pprint as pp


# returns the ISO code of relevant province. returns None if there is no clear match
# tolerates NaN values
def format_province_to_iso(raw_input: str) -> str:

    # if its just one letter or a number, or its a NaN value, throw it out
    if str(raw_input).isdigit() or len(str(raw_input)) <= 1 or pd.isna(raw_input):
        return None

    provinces = {
        "Alberta": "AB",
        "British Columbia": "BC",
        "Manitoba": "MB",
        "New Brunswick": "NB",
        "Newfoundland and Labrador": "NL",
        "Nova Scotia": "NS",
        "Ontario": "ON",
        "Prince Edward Island": "PE",
        "Quebec": "QC",
        "Saskatchewan": "SK",
        "Northwest Territories": "NT",
        "Nunavut": "NU",
        "Yukon": "YT",
    }

    # return ISO if raw input is CA-(iso code)
    for iso in provinces.values():
        if raw_input.upper() == "CA-" + iso:
            return iso

    # remove punctuation (for case N.S. or N.B.) and spaces (for case N. S.)
    raw_input = raw_input.replace(".", "")
    raw_input = raw_input.replace(" ", "")

    # match on "nova", "scotia", "nouvelle-ecosse" before matching on full name of province
    partials = ["nova", "scotia", "nouvelle-ecosse"]
    for partial in partials:
        if fuzz.ratio(raw_input.lower(), partial) >= 93:
            return "NS"

    # match on full name of province
    best_match, score = process.extractOne(
        raw_input, provinces.keys(), scorer=fuzz.ratio
    )
    if score >= 82:
        return provinces[best_match]

    # match on province ISO code
    best_match, score = process.extractOne(
        raw_input, provinces.values(), scorer=fuzz.ratio
    )
    if score >= 80:
        return best_match

    # no match, return None
    return None


if __name__ == "__main__":
    raw_province = "Nova Scotia"
    pp(format_province_to_iso(raw_province))
