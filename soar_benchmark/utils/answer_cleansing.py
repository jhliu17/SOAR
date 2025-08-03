import re


def clean_answer(answer: str):
    # matches any character that is not a newline (\n), comma (,), or period (.), zero or more times.
    pattern = r"^[^\n,\.]*"
    match = re.match(pattern, answer)

    # if there is no candidate in list, null is set.
    pred = match.group(0) if match else ""

    # clean up the answer
    pred = re.sub(r"\"|\'|\n|\.|\s|\:|\,|\*", " ", pred)
    pred = pred.strip()
    return pred
