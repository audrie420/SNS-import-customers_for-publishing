# group 2 - past import db handlers


def find_dict_key(dict, value):
    associated_keys = [key for key, val in dict.items() if val == value]
    return associated_keys[0]


if __name__ == "__main__":
    import os

    print("running module tests for", os.path.basename(__file__))

    # Sample dictionary
    my_dict = {
        "key1": "value1",
        "key2": None,
        "key3": "value3",
        "key4": None,
        "key5": "value5",
    }
    res = find_dict_key(my_dict, "value5")
    print(res)
    print(type(res))
