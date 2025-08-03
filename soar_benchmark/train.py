import json

from pathlib import Path
from dataclasses import dataclass, asdict
from transformers import set_seed
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, DataCollatorForCompletionOnlyLM
from soar_benchmark.pipeline import PipelineConfig, torch_dtype_map


@dataclass
class TrainerConfig:
    dataset_name: str
    dataset_load_from_hg: bool = False
    pipeline: PipelineConfig
    output_folder: str = "outputs/"
    random_seed: int = 2024
    response_template = " ### Answer:"


class TrainBase:
    def __init__(self, config: TrainerConfig):
        set_seed(config.random_seed)
        self.config = config
        self.output_folder = Path(config.output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # save config file
        with open(self.output_folder / "config.json", "w") as f:
            json.dump(asdict(config), f, indent=4)

        self.model, self.tokenizer = self.prepare_model_and_tokenizer(config.pipeline)

    def prepare_dataset(self, config: TrainerConfig):
        if config.dataset_load_from_hg:
            dataset = load_dataset(config.dataset_name, split="train")
        else:
            raise NotImplementedError
        return dataset

    def prepare_model_and_tokenizer(self, config: PipelineConfig):
        if config.huggingface_token:
            login(token=config.huggingface_token)

        # dispatch loading model and tokenizer
        load_from_str = config.model_name
        local_path = Path(config.local_ckpt_path)
        save_after_init = False
        if config.local_ckpt_path:
            if local_path.exists():
                load_from_str = str(local_path)
            else:
                save_after_init = True

        model = AutoModelForCausalLM.from_pretrained(
            load_from_str,
            torch_dtype=torch_dtype_map.get(config.torch_dtype, torch_dtype_map["bfloat16"]),
            device_map=config.device_map,
            **config.model_kwargs,
        )
        tokenizer = AutoTokenizer.from_pretrained(load_from_str, **config.tokenizer_kwargs)

        if save_after_init:
            model.save_pretrained(local_path)
            tokenizer.save_pretrained(local_path)
        return model, tokenizer

    def run(self, *args, **kwargs):
        raise NotImplementedError


class Cell2SentCellTypeAnnotationTrainer(TrainBase):
    def run(self, *args, **kwargs):
        dataset = self.prepare_dataset(self.config)

        def formatting_prompts_func(example):
            output_texts = []
            for i in range(len(example["instruction"])):
                text = f"### Question: {example['instruction'][i]}\n ### Answer: {example['output'][i]}"
                output_texts.append(text)
            return output_texts

        response_template = " ### Answer:"
        collator = DataCollatorForCompletionOnlyLM(response_template, tokenizer=self.tokenizer)

        trainer = SFTTrainer(
            self.model,
            train_dataset=dataset,
            args=SFTConfig(output_dir=self.output_folder),
            formatting_func=formatting_prompts_func,
            data_collator=collator,
        )

        trainer.train()
