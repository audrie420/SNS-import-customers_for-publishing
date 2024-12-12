from thefuzz import fuzz
from data_cleaning_folder.compare_name import name_is_similar
from data_cleaning_folder.format_province import format_province_to_iso
import pandas as pd

# if i run the test program from inside here, it's
# from compare_name import name_is_similar
# but if i run from main folder and it calls this program
# the import fails unless its written as
# from data_cleaning_folder.compare_name import name_is_similar
# this is a weird stupid problem and i need to learn about packages or dependencies or whatever????

# note from future me: you figured it out lol see implementation in sns ticket imports cust api interactors

# for testing purposes
from pprint import pprint as pp


# does not tolerate None or NaN values
# returns 2 if addresses are identical
# 1 if addresses are similar
# 0 if they are completely different or if either one is None or NaN value
# done
def street_address_is_similar(str1, str2):
    # check if the strings are identical
    if str1 == str2:
        return 2

    # check if the strings are the same but with different formatting
    # use fuzz.ratio for similarity comparison
    similarity_score = fuzz.ratio(str1, str2)
    if similarity_score > 90:  # Threshold can be adjusted
        return 1

    # Use ratio to check similarity ignoring case, spaces, punctuation
    normalized_str1 = "".join(e.lower() for e in str1 if e.isalnum())
    normalized_str2 = "".join(e.lower() for e in str2 if e.isalnum())

    # If the normalized strings are identical
    if normalized_str1 == normalized_str2:
        return 1

    # use fuzz.ratio for similarity comparison after normalizing
    similarity_score = fuzz.ratio(normalized_str1, normalized_str2)
    if similarity_score > 92:  # Threshold can be adjusted
        return 1

    # check other fuzz criteria
    pre_norm_partial = fuzz.partial_ratio(str1, str2)
    partial = fuzz.partial_ratio(normalized_str1, normalized_str2)
    token_sort = fuzz.token_sort_ratio(normalized_str1, normalized_str2)
    token_set = fuzz.token_set_ratio(normalized_str1, normalized_str2)
    aggregate_score = (
        similarity_score * 5
        + (partial + pre_norm_partial) / 2 * 3
        + (token_set + token_sort) / 2 * 3
    ) / 11

    if (
        similarity_score >= 65
        and partial >= 80
        and token_set >= 65
        and token_sort >= 65
        and aggregate_score >= 73
    ):
        return 1

    # completely different information
    return 0


# receives one of the addresses output from API address lookup, and incoming address
# calls street_address_is_similar
# entry from api not cleaned upon function call - this function will take that into account
# incoming address cleaned before function call
# returns 0 if different, 1 if similar, 2 if exact match
def address_entry_is_similar(
    address_entry_from_api: dict, formatted_incoming_address_entry: dict
):
    # for an address to be similar to another, they must
    # be in same country and province
    # postcode leave unvetted
    # town is similar
    # street address is similar
    exact = True
    similar = True
    aefa = address_entry_from_api
    fiae = formatted_incoming_address_entry
    # compare country
    if aefa["country"]["isoCode"]:
        if fiae["country"].lower() != aefa["country"]["isoCode"].lower():
            exact = False
            similar = False
    else:  # if no country isocode
        exact = False
        similar = False
    # compare province
    if aefa["administrativeDivision"]["isoCode"]:
        if (
            fiae["administrativeDivision"].lower()
            != aefa["administrativeDivision"]["isoCode"].lower()
        ):
            exact = False
            similar = False
    elif aefa["administrativeDivision"]["name"]:
        if format_province_to_iso(aefa["administrativeDivision"]["name"]):
            if (
                fiae["administrativeDivision"].lower()
                != format_province_to_iso(
                    aefa["administrativeDivision"]["name"]
                ).lower()
            ): # if no province isocode and the province name field doesnt translate to a province iso code
                exact = False
                similar = False
        else:
            exact = False
            similar = False

    else:
        exact = False
        similar = False
    # compare town
    town_compare = name_is_similar(fiae["town"], aefa["town"])
    if town_compare != 2:
        exact = False
    if town_compare == 0:
        similar = False
    # compare postcode
    if fiae["postcode"].lower() != aefa["postcode"].lower():
        exact = False
    # compare streetadd
    api_streetadd = "\n".join(
        aefa[key] for key in ["line1", "line2", "line3", "line4", "line5"] if aefa[key]
    )
    streetadd_compare = street_address_is_similar(fiae["streetadd"], api_streetadd)
    if streetadd_compare != 2:
        exact = False
    if streetadd_compare == 0:
        similar = False

    # final evaluation
    if exact == True:
        return 2
    if similar == True:
        return 1
    return 0


# test address_entry_is_similar
if __name__ == "__main__":
    import cust_API_requests as car  # have to copy file into higher level folder to test

    # redacted for confidentiality