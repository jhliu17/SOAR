import json
import tyro

from typing import List
from evaluate import load


def eval(
    squad_eval_results_path: List[str] = ["outputs/cell_type_annotation_analysis/qwen2-72b/squad_eval_inflect.json"],
    compute_bert_score: bool = False,
):
    bleu = load("bleu")

    predictions = []
    references = []
    for result_path in squad_eval_results_path:
        with open(result_path) as f:
            generated_results = json.load(f)
            for l in generated_results:
                predictions.append(l[0]["prediction_text"].lower())
                references.append([ll.lower() for ll in l[1]["answers"]["text"]])

    results = bleu.compute(predictions=predictions, references=references, max_order=2)
    print("BLEU:\n", results)

    if compute_bert_score:
        bertscore = load("bertscore")
        results = bertscore.compute(predictions=predictions, references=references, lang="en")
        print(results)

    rouge = load("rouge")
    results = rouge.compute(predictions=predictions, references=references)
    print("Rouge:\n", results)

    meteor = load("meteor")
    results = meteor.compute(predictions=predictions, references=references)
    print("Meteor:\n", results)


if __name__ == "__main__":
    tyro.cli(eval)
