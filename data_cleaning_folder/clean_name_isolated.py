import re
import pandas as pd

# List of name words that should not be titlecased if entered in lowercase
__special_words = [
    "al",
    "el",
    "bin",
    "binti",
    "binte",
    "da",
    "de",
    "das",
    "dos",
    "delle",
    "della",
    "du",
    "del",
    "den",
    "der",
    "la",
    "le",
    "lo",
    "van",
    "von",
]


def __title_case_word(word):
    # Convert word to title case if it's not in special_words.
    return word if word.lower() in __special_words else word.capitalize()


def __process_initials(word):
    # Convert initials to format with periods and spaces.
    return ". ".join(word) + "."


# handles float NaN values
def correct_name(name: str | float):
    # Correct the lettercase and formatting of a name
    # Split name into words based on space, dash, or period

    if not name or pd.isna(name):
        return None

    name = name.strip()
    parts = re.split(r"(\s+|-|\.)", name)

    corrected_parts = []
    for part in parts:
        if part.isspace() or part in "-":
            corrected_parts.append(part)
        if part in ".":
            corrected_parts.append(" ")
        elif len(part) > 2 and part.isupper():
            # If part is all caps and has more than 2 letters, convert to title case
            corrected_parts.append(part.capitalize())
        elif len(part) <= 2 and part.isupper():
            # If part is all caps and has 2 or fewer letters, treat as initials
            corrected_parts.append(__process_initials(part))
        elif part.islower():
            # If part is all lowercase, convert to title case or keep if special word
            corrected_parts.append(__title_case_word(part))
        elif part not in ["-", ".", " "]:
            # If part is a combination or already formatted correctly, keep original
            corrected_parts.append(part)
    # Join corrected parts into the final name
    corrected_name = "".join(corrected_parts)
    # remove double spaces
    while "  " in corrected_name:
        corrected_name = corrected_name.replace("  ", " ")

    return corrected_name


if __name__ == "__main__":

    # record_to_post = {
    #     "attribute_AudienceView ID": 135708,
    #     "lastname": "Achinoam",
    #     "firstname": "Gregorius",
    #     "phone": "0",
    #     "email": "Achinoam@Gregorius.ca",
    # }

    # Test cases
    names = [
        " audrey",
        "katherine",
        "MINGYAN",
        "da vinci",
        "da Vinci",
        "vanSlyke",
        "VanSlyke",
        "van Slyke",
        "mccullough",
        "MCCULLOUGH",
        "mcCullough",
        "McCullough",
        "LEIGH-WILLIAMS",
        "O'CALLAGHAN",
        "Thelonius S",
        "J.P. Morgan",
        "JP Morgan",
        "JP MORGAN",
        "J.P.MORGAN",
    ]

    for name in names:
        print(f"{name} -> {correct_name(name)}")
        correct_name()
