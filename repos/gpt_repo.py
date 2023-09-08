import openai
import os
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.INFO)

class GPTRepo:
    def __init__(self, model_engine= 'gpt-3.5-turbo-16k-0613',):
        self.model_engine = model_engine

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    async def get_gpt_answer(self, text: str):
        logging.info('Send request to openai...')
        async for chunk in await openai.ChatCompletion.acreate(
            model=self.model_engine,
            messages=[{"role": "user", "content": text}],
            stream=True
        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                yield content