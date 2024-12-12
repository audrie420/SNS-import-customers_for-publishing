# WIP

from data_cleaning_folder.clean_name_isolated import correct_name
from data_cleaning_folder.clean_address_isolated import format_street_address
from data_cleaning_folder.compare_name import name_is_similar
from data_cleaning_folder.compare_phone import phone_is_similar
from data_cleaning_folder.compare_address import address_entry_is_similar
from data_cleaning_folder.format_province import format_province_to_iso
# the unused imports are here so that you can call them through this .py
from thefuzz import fuzz
from thefuzz import process
import re
import pandas as pd

# for testing purposes
# import cust_API_requests
from pprint import pprint as pp


# returns None if fed float('nan')
def format_phone_number(number: str | float):
    # rule out NaN values
    if pd.isna(number):
        return None

    # turn all delimiters into dashes
    number = re.sub(r"[+() ,.]", "-", number)

    # remove leading and trailing dashes
    number = number.strip("-")

    # remove double dashes
    while "--" in number:
        number = number.replace("--", "-")

    # Handle extensions ### but extensions can appear in many ways
    ext_match = re.search(r"(ext|x)\s*(\d+)", number, re.IGNORECASE)
    extension = ""
    if ext_match:
        extension = f" x {ext_match.group(2)}"
        number = number[: ext_match.start()]

    # Remove all non-digit characters except for '-'
    number = re.sub(r"[^\d-]", "", number)

    # Local, non-long distance numbers (902, 782)
    if re.match(r"^(902|782)\d{7}$", number):
        formatted = f"{number[:3]}-{number[3:6]}-{number[6:]}"

    # Long distance North American numbers
    elif re.match(r"^[2-9]\d{9}$", number):
        formatted = f"1-{number[:3]}-{number[3:6]}-{number[6:]}"

    elif re.match(r"^1[2-9]\d{9}$", number):
        formatted = f"1-{number[1:4]}-{number[4:7]}-{number[7:]}"

    # International phone numbers or numbers that cannt be identified
    else:
        formatted = number

    # remove double dashes
    while "--" in formatted:
        formatted = formatted.replace("--", "-")

    return formatted + extension


# this is for data that will be posted as a new customer
# handles NaN values - returns None for each field with Nan value
def clean_cust_body_in_isolation(post_body):
    post_body["lastName"] = correct_name(post_body["lastName"])
    post_body["firstName"] = correct_name(post_body["firstName"])
    post_body["phone"] = format_phone_number(post_body["phone"])
    if pd.isna(post_body["attribute_AudienceView ID"]):
        post_body["attribute_AudienceView ID"] = None
    if pd.isna(post_body["email"]):
        post_body["email"] = None
    return post_body


if __name__ == "__main__":
    raw_province = "Nova"

    # cust_rec = {
    #     "attribute_AudienceView ID": float("nan"),
    #     "lastName": float("nan"),
    #     "firstName": float("nan"),
    #     "phone": float("nan"),
    #     "email": float("nan"),
    # }
    # pp(cust_rec)
    # cleaned = clean_cust_body_in_isolation(cust_rec)
    # pp(cleaned)
