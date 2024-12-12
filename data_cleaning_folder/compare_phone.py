from thefuzz import fuzz
import pandas as pd


# returns 2 if names are identical
# 1 if names are similar
# 0 if they are completely different
def phone_is_similar(str1: str, str2: str):
    # check if the strings are identical
    if str1 == str2:
        return 2

    # screen for None or float nan values
    if (not str1) or (not str2) or pd.isna(str1) or pd.isna(str2):
        return 0

    # Use ratio to check similarity ignoring case, spaces, punctuation
    normalized_str1 = "".join(e.lower() for e in str1 if e.isalnum())
    normalized_str2 = "".join(e.lower() for e in str2 if e.isalnum())

    # If the normalized strings are identical
    if normalized_str1 == normalized_str2:
        return 1

    # 902 1234563 case - want to identify as diff
    # +1 1234567892 case - identify as same - partial match 100% and post norm simple ratio 90
    # 4165436666ext765 to x 765 case - identify as same - post norm simple min 90, post norm partial min 86, token sorts min 89

    # check other fuzz criteria
    simple = fuzz.ratio(normalized_str1, normalized_str2)
    partial = fuzz.partial_ratio(normalized_str1, normalized_str2)
    token_sort = fuzz.token_sort_ratio(normalized_str1, normalized_str2)
    token_set = fuzz.token_set_ratio(normalized_str1, normalized_str2)

    if partial == 100 and simple >= 90:
        return 1
    if simple >= 90 and partial >= 86 and (token_sort + token_set) / 2 >= 89:
        return 1

    # completely different information
    return 0


# need to move this file into parent folder to test.
# the alternative is some complicated shit. see chat in cgpt "python subfolder testing problem"
if __name__ == "__main__":
    from data_cleaning import (
        format_phone_number,
    )  # this wont work if file is in subfolder

    # redacted for confidentiality
