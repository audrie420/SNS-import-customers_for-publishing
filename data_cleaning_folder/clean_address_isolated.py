import re
import pandas as pd

# for testing block
from pprint import pprint as pp

# Define a list of common abbreviations and their expansions
abbreviations = {
    "Avenue": "Ave",
    "Boulevard": "Blvd",
    "Centre": "Ctr",
    "Circle": "Cir",
    "Court": "Crt",
    "Crescent": "Cres",
    "Drive": "Dr",
    "Esplanade": "Espl",
    "Freeway": "Fwy",
    "Gardens": "Gdns",
    "Grounds": "Grnds",
    "Heights": "Hts",
    "Highway": "Hwy",
    "Lookout": "Lkout",
    "Mountain": "Mtn",
    "Orchard": "Orch",
    "Parkway": "Pky",
    "Place": "Pl",
    "Plateau": "Plat",
    "Point": "Pt",
    "Private": "Pvt",
    "Promenade": "Prom",
    "Road": "Rd",
    "Route": "Rte",
    "Square": "Sq",
    "Street": "St",
    "Terrace": "Terr",
}

change_indicators = ["apt", "apartment", "suite", "unit", "condo"]
# consider adding "#"?
# cant because there's highway #{num} and RR#{num}
# and transform_string() expects a space between change_indicators[] and num

names_for_no_address = ["placeholder"]  # redacted for confidentiality

sequences_for_no_address = [
    "no info given",
    "no address given",
    "no info",
    "do not merge",
    "do not exchange",
    "contest winner",
    "seaside fm winner",
    "music director",
    "member of parliament",
    "invest nova scotia winner",
    "sns musician",
    "do not mail",
    "ticket face",
] + [f"per {name}" for name in names_for_no_address]


def transform_string(raw_string, change_indicators):
    # Patterns for transformations
    pattern1 = re.compile(
        r"^(\d+)\s(.*)\s(" + "|".join(change_indicators) + r")[\s-]*(\d*)$",
        re.IGNORECASE | re.DOTALL,
    )

    pattern2 = re.compile(
        r"^(\d+)\s(.*)\s(" + "|".join(change_indicators) + r")[\s-]*([A-Z]{1,2})$",
        re.IGNORECASE | re.DOTALL,
    )

    # Check for the first pattern
    match1 = pattern1.search(raw_string)
    if match1:
        numeric_digits_start = match1.group(1)
        middle_part = match1.group(2)
        numeric_digits_end = match1.group(4)
        return f"{numeric_digits_end}-{numeric_digits_start} {middle_part}"

    # Check for the second pattern
    match2 = pattern2.search(raw_string)
    if match2:
        numeric_digits_start = match2.group(1)
        middle_part = match2.group(2)
        alpha_end = match2.group(4)
        return f"{alpha_end}-{numeric_digits_start} {middle_part}"

    # Return the original string if no pattern matches
    return raw_string


def replace_abbreviations(raw_string, abbreviations):
    # Split the input string into lines
    lines = raw_string.splitlines()

    # Process each line
    updated_lines = []
    for line in lines:
        # Check each unabbreviated word in the dictionary
        for unabbrev, abbrev in abbreviations.items():
            # Check if the line ends with the unabbreviated word
            if line.endswith(f" {unabbrev}"):
                # Replace the unabbreviated word with the abbreviated word
                line = line[: -len(unabbrev)] + abbrev
                break  # Assuming only one replacement needed per line
        updated_lines.append(line)

    # Join the processed lines back into a single string
    return "\n".join(updated_lines)


# returns empty dict if no address is put in, or if input address contains sequences that signal invalid address (eg "sns per kayleigh")
def format_street_address(raw) -> dict:

    if (not raw) or pd.isna(raw):
        return {}

    if any(seq.lower() in raw.lower() for seq in sequences_for_no_address):
        return {}

    if raw.lower() == "na" or not raw:
        return {}

    string = raw.replace("—", "-").replace("–", "-")  # em and en dash to hyphen
    string = (
        string.replace(".", "").replace("'", "").replace("’", "")
    )  # remove periods and apostrophes and the weird apostrophes
    string = re.sub(r" ?- ?", "-", string)  # remove spaces around dashes
    string = transform_string(
        string, change_indicators
    )  # move unit number or letter to front
    string = replace_abbreviations(string, abbreviations)
    # remove leading and trailing spaces on each line
    string = "\n".join(line.strip() for line in string.splitlines())
    # remove leading and trailing whitespaces for whole string
    string = string.strip()
    # titlecase - any letter that follows a whitespace character (or apostrophe but those were removed) is capitalised
    string = re.sub(r"\b\w", lambda m: m.group().upper(), string)

    # fit lines into dictonary
    formatted_street_address = {
        "line1": "",
        "line2": "",
        "line3": "",
        "line4": "",
        "line5": "",
        "whole_address": string,
    }
    # Split the string into lines
    lines = string.split("\n")

    # Populate the dictionary with the lines
    for i in range(5):
        if i < len(lines):
            formatted_street_address[f"line{i+1}"] = lines[i]

    return formatted_street_address


if __name__ == "__main__":
    test_input = [
        "532 Bland Street\nApt. 5",
        "79 Larry Boulevard.\nApt. 97",
        "PO Box 42069",
        "per sns no info given",
        "no info",
        "123-456 Star Drive",
        "",
        "Please Do Not Mail",
        "Testing/proofing ticket face",
    ]
    for raw in test_input:
        output = format_street_address(raw)
        pp(output)
        print("==================")
