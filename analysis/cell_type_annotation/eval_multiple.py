import json
import tyro

from copy import deepcopy
from pathlib import Path
from tqdm import tqdm
from evaluate import load
from collections import defaultdict
from typing import List, Literal
from analysis.cell_type_annotation.answer_cleansing import clean_answer


def map_squad_predref2bleu_predref(predictions, references):
    bleu_predictions = [p["prediction_text"].lower() for p in predictions]
    bleu_references = [[rr.lower() for rr in r["answers"]["text"]] for r in references]
    return bleu_predictions, bleu_references


def eval(
    chat_results_path: List[str],
    normalized_answers_path: List[str] = [
        "outputs/cell_type_annotation_analysis/datasets/sora_rna/normalized_answers.json"
    ],
    squad_eval_results_path: str = "",
    instruction_prefix: str = "",
    instruction_prefix_group_index: int = 0,
    instruction_model: str = "",
    model_name: str = "",
    save_results: bool = True,
    group_by: Literal["dataset", "tissue", ""] = "dataset",
):
    squad_metric = load("squad")
    bleu_metric = load("bleu")
    rouge = load("rouge")
    meteor = load("meteor")

    predictions = []
    references = []
    id2prediction = {}
    id2normalized_answers = {}
    for chat_path, normalized_path in zip(chat_results_path, normalized_answers_path):
        with open(chat_path) as f:
            generated_results = json.load(f)

        with open(normalized_path) as f:
            normalized_answers = json.load(f)

        for result in tqdm(generated_results):
            total_problem_id = str(len(id2prediction))
            problem_id = str(result["index"])
            answer = result["messages"][0]["generated_text"][-1]["content"]
            cleaned_answer = clean_answer(
                answer,
                instruction_prefix,
                instruction_prefix_group_index,
                instruction_model,
                model_name=model_name,
            )

            prediction = {
                "prediction_text": cleaned_answer,
                "id": total_problem_id,
            }
            predictions.append(prediction)

            # the id need to be updated
            answer = deepcopy(normalized_answers[problem_id]["normalized_answers"])
            answer["id"] = total_problem_id
            references.append(answer)
            id2prediction[total_problem_id] = prediction
            id2normalized_answers[total_problem_id] = normalized_answers[problem_id]

    squad_results = squad_metric.compute(predictions=predictions, references=references)
    print("All SQUAD")
    print(squad_results)

    bleu_predictions, bleu_references = map_squad_predref2bleu_predref(
        predictions, references
    )
    bleu_results = bleu_metric.compute(
        predictions=bleu_predictions, references=bleu_references, max_order=2
    )
    print("All BLEU")
    print(bleu_results)

    rouge_results = rouge.compute(
        predictions=bleu_predictions, references=bleu_references
    )
    print("All Rouge")
    print(rouge_results)

    meteor_results = meteor.compute(
        predictions=bleu_predictions, references=bleu_references
    )
    print("All Meteor")
    print(meteor_results)

    # save results
    if save_results:
        save_path = Path(squad_eval_results_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(squad_eval_results_path, "w") as f:
            json.dump([(p, r) for p, r in zip(predictions, references)], f, indent=4)

    # evaluate for each dataset
    if group_by:
        group_by_collection = defaultdict(list)
        for total_problem_id, sample in id2normalized_answers.items():
            group_by_collection[sample["sample"][group_by]].append(total_problem_id)

        for group_name, total_problem_ids in group_by_collection.items():
            sub_predictions = []
            sub_references = []

            for total_problem_id in total_problem_ids:
                sub_predictions.append(id2prediction[total_problem_id])
                sub_references.append(
                    id2normalized_answers[total_problem_id]["normalized_answers"]
                )

            print()
            print(group_name, len(sub_predictions), len(sub_references))
            print("squad")
            squad_results = squad_metric.compute(
                predictions=sub_predictions, references=sub_references
            )
            print(group_name, squad_results)

            print("bleu")
            bleu_sub_predictions, bleu_sub_references = map_squad_predref2bleu_predref(
                sub_predictions, sub_references
            )
            bleu_results = bleu_metric.compute(
                predictions=bleu_sub_predictions,
                references=bleu_sub_references,
                max_order=2,
            )
            print(group_name, bleu_results)


if __name__ == "__main__":
    tyro.cli(eval)
