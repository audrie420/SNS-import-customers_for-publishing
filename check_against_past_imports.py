# group 2 - past import db handlers

import pandas as pd
from datetime import datetime
import import_new_record as inr
from find_dict_key import find_dict_key
import flags_n_stamps as fns

# imports for test block only
from build_header_dict import build_header_dict
from pprint import pprint as pp

# so im pretty sure the update, inspect and timestamp functions modify the dataframe in place
# but if not, return a modified function


# checks against past imports, sets flags, writes new entries into database of past imports
def check_against_past_imports(
    past_imports_df, incoming_import_df, incoming_timestamp, header_dict
):
    p_df = past_imports_df
    i_df = incoming_import_df
    __df_headers_no_flags = [key for key in header_dict.keys() if "_" not in key]
    # check if record ID in incoming_import is present in past_imports
    for AV_ID in i_df[header_dict["AVID"]]:
        if AV_ID in p_df["AVID"].values:
            for incoming_header_name in header_dict.values():
                if incoming_header_name is not None:
                    header_name = find_dict_key(header_dict, incoming_header_name)
                    # Prep to check timestamp to see if incoming field is older
                    timestamp_field = header_name + "_TS"
                    field_timestamp = p_df.loc[
                        p_df["AVID"] == AV_ID, timestamp_field
                    ].values[0]
                    # make timestamp = 0 if theres nothing in there. for comparison operator to work
                    if not field_timestamp:
                        p_df.loc[p_df["AVID"] == AV_ID, timestamp_field] = 0
                        field_timestamp = p_df.loc[
                            p_df["AVID"] == AV_ID, timestamp_field
                        ].values[0]
                    # aliasing fields into variables for easy reference
                    past_field = p_df.loc[p_df["AVID"] == AV_ID, header_name].values[0]
                    incoming_field = i_df.loc[
                        i_df[header_dict["AVID"]] == AV_ID, header_dict[header_name]
                    ].values[0]
                    # Check timestamp to see if incoming field is older
                    # check field to see if data is identical
                    if float(field_timestamp) > incoming_timestamp:
                        # if existing field is fresher than incoming field
                        if (past_field == incoming_field) or (
                            pd.isna(past_field) and pd.isna(incoming_field)
                        ):
                            # 	If yes, DO NOTHING
                            pass
                        else:
                            # 	If no, FLAG INSPECT FIELD
                            # Manually inspect for extra relevant info, then update it manually.
                            # Refine this process more in practice
                            fns.flag_inspect(p_df, AV_ID, header_name, True)

                    # If no, incoming field is newer. Check to see if data is identical
                    else:
                        if (past_field == incoming_field) or (
                            pd.isna(past_field) and pd.isna(incoming_field)
                        ):
                            # 	If yes, UPDATE TIMESTAMP FIELD
                            fns.update_timestamp(
                                incoming_timestamp, p_df, AV_ID, header_name
                            )
                        else:
                            # 	If no, FLAG UPDATE FIELD + UPDATE TIMESTAMP FIELD
                            fns.flag_update(p_df, AV_ID, header_name, True)
                            fns.update_timestamp(
                                incoming_timestamp, p_df, AV_ID, header_name
                            )

        elif not pd.isna(AV_ID):
            # If AVID not present,
            # add the new record onto the past_imports list
            p_df = inr.import_1_new_record(header_dict, p_df, i_df, AV_ID)
            fns.flag_update_all_fields(p_df, AV_ID, True, __df_headers_no_flags)
            fns.flag_inspect_all_fields(p_df, AV_ID, False, __df_headers_no_flags)
            fns.update_timestamp_all_fields(
                incoming_timestamp, p_df, AV_ID, __df_headers_no_flags
            )

    # output new csv file containing past imports
    filename = f"{incoming_timestamp}_actions_to_take.csv"
    p_df.to_csv(filename, index=False)
    return filename


# tester block for flaggers
if __name__ == "__main__":
    print("I'm actually a module, but I can do some tests for you.")

    past_filename = "tester_20240528.1234_past_imports.csv"
    past_imports = pd.read_csv(past_filename)
    print("Past imports file is", past_filename)

    incoming_filename = "tester_ April 1 n 2 2022 attendees final.csv"
    incoming_import = pd.read_csv(incoming_filename)
    print("Incoming imports file is", incoming_filename)

    incoming_timestamp = None
    manual_timestamp = input(
        "Would you like to manually input the timestamp of this import? If not, the current date and time will be used instead. Y/N:"
    )
    if manual_timestamp == "Y":
        incoming_timestamp = float(
            input(
                "Enter the date and time of the import data as a decimal number in the format YYYYMMDD.hhmm:"
            )
        )
    else:
        incoming_timestamp = float(datetime.now().strftime("%Y%m%d.%H%M"))

    # initialise the header dictionary
    header_dict = build_header_dict(past_imports, incoming_import, False)
    pp("Initialized header dictionary to default one.")

    pp(
        check_against_past_imports(
            past_imports, incoming_import, incoming_timestamp, header_dict
        )
    )


# # tester block for inr
# if __name__ == "__main__":
#     print("I prefer to be a module, but I can do some tests for you.")

#     past_filename = "past_imports.csv"
#     past_imports = pd.read_csv(past_filename)
#     print("Past imports file is", past_filename)

#     incoming_filename = "asdf April 1 n 2 2022 attendees final.csv"
#     incoming_import = pd.read_csv(incoming_filename)
#     print("Incoming imports file is", incoming_filename)

#     # initialise the header dictionary
#     header_dict = build_header_dict(past_imports, incoming_import, False)
#     pp("initialised header dictionary to default one.")
#     pp(header_dict)

#     check_against_past_imports(past_imports, incoming_import, header_dict)
