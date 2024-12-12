import cust_API_requests as car  # has the logger file initialiser
import pandas as pd
import flags_n_stamps as fns
import data_cleaning as dc

# group 3 - flag resolving and calling API funcs

# imports for testing
from pprint import pprint as pp


__av_to_api_header_dict_for_POST = {
    "AVID": "attribute_AudienceView ID",
    "LastName": "lastName",
    "FirstName": "firstName",
    "Phone": "phone",
    "Email": "email",
}


# done, tested on normal record
# a dict is passed into this function. NaN values are float type
# returns array of headers to flag inspect if theres a problem
def __build_and_post_new_cust(
    record_to_post: dict, client_name: str, df_headers_no_flags: list
):
    flag_inspect = (
        []
    )  # this will be returned with a list of fields that need to have INS flagged
    # build body for initial customer POST
    body = {}
    for av_key, api_header in __av_to_api_header_dict_for_POST.items():
        body[api_header] = record_to_post[av_key]
    body = dc.clean_cust_body_in_isolation(body)  # clean it - handles NaN values
    cust_info = car.make_new_cust(body, client_name)  # POST it

    if cust_info.ok is False:
        flag_inspect.extend(df_headers_no_flags)  # flag all fields
        return flag_inspect

    # store customer id for contpref and address upload
    cust_id = cust_info.json()["id"]

    # check and update contact preference
    if not pd.isna(
        record_to_post["EmailContPref"]
    ):  # if emailcontpref field is not empty
        if (
            record_to_post["EmailContPref"][:3].lower()
            == "yes"  # the [:3] will not cause an error even if string is shorter than 3. tested.
        ):  # if record has a positive for email cont pref
            res = car.turn_on_email_cont_pref(cust_id, client_name)
            # dont check for other results, leave all as no.

    res = __clean_build_and_post_address(
        cust_id, body["firstName"] + " " + body["lastName"], record_to_post, client_name
    )
    if res is None:
        flag_inspect.extend(["Street", "Country", "City", "Province", "PostalCode"])
        return flag_inspect
    # if everything goes well with no issues, return None.
    return None


# done, tested on normal record
# should tolerate NaN values
# cleans, builds and posts address
# if no valid address/API call unsuccessful, flags inspect by returning None
def __clean_build_and_post_address(
    cust_id, cust_full_name, record_to_post, client_name
):
    # check if address field is present
    # # requires name, postal code, line 1 at least, city, province, country
    if (
        all(
            record_to_post.get(field)
            for field in ["Street", "Country", "City", "Province", "PostalCode"]
        )
        and (pd.notna(record_to_post["Street"]))
        and (pd.notna(record_to_post["City"]))
        and (pd.notna(record_to_post["Country"]))
    ):
        # clean street field. function returns {} if no valid address
        street_dict = dc.format_street_address(record_to_post["Street"])
        if not street_dict:
            return None
        # format country and province field to iso codes. non canadian addresses are kicked
        province = dc.format_province_to_iso(record_to_post["Province"])
        if province and (pd.notna(record_to_post["Province"])):
            country = "CA"
        else:
            return None
        # fill in a shell postal code if necessary. at this point, street province country have been validated
        if pd.isna(record_to_post["PostalCode"]) or not record_to_post["PostalCode"]:
            record_to_post["PostalCode"] = "A0A0A0"
        # attempt to post address
        # build address body
        # make "name" the customer name
        # country must be real country ISO code
        # province must be real province spelled out or ISO code (code can include country or not, works both ways. eg CA_NS or NS)
        # empty fields must be 0 length strings
        address_body = {
            "isDelivery": True,
            "isBilling": True,
            "country": country,
            "administrativeDivision": province,
            "name": cust_full_name,
            "postcode": record_to_post["PostalCode"],
            "town": record_to_post["City"],
        }
        dict_keys = ["line1", "line2", "line3", "line4", "line5"]
        for key in dict_keys:
            address_body[key] = street_dict[key]
        res = car.add_new_address(address_body, cust_id, client_name)
        if res.ok:
            return True
    return None  # a None return signals to parent block (__build_n_post_new_cust) to flag inspect on the address record


# done
def __records_with_upd_flags(actions_to_take_df):
    a_df = actions_to_take_df
    flag_columns = [col for col in a_df.columns if col.endswith("_UPD")]
    mask = a_df[flag_columns].any(axis=1)
    list_emails_with_upd_flags = a_df.loc[mask, "Email"].tolist()
    return list_emails_with_upd_flags


# done not tested
# should tolerate possible NaN values
# referred to in onenote as "normal update process"
# returns a dict of 2 arrays:  what fields to flag inspect, and then what fields to update timestamp on
def __compare_clean_n_update_cust_rec(
    cust_lookup_res: dict, record_to_update: pd.DataFrame, client_name: str
):
    ret = {"inspect": [], "timestamp": []}
    # transform record into a dict for easy access
    incoming_record = record_to_update.to_dict(orient="records")[0]
    # non-address related fields
    # build the cust and then pass it to dc to clean
    cust_overwrite_body = {}

    # compare audienceview ID
    spx_AVID = cust_lookup_res["attribute_AudienceViewID"]
    if not spx_AVID:
        cust_overwrite_body["attribute_AudienceView ID"] = incoming_record["AVID"]
    if str(spx_AVID) == str(int(incoming_record["AVID"])):
        ret["timestamp"].append("AVID")
    else:
        ret["inspect"].append("AVID")

    # clean and compare lastname
    formatted_lastname = dc.correct_name(incoming_record["LastName"])
    temp_compare = dc.name_is_similar(formatted_lastname, cust_lookup_res["lastName"])
    if temp_compare == 2:
        ret["timestamp"].append("LastName")
    if temp_compare == 1:
        cust_overwrite_body["lastName"] = formatted_lastname
        ret["timestamp"].append("LastName")
    if temp_compare == 0:
        ret["inspect"].append("LastName")

    # clean and compare firstname
    formatted_firstname = dc.correct_name(incoming_record["FirstName"])
    temp_compare = dc.name_is_similar(formatted_firstname, cust_lookup_res["firstName"])
    if temp_compare == 2:
        ret["timestamp"].append("FirstName")
    if temp_compare == 1:
        ret["timestamp"].append("FirstName")
        if (
            " and " not in incoming_record["FirstName"]
            and " & " not in incoming_record["FirstName"]
        ):
            # dont modify firstname if spektrix firstname contains " and " or " & "
            cust_overwrite_body["firstName"] = formatted_firstname
    if temp_compare == 0:
        ret["inspect"].append("FirstName")

    # clean and compare phone (check mobile field in spektrix too)
    # draw grid of possible case combos of 2: [N 0 1 2] (N meaning no data in spx)
    formatted_phone = dc.format_phone_number(incoming_record["Phone"])
    if pd.notna(incoming_record["Phone"]):
        phone_compare = dc.phone_is_similar(formatted_phone, cust_lookup_res["phone"])
        mobile_compare = dc.phone_is_similar(formatted_phone, cust_lookup_res["mobile"])
        if phone_compare == 2 or mobile_compare == 2:
            ret["timestamp"].append("Phone")
        else:
            # we know there are no exact matches. check similar matches
            temp_bool = False
            if phone_compare == 1:
                cust_overwrite_body["phone"] = formatted_phone
                temp_bool = True
            elif mobile_compare == 1:
                cust_overwrite_body["mobile"] = formatted_phone
                temp_bool = True
            if temp_bool == True:
                ret["timestamp"].append("Phone")
            else:  # at this point we know they're both returning 0 similarity, check if spx field is blank
                if not cust_lookup_res["phone"]:
                    cust_overwrite_body["phone"] = formatted_phone
                    ret["timestamp"].append("Phone")
                elif not cust_lookup_res["mobile"]:
                    cust_overwrite_body["mobile"] = formatted_phone
                    ret["timestamp"].append("Phone")
                else:
                    ret["inspect"].append("Phone")

    # patch in the overwrite
    if cust_overwrite_body:
        patch_call = car.overwrite_fields(
            cust_overwrite_body, cust_lookup_res["id"], client_name
        )

    # deal with contact preference
    if not pd.isna(incoming_record["EmailContPref"]):
        if incoming_record["EmailContPref"][:3].lower() == "yes":
            contpref_on = car.turn_on_email_cont_pref(
                cust_lookup_res["id"], client_name
            )
            # dont check for a "no", because blanks would register as turning off contpref
            # on spektrix they would likely have it as "not asked" anyway.
            # in the scenario that it's "yes" on spektrix that's only because they made it "yes" before
            # they can easily unsub
            ret["timestamp"].append("EmailContPref")

    # address related fields
    # build out a dict of incoming address
    incoming_address = {
        "country": incoming_record["Country"],
        "administrativeDivision": incoming_record["Province"],
        "town": incoming_record["City"],
        "postcode": incoming_record["PostalCode"],
        "streetadd": incoming_record["Street"],
    }

    # clean address entry
    formatted_incoming_address = {}
    # 1. country
    formatted_incoming_address["country"] = (
        "CA"  # assume it's canada. if it's not, inspect will be flagged in later step
    )
    # 2. province
    if dc.format_province_to_iso(
        incoming_address["administrativeDivision"]
    ):  # checks that iso format returns something prevent error from concatenating str and None
        formatted_incoming_address["administrativeDivision"] = (
            "CA_"
            + dc.format_province_to_iso(incoming_address["administrativeDivision"])
        )
    else:
        formatted_incoming_address["administrativeDivision"] = None
    # 3. city
    formatted_incoming_address["town"] = incoming_address["town"]
    # 4. postcode
    formatted_incoming_address["postcode"] = incoming_address[
        "postcode"
    ]  # rely on vetting street addresses and province ISO to weed out invalid entries
    if (not formatted_incoming_address["postcode"]) or pd.isna(
        formatted_incoming_address["postcode"]
    ):
        formatted_incoming_address["postcode"] = (
            "A0A 0A0"  # wont throw away otherwise valid addresses if postcode was not included
        )
    # 5. street address
    storage_formatted_street_address = dc.format_street_address(
        incoming_address["streetadd"]
    )
    if storage_formatted_street_address:
        formatted_incoming_address["streetadd"] = storage_formatted_street_address[
            "whole_address"
        ]
    else:
        formatted_incoming_address["streetadd"] = None

    # check if incoming fields are filled
    if (
        not formatted_incoming_address["administrativeDivision"]
        or not formatted_incoming_address["streetadd"]
        or not formatted_incoming_address["town"]
        or pd.isna(formatted_incoming_address["administrativeDivision"])
        or pd.isna(formatted_incoming_address["streetadd"])
        or pd.isna(formatted_incoming_address["town"])
    ):
        # flag inspect, do not update address
        ret["inspect"].extend(["Country", "Province", "City", "PostalCode", "Street"])
    else:  # do comparisons
        res = car.lookup_cust_addresses(cust_lookup_res["id"], client_name)
        if not res:  # check if spektrix has addresses
            # build and post address
            post_body = {
                "isDelivery": True,
                "isBilling": True,
                "country": formatted_incoming_address["country"],
                "administrativeDivision": formatted_incoming_address[
                    "administrativeDivision"
                ],
                "name": cust_lookup_res["firstName"]
                + " "
                + cust_lookup_res["lastName"],
                "line1": storage_formatted_street_address["line1"],
                "line2": storage_formatted_street_address["line2"],
                "line3": storage_formatted_street_address["line3"],
                "line4": storage_formatted_street_address["line4"],
                "line5": storage_formatted_street_address["line5"],
                "postcode": formatted_incoming_address["postcode"],
                "town": formatted_incoming_address["town"],
            }
            post_call = car.add_new_address(
                post_body, cust_lookup_res["id"], client_name
            )
            if post_call.ok:
                ret["timestamp"].extend(
                    ["Country", "Province", "City", "PostalCode", "Street"]
                )
            else:
                ret["inspect"].extend(
                    ["Country", "Province", "City", "PostalCode", "Street"]
                )
        elif not (
            formatted_incoming_address["postcode"]
            and formatted_incoming_address["country"]
            and pd.notna(formatted_incoming_address["postcode"])
            and pd.notna(formatted_incoming_address["country"])
        ):
            ret["inspect"].extend(
                ["Country", "Province", "City", "PostalCode", "Street"]
            )
        else:
            # start matching against spektrix addresses
            similar_match = 0
            exact_match = 0
            similar_match_id = ""
            # at this point, None and NaN values have been eliminated from incoming side but not existing-in-API side
            # dc.aeis() will accept None or NaN values on API side but not incoming side.
            # it's rare, and really should be impossible, but it happened somehow that API isoCode was blank but had name NS-Nova Scotia
            #   see Tracy Keigan, address entry had province as "NS-Nova Scotia" with no isoCode.
            for address_dict in res.json():
                comparison_ret = dc.address_entry_is_similar(
                    address_dict, formatted_incoming_address
                )
                if comparison_ret == 2:
                    exact_match += 1
                if comparison_ret == 1:
                    similar_match += 1
                    similar_match_id = address_dict["id"]

            # if exact match is more than 0, dont update record, update timestamp.
            if exact_match > 0:
                ret["timestamp"].extend(
                    ["Country", "Province", "City", "PostalCode", "Street"]
                )
            # if similar match is 1, overwrite address, add timestamps
            elif similar_match == 1:
                # build address body and overwrite
                overwrite_body = {
                    "town": formatted_incoming_address["town"],
                    "postcode": formatted_incoming_address["postcode"],
                    "line1": storage_formatted_street_address["line1"],
                    "line2": storage_formatted_street_address["line2"],
                    "line3": storage_formatted_street_address["line3"],
                    "line4": storage_formatted_street_address["line4"],
                    "line5": storage_formatted_street_address["line5"],
                }
                overwrite_call = car.edit_address(
                    overwrite_body, similar_match_id, cust_lookup_res["id"], client_name
                )
                if overwrite_call.ok:
                    ret["timestamp"].extend(
                        ["Country", "Province", "City", "PostalCode", "Street"]
                    )
                else:
                    ret["inspect"].extend(
                        ["Country", "Province", "City", "PostalCode", "Street"]
                    )
            # if similar match is 0, append address, add timestamps
            elif similar_match == 0:
                # build and post new address
                post_body = {
                    "isDelivery": True,
                    "isBilling": True,
                    "country": formatted_incoming_address["country"],
                    "administrativeDivision": formatted_incoming_address[
                        "administrativeDivision"
                    ],
                    "name": cust_lookup_res["firstName"]
                    + " "
                    + cust_lookup_res["lastName"],
                    "line1": storage_formatted_street_address["line1"],
                    "line2": storage_formatted_street_address["line2"],
                    "line3": storage_formatted_street_address["line3"],
                    "line4": storage_formatted_street_address["line4"],
                    "line5": storage_formatted_street_address["line5"],
                    "postcode": formatted_incoming_address["postcode"],
                    "town": formatted_incoming_address["town"],
                }
                post_call = car.add_new_address(
                    post_body, cust_lookup_res["id"], client_name
                )
                if post_call.ok:
                    ret["timestamp"].extend(
                        ["Country", "Province", "City", "PostalCode", "Street"]
                    )
                else:
                    ret["inspect"].extend(
                        ["Country", "Province", "City", "PostalCode", "Street"]
                    )
            else:
                # flag inspect on record for having too many similarity matches
                ret["inspect"].extend(
                    ["Country", "Province", "City", "PostalCode", "Street"]
                )

    return ret


# takes actions to address update flags
# puts down UPD flags, puts up INS flags
# modifies dataframe and passes it back to main
def resolve_update_flags(
    actions_to_take_df, client_name, incoming_timestamp, HEADER_DICT
) -> pd.DataFrame:
    df_headers_no_flags = [key for key in HEADER_DICT.keys() if "_" not in key]

    a_df = actions_to_take_df
    # filter for records with update flags on
    list_email_with_upd_flags = __records_with_upd_flags(a_df)
    #   search customer record by email in spektrix
    for (
        email
    ) in (
        list_email_with_upd_flags
    ):  # this doesnt work if incoming emails are not unique from each other. ensured in preprocessing
        res = car.lookup_cust_email(email, client_name)
        if res.status_code == 200:
            # if match, keep spektrix ID, run the fuzzy match stuff
            record_to_update = a_df.loc[
                a_df["Email"] == email
            ]  # generates a single line dataframe containing the customer to be updated

            # record_to_update.to_pickle(
            #     "single_line_for_testing_normal_update_function.pkl"
            # ) # PICKLE WAS GENERATED HERE -----------------------------------------------------------------------

            ccnucr_ret = __compare_clean_n_update_cust_rec(
                res.json(), record_to_update, client_name
            )
            # find the AVID for fns functions
            current_AVID = record_to_update.loc[
                record_to_update["Email"] == email, "AVID"
            ].iloc[0]
            # flag inspect according to return value
            for header_to_flag_inspect in ccnucr_ret["inspect"]:
                fns.flag_inspect(
                    a_df,
                    current_AVID,
                    header_to_flag_inspect,
                    True,
                )
            # update timestamps according to return value
            for header_to_timestamp in ccnucr_ret["timestamp"]:
                fns.update_timestamp(
                    incoming_timestamp,
                    a_df,
                    current_AVID,
                    header_to_timestamp,
                )
            # unflag all updates
            fns.flag_update_all_fields(
                a_df,
                current_AVID,
                False,
                df_headers_no_flags,
            )

        else:  # if not email match in spektrix
            record_to_post = a_df.loc[
                a_df["Email"] == email
            ]  # generates a single line dataframe containing the customer to be POSTed
            if (
                not record_to_post.empty
            ):  # if the generated dataframe exists and has an email
                record_to_post = record_to_post.iloc[
                    0
                ].to_dict()  # transform the record into a dictionary. NaN float values will be turned into NaN float values
                res = __build_and_post_new_cust(
                    record_to_post, client_name, df_headers_no_flags
                )  # cleans, gens body and POSTs it. returns None if everything went well. returns array of fields to flag inspect if there was an issue
                # note: you could consider using fns for this instead

                # find current AVID for fns funcs
                # record_to_post IS A DICTIONARY NOT A SINGLE LINE DATAFRAME
                current_AVID = record_to_post["AVID"]
                # false all update flags
                fns.flag_update_all_fields(
                    a_df,
                    current_AVID,
                    False,
                    df_headers_no_flags,
                )
                # update all timestamps
                fns.update_timestamp_all_fields(
                    incoming_timestamp,
                    a_df,
                    current_AVID,
                    df_headers_no_flags,
                )
                # true inspect flags for headers in the returned array
                if res:
                    for header in res:
                        fns.flag_inspect(
                            a_df,
                            current_AVID,
                            header,
                            True,
                        )

                # __a_df_header_upd_flags = []
                # for header in df_headers_no_flags:
                #     __a_df_header_upd_flags.append(header + "_UPD")

                # __a_df_header_timestamps = []
                # for header in df_headers_no_flags:
                #     __a_df_header_timestamps.append(header + "_TS")

                # record_index = a_df[
                #     a_df["Email"] == email
                # ].index  # Find the index of the row where "Email" column matches email
                # for header in __a_df_header_upd_flags:
                #     a_df.at[record_index[0], header] = False
                # # update all timestamps
                # for header in __a_df_header_timestamps:
                #     a_df.at[record_index[0].header] = incoming_timestamp
                # # true the inspect flags for headers in the returned array
                # if res:
                #     for header in res:
                #         a_df.at[record_index[0], header] = True

    return a_df


if __name__ == "__main__":
    # redacted for confidentiality
    pass
