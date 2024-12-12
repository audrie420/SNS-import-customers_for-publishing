# group 2 - past import db handlers

import pandas as pd
import json
from pprint import pprint as pp


def validation_loop(incoming_headers: list, header_mapping: dict, key: str):
    print(f"\nSelect header for key '{key}':")
    print("Available headers:", incoming_headers)
    selected_header = input("Enter header name (or press Enter to skip): ").strip()
    print("=============================================")
    if selected_header in incoming_headers:
        header_mapping[key] = selected_header
        incoming_headers.remove(selected_header)
    elif selected_header == "":
        header_mapping[key] = None
        print(f"No header allocated for key '{key}'")
    else:
        print("Invalid header name. Please select from the available headers.")
        validation_loop(incoming_headers, header_mapping, key)


def select_headers(incoming_headers: list, dict: dict):
    header_mapping = {}
    print("Select headers for each key (press Enter to skip a key)")
    for key in dict:
        if not key.endswith(("_TS", "_UPD", "_INS")):
            validation_loop(incoming_headers, header_mapping, key)
    return header_mapping


def build_header_dict(
    past_csv_df: pd.DataFrame,
    incoming_csv_df: pd.DataFrame,
    customise=True,
):
    if customise:
        # Get headers from past imports df
        header_arr = past_csv_df.columns.tolist()
        header_dict = {key: None for key in header_arr}

        # Get headers from incoming df
        incoming_headers = incoming_csv_df.columns.tolist()

        header_mapping = select_headers(incoming_headers, header_dict)
        return header_mapping

    else:
        header_mapping = {
            "AVID": "Cust #",
            "AVID_INS": None,
            "AVID_TS": None,
            "AVID_UPD": None,
            "City": "City",
            "City_INS": None,
            "City_TS": None,
            "City_UPD": None,
            "Email": "Email",
            "EmailContPref": "Yes No SNS Email",
            "EmailContPref_INS": None,
            "EmailContPref_TS": None,
            "EmailContPref_UPD": None,
            "Email_INS": None,
            "Email_TS": None,
            "Email_UPD": None,
            "FirstName": "First Name",
            "FirstName_INS": None,
            "FirstName_TS": None,
            "FirstName_UPD": None,
            "LastName": "Last Name",
            "LastName_INS": None,
            "LastName_TS": None,
            "LastName_UPD": None,
            "Phone": "Phone",
            "Phone_INS": None,
            "Phone_TS": None,
            "Phone_UPD": None,
            "PostalCode": "Postal Code",
            "PostalCode_INS": None,
            "PostalCode_TS": None,
            "PostalCode_UPD": None,
            "Province": "Province",
            "Province_INS": None,
            "Province_TS": None,
            "Province_UPD": None,
            "Street": "Street",
            "Street_INS": None,
            "Street_TS": None,
            "Street_UPD": None,
            "Country": "Order Country",
            "Country_INS": None,
            "Country_TS": None,
            "Country_UPD": None,
        }
        return header_mapping

    # pp("Header mapping:", header_mapping)

    # use this if you want to persist the dictionary by saving in json format
    # with open('my_dict.json', 'w') as f:
    #     json.dump(my_dict, f)


if __name__ == "__main__":
    print("test time")
    past_imports = pd.read_csv("test_csv_past.csv")
    incoming_imports = pd.read_csv("test_csv_incoming.csv")
    pp(build_header_dict(past_imports, incoming_imports, True))
