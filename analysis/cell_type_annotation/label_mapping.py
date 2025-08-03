import json
import time
import tyro

from tqdm import tqdm
from nntool.utils.utils_module import read_toml_file
from soar_benchmark.bioontology.decode import BioOntologyDecoder, BioOntologyDecoderConfig


def mapping(
    chat_results_path: str = ("outputs/cell_type_annotation/07042024_141209/qwen2-72b-instruct.json"),
    normalized_answers_path: str = "outputs/cell_type_annotation_analysis/datasets/sora_rna/normalized_answers.json",
    possible_label_mapping_path: str = "",
):
    api_key = read_toml_file("env.toml")["bioportal"]["token"]
    config = BioOntologyDecoderConfig(api_key=api_key)
    decoder = BioOntologyDecoder(config)

    def normalize_answer(cell_str: str, add_synonym=False):
        time.sleep(0.1)
        result = decoder.decode_one(cell_str, top_k=1)
        if add_synonym:
            return [result[0]["prefLabel"]] + result[0]["synonym"]
        else:
            return result[0]["prefLabel"]

    with open(chat_results_path) as f:
        generated_results = json.load(f)

    possible_label_mapping = {}
    if possible_label_mapping_path:
        with open(possible_label_mapping_path) as f:
            possible_label_mapping = json.load(f)

    references = {}
    for result in tqdm(generated_results):
        problem_id = str(result["index"])

        # mapping raw label if possible
        raw_label = result["sample"]["label"]
        if raw_label in possible_label_mapping:
            raw_label = possible_label_mapping[raw_label]

        # collect all possible labels
        labels = [raw_label]
        labels += normalize_answer(raw_label, add_synonym=True)

        references[problem_id] = {
            "sample": result["sample"],
            "normalized_answers": {
                "answers": {
                    "answer_start": [-1] * len(labels),
                    "text": labels,
                },
                "id": problem_id,
            },
        }

    with open(
        normalized_answers_path,
        "w",
    ) as f:
        json.dump(references, f, indent=4)


if __name__ == "__main__":
    tyro.cli(mapping)
