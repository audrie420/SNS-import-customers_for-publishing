# group 3 - flag resolving and calling API funcs

import pandas as pd
from build_header_dict import build_header_dict
from pprint import pprint as pp
from datetime import datetime
from check_against_past_imports import (
    check_against_past_imports,
)  # yes i checked and its fine that you only import the func you use even if it relies on other funcs you didnt import
from resolve_update_flags import resolve_update_flags as ruf
import keys as k  # to access client_name


# read files into dataframes
past_filename = input("Enter relative file path of past imports csv:")
past_imports = pd.read_csv(past_filename)

incoming_filename = input("Enter relative file path of incoming import csv:")
incoming_import = pd.read_csv(incoming_filename)

# timestamp incoming import
INCOMING_TIMESTAMP = None
manual_timestamp = input(
    "Would you like to manually input the timestamp of this import? If not, the current date and time will be used instead. y/n:"
)
if manual_timestamp == "y":
    INCOMING_TIMESTAMP = float(
        input(
            "Enter the date and time of the import data (cannot be exact same as another import) as a decimal number in the format YYYYMMDD.hhmm:"
        )
    )
else:
    INCOMING_TIMESTAMP = float(datetime.now().strftime("%Y%m%d.%H%M"))


# initialise the header dictionary
header_dict_customise = input(
    ("Would you like to customize the header dictionary? y/n: ")
)
HEADER_DICT = build_header_dict(
    past_imports, incoming_import, (header_dict_customise == "y")
)
if not (header_dict_customise == "y"):
    pp("Initialized header dictionary to default one.")


# checks against past imports, sets flags, writes new entries into database of past imports
pp("Checking against past imports...")
checked_past_imports_filename = check_against_past_imports(
    past_imports, incoming_import, INCOMING_TIMESTAMP, HEADER_DICT
)
actions_to_take_filename = checked_past_imports_filename
print(
    f"Done checking against past imports. Actions_to_take file has been generated. It is {actions_to_take_filename}"
)


# move old past imports file to archive
# if os.path.exists(past_filename):
#     os.remove(past_filename)
#     print(f"The old past imports file {past_filename} has been deleted.")

# now start resolving flags
# resolves update flags, updates timestamps where relevant, raises some inspect flags
# load up dataframe of new CSV
print("Starting to resolve flags...")
actions_to_take_df = pd.read_csv(actions_to_take_filename)
actions_to_take_df = ruf(
    actions_to_take_df, k.client_name, INCOMING_TIMESTAMP, HEADER_DICT
)
print("=================resolved update flags===============")

# output new csv file containing past imports
filename = f"{INCOMING_TIMESTAMP}_past_imports.csv"
actions_to_take_df.to_csv(filename, index=False)
print("new past imports file generated:", filename)


# put up a message to prompt user to manually inspect those flagged for inspection
