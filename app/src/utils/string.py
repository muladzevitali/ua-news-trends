def clean_title(string: str) -> str:
    string = string.lower()
    return "".join(filter(str.isalpha, string))
