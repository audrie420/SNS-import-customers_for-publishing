from thefuzz import fuzz
import pandas as pd


# returns 2 if names are identical
# 1 if names are similar
# 0 if they are completely different
def name_is_similar(str1, str2):
    if not (str1 and str2 and pd.notna(str1) and pd.notna(str2)):
        return 0

    # check if the strings are identical
    if str1 == str2:
        return 2

    # check if the strings are the same but with different formatting
    # use fuzz.ratio for similarity comparison
    similarity_score = fuzz.ratio(str1, str2)
    if similarity_score > 85:  # Threshold can be adjusted
        return 1

    # Use ratio to check similarity ignoring case, spaces, punctuation
    normalized_str1 = "".join(e.lower() for e in str1 if e.isalnum())
    normalized_str2 = "".join(e.lower() for e in str2 if e.isalnum())

    # If the normalized strings are identical
    if normalized_str1 == normalized_str2:
        return 1

    # use fuzz.ratio for similarity comparison after normalizing
    similarity_score = fuzz.ratio(normalized_str1, normalized_str2)
    if similarity_score > 87:  # Threshold can be adjusted
        return 1

    # check other fuzz criteria
    pre_norm_partial = fuzz.partial_ratio(str1, str2)
    partial = fuzz.partial_ratio(normalized_str1, normalized_str2)
    token_sort = fuzz.token_sort_ratio(normalized_str1, normalized_str2)
    token_set = fuzz.token_set_ratio(normalized_str1, normalized_str2)
    if (
        partial == 100
        and pre_norm_partial >= 40
        and (partial + token_sort + token_set) / 3 >= 85
    ):
        return 1
    if (partial + token_sort + token_set) / 3 >= 86:
        return 1

    # completely different information
    return 0


# # name and cleaned name
# if __name__ == "__main__":
#     from clean_name_isolated import correct_name

#     names = [
#         " audrey",
#         "katherine",
#         "MINGYAN",
#         "da vinci",
#         "da Vinci",
#         "vanSlyke",
#         "VanSlyke",
#         "van Slyke",
#         "mccullough",
#         "MCCULLOUGH",
#         "mcCullough",
#         "McCullough",
#         "LEIGH-WILLIAMS",
#         "O'CALLAGHAN",
#         "Thelonius S",
#         "J.P. Morgan",
#         "JP Morgan",
#         "JP MORGAN",
#         "J.P.MORGAN",
#     ]

#     cleaned_name = ""

#     for name in names:
#         cleaned_name = correct_name(name)
#         print("=====================")
#         ret = name_is_similar(name, cleaned_name)
#         print(f"{name}\n{cleaned_name}/nRelationship between strings is {ret}")


# different names
if __name__ == "__main__":
    from clean_name_isolated import correct_name

    names = [
        "jokerp",
        "adrian",
        " audrey",
        "katherine",
        "mccullough",
        "MCCULLOUGH",
        "McCullough",
        "LEIGH-WILLIAMS",
        "O'CALLAGHAN",
        "Thelonius S",
        "J.P. Morgan",
        "JP Morgan",
        "J.P.MORGAN",
    ]

    other_names = [
        "jakerp",
        "adrianna",
        " audrie",
        "katheryne",
        "MCCcULLOUGH",
        "Adrian mcCullough",
        "A McCul",
        "LEe-WILLIAMS",
        "O'CALAGHAN",
        "Thelonius Stork",
        "John-paul Morgan",
        "Jean paul Morgan",
        "John p MORGAN",
    ]

    cleaned_name = ""
    counter = 0

    for name in names:
        name = correct_name(name)
        other_name = other_names[counter]
        counter += 1
        print("=====================")
        ret = name_is_similar(name, other_name)
        print(f"{name}\n{other_name}\nRelationship between strings is {ret}")

    str1 = "jokarp"
    str2 = "jokerp"
    print(fuzz.ratio(str1, str2))
    print(fuzz.partial_ratio(str1, str2))
    print(fuzz.token_set_ratio(str1, str2))
    print(fuzz.token_sort_ratio(str1, str2))
