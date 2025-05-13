import os
import time
import datetime
import openai  # For GPT-3 API ...

from dataclasses import dataclass
from openai import OpenAI


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


@dataclass
class DecoderArgs:
    model: str
    api_time_interval: float = 0.1


class Decoder:
    def __init__(self, config):
        print_now()
        self.client = OpenAI()

    def decode(self, args, input, max_length, i, k):
        response = self.decoder_for_gpt3(args, input, max_length, i, k)
        return response

    # Sentence Generator (Decoder) for GPT-3 ...
    def decoder_for_gpt3(self, args, input, max_length, i, k):

        # GPT-3 API allows each users execute the API within 60 times in a minute ...
        # time.sleep(1)
        time.sleep(args.api_time_interval)

        # https://beta.openai.com/account/api-keys
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # print(openai.api_key)

        # Specify engine ...
        # Instruct GPT3
        if args.model == "gpt3":
            engine = "text-ada-001"
        elif args.model == "gpt3-medium":
            engine = "text-babbage-001"
        elif args.model == "gpt3-large":
            engine = "text-curie-001"
        elif args.model == "gpt3-xl":
            engine = "text-davinci-002"
        else:
            raise ValueError("model is not properly defined ...")

        response = self.client.chat.completions.create(
            model=engine,
            messages=input,
            max_tokens=max_length,
            temperature=0,
            stop=None,
        )

        return response["choices"][0]["message"]
