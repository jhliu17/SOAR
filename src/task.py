import json
import pprint
from typing import Any

from tqdm import tqdm
from pathlib import Path
from dataclasses import asdict, dataclass, field
from transformers import set_seed
from nntool.slurm import SlurmConfig
from torch.utils.data import Subset, DataLoader

from src.dataset import (
    CSVDatasetConfig,
    DatasetBaseConfig,
    H5ADDataset,
    H5ADDatasetConfig,
)
from src.pipeline import PipelineConfig, GenerationConfig
from src.pipeline import (
    CellTypeAnnotationPipeline,
    PipelineBase,
    Cell2SentCellTypeAnnotationPipeline,
    ChatGPTCellTypeAnnotationPipeline,
)
from src.dataset import CSVDataset
from src.prompt_templates.factory import (
    PromptTemplateBase,
    RankedGeneNamesPromptTemplate,
    ZeroShotRankedGeneNamesPromptTemplate,
    ZeroShotRankedGeneNamesPromptTemplateForSCACT,
    ZeroShotCoTRankedGeneNamesPromptTemplate,
    ZeroShotCoTRankedGeneNamesPromptTemplateForSCACT,
    FewShotRankedGeneNamesPromptTemplate,
)

prompter_cls: dict[str, PromptTemplateBase] = {
    "ranked_gene": RankedGeneNamesPromptTemplate,
    "zero_shot": ZeroShotRankedGeneNamesPromptTemplate,
    "zero_shot_scact": ZeroShotRankedGeneNamesPromptTemplateForSCACT,
    "zero_shot_cot": ZeroShotCoTRankedGeneNamesPromptTemplate,
    "zero_shot_cot_scact": ZeroShotCoTRankedGeneNamesPromptTemplateForSCACT,
    "few_shot": FewShotRankedGeneNamesPromptTemplate,
}

pipeline_cls: dict[str, PipelineBase] = {
    "CellTypeAnnotationPipeline": CellTypeAnnotationPipeline,
    "Cell2SentCellTypeAnnotationPipeline": Cell2SentCellTypeAnnotationPipeline,
    "ChatGPTCellTypeAnnotationPipeline": ChatGPTCellTypeAnnotationPipeline,
}


@dataclass
class TaskConfig:
    output_folder: str = "outputs/"
    random_seed: int = 2024


class TaskBase:
    def __init__(self, config: TaskConfig):
        set_seed(config.random_seed)
        self.output_folder = Path(config.output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # save config file
        with open(self.output_folder / "config.json", "w") as f:
            json.dump(asdict(config), f, indent=4)

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def prepare_model(self):
        raise NotImplementedError


@dataclass
class CellTypeAnnotationTaskConfig(TaskConfig):
    promter_name: str = "ranked_gene"
    gene_num_limit: int = -1
    dataset: DatasetBaseConfig = field(default_factory=DatasetBaseConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    slurm: SlurmConfig = field(default_factory=SlurmConfig)


class CellTypeAnnotationTask(TaskBase):
    def __init__(self, config: CellTypeAnnotationTaskConfig):
        super().__init__(config)
        self.config = config
        self.gene_limit_num = (
            config.gene_num_limit if config.gene_num_limit > 0 else None
        )

    def prepare_input(
        self, batch: list[dict[str, Any]], post_batch: list[dict[str, Any]] = None
    ):
        prompter_name = self.config.promter_name
        prompter = prompter_cls[prompter_name]()

        messages = []
        for i, sample in enumerate(batch):
            if prompter_name in {"zero_shot", "zero_shot_scact", "ranked_gene"}:
                x = prompter.get_messages(
                    sample["tissue"],
                    sample["genes"][: self.gene_limit_num],
                )
            elif prompter_name in {"zero_shot_cot", "zero_shot_cot_scact"}:
                kwargs = (
                    {"reasoning": post_batch[i][0]["generated_text"][-1]["content"]}
                    if post_batch is not None
                    else {}
                )
                x = prompter.get_messages(
                    sample["tissue"], sample["genes"][: self.gene_limit_num], **kwargs
                )
            elif prompter_name in {
                "few_shot",
            }:
                x = prompter.get_messages(
                    sample["tissue"],
                    sample["genes"][: self.gene_limit_num],
                    demo=sample["demo"],
                )
            else:
                raise ValueError(f"Invalid prompter name: {prompter_name}")

            messages.append(x)
        return messages

    def prepare_dataset(self):
        dataset = None
        if isinstance(self.config.dataset, CSVDatasetConfig):
            dataset = CSVDataset(self.config.dataset)
        elif isinstance(self.config.dataset, H5ADDatasetConfig):
            dataset = H5ADDataset(self.config.dataset)
        else:
            raise NotImplementedError

        dataset = Subset(dataset, indices=list(range(len(dataset))))
        return dataset

    def run(self, *args, **kwargs):
        pipeline = pipeline_cls[self.config.pipeline.pipeline_class_name](
            self.config.pipeline
        )
        dataset = self.prepare_dataset()
        dataloader = DataLoader(
            dataset,
            batch_size=self.config.pipeline.batch_size,
            shuffle=False,
            collate_fn=lambda x: x,
        )

        context = []
        for batch in tqdm(dataloader):
            x = self.prepare_input(batch)
            responses = pipeline(x, self.config.generation)

            if self.config.promter_name in {"zero_shot_cot", "zero_shot_cot_scact"}:
                x = self.prepare_input(batch, responses)
                post_responses = pipeline(x, self.config.generation)
                pprint.pp(
                    [(r, pr) for r, pr in zip(responses, post_responses)], width=240
                )

                responses = post_responses

            for i, response in enumerate(responses):
                index = batch[i]["index"]
                context.append(
                    {
                        "index": index,
                        "sample": batch[i],
                        "messages": response,
                    }
                )
                pprint.pp(context[-1], width=240)

        with open(
            self.output_folder / f"{self.config.pipeline.model_custom_id}.json", "w"
        ) as f:
            json.dump(context, f, indent=4)
