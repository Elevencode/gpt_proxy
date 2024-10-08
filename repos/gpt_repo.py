import openai
import os
import logging

from dotenv import load_dotenv
from typing import List


load_dotenv()
logging.basicConfig(level=logging.INFO)

class GPTRepo:
    def __init__(self, model_engine= 'gpt-3.5-turbo-16k-0613',):
        self.model_engine = model_engine

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    async def get_gpt_answer(self, text: str, context):
        """
        Asynchronously sends a request to OpenAI to generate a completion for the given text.

        Params:
        - text (str): User message text.
        - context (List[dict]): context of current channel.

        Yields:
        - str: token (chunk) of an answer generated by GPT.

        Usage:
        >>> user = 'Hello, world! Tell me a fairytale'
        >>> await get_gpt_answer(text)
        token
        """
        messages = context + [{"role": "user", "content": text}]
        logging.info('Send request to openai...')
        try:
            async for chunk in await openai.ChatCompletion.acreate(
                model=self.model_engine,
                messages=messages,
                stream=True
            ):
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    yield content
        except Exception as e:
            logging.error(f'GPT ERROR: {e}')