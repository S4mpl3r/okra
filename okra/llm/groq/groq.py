from groq import Groq
from numpy import dtype, ndarray, uint8
from typing_extensions import Any

from ..llm import LLM


class GroqLLM(LLM):

    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        config: dict = {"temperature": 0.5, "max_tokens": 512},
    ) -> None:
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.config = config
        self.client = Groq()

    def run(
        self, text: str, image: ndarray[Any, dtype[uint8]], use_vision: bool = True
    ) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": text},
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **self.config,
        )
        return response.choices[0].message.content.strip()
