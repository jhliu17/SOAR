import json
import tyro

from pathlib import Path
from tqdm import tqdm
from evaluate import load
from collections import defaultdict
from analysis.cell_type_annotation.answer_cleansing import clean_answer


def eval(
    chat_results_path: str = (
        "outputs/cell_type_annotation/07042024_141209/qwen2-72b-instruct.json"
    ),
    normalized_answers_path: str = "outputs/cell_type_annotation_analysis/datasets/sora_rna/normalized_answers.json",
    squad_eval_results_path: str = (
        "outputs/cell_type_annotation_analysis/qwen2-72b/squad_eval_inflect.json"
    ),
    instruction_prefix: str = "",
    instruction_prefix_group_index: int = 0,
    instruction_model: str = "",
    model_name: str = "",
):
    squad_metric = load("squad")

    with open(chat_results_path) as f:
        generated_results = json.load(f)

    with open(normalized_answers_path) as f:
        normalized_answers = json.load(f)

    predictions = []
    id2prediction = {}
    references = []
    for result in tqdm(generated_results):
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
            "id": problem_id,
        }
        predictions.append(prediction)
        id2prediction[problem_id] = prediction
        references.append(normalized_answers[problem_id]["normalized_answers"])

    results = squad_metric.compute(predictions=predictions, references=references)
    print("All")
    print(results)

    # save results
    save_path = Path(squad_eval_results_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(squad_eval_results_path, "w") as f:
        json.dump([(p, r) for p, r in zip(predictions, references)], f, indent=4)

    # evaluate for each dataset
    datasets = defaultdict(list)
    for problem_id, sample in normalized_answers.items():
        datasets[sample["sample"]["dataset"]].append(problem_id)

    for dataset, problem_ids in datasets.items():
        sub_predictions = []
        sub_references = []

        for problem_id in problem_ids:
            sub_predictions.append(id2prediction[problem_id])
            sub_references.append(normalized_answers[problem_id]["normalized_answers"])

        print()
        print(dataset, len(sub_predictions), len(sub_references))
        results = squad_metric.compute(
            predictions=sub_predictions, references=sub_references
        )
        print(dataset, results)


if __name__ == "__main__":
    tyro.cli(eval)
