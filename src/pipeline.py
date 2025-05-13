import torch
import re
import time
import datetime

from pathlib import Path
from huggingface_hub import login
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
from dataclasses import asdict, dataclass, field
from typing import Dict, Literal
from openai import OpenAI


@dataclass
class GenerationConfig:
    max_new_tokens: int = 256
    do_sample: bool = True
    temperature: float = 0.6
    top_p: float = 0.9


@dataclass
class PipelineConfig:
    model_custom_id: str
    model_name: str
    local_ckpt_path: str = ""
    local_finetuned_ckpt_path: str = ""
    torch_dtype: Literal["bfloat16"] = "bfloat16"
    device_map: str = "auto"
    pipeline_name: str = "text-generation"
    batch_size: int = 8
    model_kwargs: Dict[str, str] = field(default_factory=dict)
    tokenizer_kwargs: Dict[str, str] = field(default_factory=dict)
    huggingface_token: str = ""
    openai_token: str = ""
    pipeline_class_name: str = "CellTypeAnnotationPipeline"
    api_time_interval: float = 1


torch_dtype_map = {
    "float16": torch.float16,
    "float32": torch.float32,
    "bfloat16": torch.bfloat16,
}


def print_now(return_flag=0):
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, "JST")
    now = datetime.datetime.now(JST)
    now = now.strftime("%Y/%m/%d %H:%M:%S")
    if return_flag == 0:
        print(now)
    elif return_flag == 1:
        return now
    else:
        pass


class PipelineBase:
    """Reference implementation of a pipeline wrapper.

    https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct

    Example:
    pipe = pipeline(
        "text-generation",
        "meta-llama/Meta-Llama-3-8B-Instruct",
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    response = pipe(chat, max_new_tokens=512)
    print(response[0]["generated_text"][-1]["content"])
    """

    def __init__(self, config: PipelineConfig):
        self.config = config

        self.model, self.tokenizer = self.prepare_model_and_tokenizer(config)
        self.pipe = self.prepare_pipeline(config, self.model, self.tokenizer)

    def prepare_pipeline(self, config: PipelineConfig, model, tokenizer):
        pipeline_kwargs = {}
        pipe = pipeline(
            config.pipeline_name,
            model=model,
            tokenizer=tokenizer,
            batch_size=config.batch_size,
            **pipeline_kwargs,
        )

        # additional setup
        if "Meta-Llama-3" in config.model_name:
            # ref: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/discussions/56
            pipe.tokenizer.pad_token_id = pipe.model.config.eos_token_id
        elif "Mixtral" in config.model_name:
            # ref: https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1/discussions/187
            pipe.tokenizer.pad_token_id = pipe.model.config.eos_token_id
        return pipe

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
            torch_dtype=torch_dtype_map.get(
                config.torch_dtype, torch_dtype_map["bfloat16"]
            ),
            device_map=config.device_map,
            **config.model_kwargs,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            load_from_str, **config.tokenizer_kwargs
        )

        if save_after_init:
            model.save_pretrained(local_path)
            tokenizer.save_pretrained(local_path)
        return model, tokenizer

    def __call__(
        self, messages: list[dict[str, str]], generation_config: GenerationConfig
    ) -> dict:
        # additional kwargs
        pipeline_kwargs = {}
        if "Meta-Llama-3" in self.config.model_name:
            # ref: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/discussions/56
            terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
            ]
            pipeline_kwargs["eos_token_id"] = terminators
        else:
            pass

        return self.pipe(
            messages,
            **asdict(generation_config),
            **pipeline_kwargs,
            batch_size=self.config.batch_size,
        )

    def run(
        self,
        list_of_messages: list[list[dict[str, str]]],
        generation_config: GenerationConfig,
    ) -> dict:
        list_of_responses = []
        for messages in list_of_messages:
            responses = self(messages, generation_config)
            list_of_responses.append(responses)
        return list_of_responses


class CellTypeAnnotationPipeline(PipelineBase):
    def __init__(self, config: PipelineConfig):
        super().__init__(config)


class ChatGPTCellTypeAnnotationPipeline(PipelineBase):
    def __init__(self, config: PipelineConfig):
        super().__init__(config)
        self.client = OpenAI(api_key=config.openai_token)
        print_now()

    def prepare_model_and_tokenizer(self, config: PipelineConfig):
        return None, None

    def prepare_pipeline(self, config: PipelineConfig, model, tokenizer):
        return None

    def __call__(
        self, messages: list[dict[str, str]], generation_config: GenerationConfig
    ) -> dict:
        generated = []
        for message in messages:
            output_dict = self.decode(
                self.config.model_name,
                message,
                max_length=generation_config.max_new_tokens,
                i=-1,
                k=-1,  # no meaning for i and k
            )

            # outputs
            outputs = [{"generated_text": message.copy()}]
            outputs[0]["generated_text"].append(
                {"role": "assistant", "content": output_dict.content}
            )

            generated.append(outputs)

        return generated

    def decode(self, model, input, max_length, i, k):
        response = self.decoder_for_chatgpt(model, input, max_length, i, k)
        return response

    # Sentence Generator (Decoder) for ChatGPT ...
    def decoder_for_chatgpt(self, model, input, max_length, i, k):
        # GPT-3 API allows each users execute the API within 60 times in a minute ...
        time.sleep(self.config.api_time_interval)

        # Specify engine ...
        # Instruct GPT3
        if model == "gpt3":
            engine = "text-ada-001"
        elif model == "gpt3-medium":
            engine = "text-babbage-001"
        elif model == "gpt3-large":
            engine = "text-curie-001"
        elif model == "gpt3-xl":
            engine = "text-davinci-002"
        else:
            engine = model

        response = self.client.chat.completions.create(
            model=engine,
            messages=input,
            max_tokens=max_length,
            temperature=0,
            stop=None,
        )

        return response.choices[0].message


class Cell2SentCellTypeAnnotationPipeline(CellTypeAnnotationPipeline):
    """
    ref: https://huggingface.co/vandijklab/pythia-160m-c2s
    """

    def __init__(self, config: PipelineConfig):
        super().__init__(config)

    def prepare_model_and_tokenizer(self, config: PipelineConfig):
        if config.huggingface_token:
            login(token=config.huggingface_token)

        # dispatch loading model and tokenizer
        load_from_str = config.model_name  # "vandijklab/pythia-160m-c2s"
        local_path = Path(config.local_ckpt_path)
        save_after_init = False
        if config.local_ckpt_path:
            if local_path.exists():
                load_from_str = str(local_path)
            else:
                save_after_init = True

        # for cell2sent, we use customly fintuned model. However, the tokenizer is loaded from the huggingface model.
        model = AutoModelForCausalLM.from_pretrained(
            (
                config.local_finetuned_ckpt_path
                if config.local_finetuned_ckpt_path
                else load_from_str
            ),
            torch_dtype=torch_dtype_map.get(
                config.torch_dtype, torch_dtype_map["bfloat16"]
            ),
            device_map=config.device_map,
            attn_implementation="flash_attention_2",
            **config.model_kwargs,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            load_from_str, **config.tokenizer_kwargs
        )

        if save_after_init:
            model.save_pretrained(local_path)
            tokenizer.save_pretrained(local_path)
        return model, tokenizer

    def prepare_cellsentence(self, messages: list[dict[str, str]]) -> str:
        # assume gene names are listed in a list with [...]
        user_message = messages[-1]["content"]
        gene_names = re.findall(r"\[(.*?)\]", user_message)[0].replace(",", " ").split()
        cellsentence = " ".join(gene_names)

        # Prompts for other forms a generation.
        ctp = (
            "Identify the cell type most likely associated with these {gene_number} highly expressed genes listed in descending order. ".format(
                gene_number=len(gene_names)
            )
            + cellsentence
            + " The expected cell type based on these genes is: "
        )
        return ctp

    def complete_sentence(self, ctp: str) -> str:
        tokens = self.tokenizer(ctp, return_tensors="pt")
        input_ids = tokens["input_ids"].to(torch.device("cuda"))
        attention_mask = tokens["attention_mask"].to(torch.device("cuda"))

        with torch.inference_mode():
            outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                do_sample=True,
                max_length=2048,
                top_k=50,
                top_p=0.95,
            )

        output_text = self.tokenizer.decode(
            outputs[0, input_ids.size(1) :], skip_special_tokens=True
        )  # return newly generated tokens only
        return output_text

    def __call__(
        self, messages: list[dict[str, str]], generation_config: GenerationConfig
    ) -> dict:
        generated = []
        for message in messages:
            ctp = self.prepare_cellsentence(message)
            output_text = self.complete_sentence(ctp)

            # outputs
            outputs = [{"generated_text": message.copy()}]
            outputs[0]["generated_text"].append(
                {"role": "assistant", "content": output_text}
            )

            generated.append(outputs)

        return generated
