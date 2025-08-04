import re
import urllib
import urllib.request
import json
import inflect

from urllib.parse import quote
from pprint import pprint
from nntool.utils import read_toml_file


def to_singular(text: str):
    # Create an inflect engine
    p = inflect.engine()

    # Split text into words
    words = text.split()

    # Convert each word to its singular form if possible
    singular_words = [p.singular_noun(word) if p.singular_noun(word) else word for word in words]

    # Join the words back into a single string
    result = " ".join(singular_words)
    return result


instruction_prefix_by_model = {
    "qwen2-72b": [
        (
            r"the most likely cell type \(one cell type name\) is ([^\n,\.]+)",
            1,
        )
    ],
    "zero-shot-qwen2-72b": [
        (
            r"cell type(.*?)(is|are|would be|corresponds to|could be) ([^\n,\.]+)",
            3,
        ),
        (r"([^\n,\.]+) (is|are|would be|corresponds to|could be)(.*?)cell type", 0),
    ],
}


def clean_answer(
    answer: str,
    instruction_prefix: str = "",
    instruction_prefix_group_index: int = 0,
    instruction_model: str = "",
    model_name: str = "",
):
    prefix = []
    if instruction_prefix:
        prefix.append((instruction_prefix, instruction_prefix_group_index))
    elif instruction_model:
        prefix = instruction_prefix_by_model[instruction_model]
    else:
        pass

    if prefix:
        # matches any character that is not a newline (\n), comma (,), or period (.), zero or more times.
        for pat, gid in prefix:
            match = re.search(pat, answer)
            if match:
                break

        # if there is no candidate in list, null is set.
        pred = match.group(gid) if match else ""
    else:
        # matches any character that is not a newline (\n), comma (,), or period (.), zero or more times.
        pattern = r"^[^\n,\.]*"
        match = re.match(pattern, answer)

        # if there is no candidate in list, null is set.
        pred = match.group(0) if match else ""

    # clean up the answer
    pred = re.sub(r"\"|\'|\n|\.|\s|\:|\,|\*", " ", pred)
    pred = pred.strip()
    pred = to_singular(pred)

    # special case for "cell type"
    if "gpt-4" in model_name:
        pred = pred.replace("activated", "").strip()

    return pred


def bioportal_rest(cell_name: str):
    REST_URL = "http://data.bioontology.org"
    API_KEY = read_toml_file("env.toml")["bioportal"]["token"]

    def get_json(url):
        opener = urllib.request.build_opener()
        opener.addheaders = [("Authorization", "apikey token=" + API_KEY)]
        return json.loads(opener.open(url).read())

    # Do a search for every term
    search_results = []
    results = get_json(REST_URL + "/search?q=" + quote(cell_name) + "&ontologies=CL")
    breakpoint()
    search_results.append(results["collection"])

    # Print the results
    for result in search_results:
        pprint(result)
    return search_results


if __name__ == "__main__":
    # for sample in samples:
    #     answer = sample["messages"][0]["generated_text"][-1]["content"]
    #     cleaned_answer = clean_answer(answer)
    #     cl_matches = map_cell_name_to_cl_name(cleaned_answer)

    #     print(f"Before: {answer}")
    #     print(f"After: {cleaned_answer}")
    #     print(f"Mapped CL name: {cl_matches.name}, CL ID: {cl_matches.id}")
    #     print("Label:", sample["sample"]["label"])
    #     print("Label CL:", sample["sample"]["label_cl"])
    #     print()

    # bioportal_rest("Sst+ Chodl+ GABAergic neuron")
    bioportal_rest("Conventional Dendritic Cell 2")
