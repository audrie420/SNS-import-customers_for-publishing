# group 2 - past import db handlers

# For each incoming record,
# 	Check if their customer number exists in our database
# If no, for all fields, IMPORT DATA + FLAG UPDATE + UPDATE TIMESTAMP

import pandas as pd

# imports for testing
from pprint import pprint as pp
import build_header_dict as bhd


def new_df_entry(past_imports_df, incoming_df):
    common_columns = past_imports_df.columns.intersection(incoming_df.columns)
    # Create a new row with desired values
    new_row = {
        col: incoming_df[col].iloc[0] if col in common_columns else None
        for col in past_imports_df.columns
    }
    new_row_df = pd.DataFrame([new_row])
    # Append the new row to pastdf
    past_imports_df = pd.concat([past_imports_df, new_row_df], ignore_index=True)
    # the line below is usable as a replacement for line above if you remove line 18
    # past_imports_df = past_imports_df._append(new_row, ignore_index=True)

    return past_imports_df


# def import_new_record(header_dict, past_imports, incoming_import, AVID):

#     search_header = header_dict["AVID"]
#     search_res = incoming_import[incoming_import[search_header] == AVID]
#     search_res_copy = search_res.copy()
#     inverted_header_dict = {v: k for k, v in header_dict.items()}
#     search_res_copy.rename(columns=inverted_header_dict, inplace=True)
#     combined_df = pd.concat([past_imports, search_res_copy])
#     return combined_df


def import_1_new_record(header_dict, past_imports, incoming_import, AVID):
    search_header = header_dict["AVID"]
    search_res = incoming_import[incoming_import[search_header] == AVID]
    search_res_copy = search_res.copy()
    inverted_header_dict = {v: k for k, v in header_dict.items()}
    search_res_copy.rename(columns=inverted_header_dict, inplace=True)
    updated_df = new_df_entry(past_imports, search_res_copy)

    return updated_df


# if __name__ == "__main__":
#     print("I prefer to be a module, but I can do some tests for you.")
#     past_imports = pd.read_csv("0000past_imports.csv")
#     incoming_import = pd.read_csv("test_cust_rec_import.csv")

#     AVID = 135705
#     header_dict = bhd.build_header_dict(past_imports, incoming_import, False)
#     res = import_1_new_record(header_dict, past_imports, incoming_import, AVID)
#     pp(res)
