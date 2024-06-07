from os import environ

from google.generativeai import GenerationConfig, GenerativeModel, configure
from numpy import dtype, ndarray, uint8
from typing_extensions import Any

from ..llm import LLM


class Gemini(LLM):

    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        config: dict = {"temperature": 0.5, "max_output_tokens": 512},
    ) -> None:
        configure(api_key=environ.get("GOOGLE_API_KEY"))
        self.model_name = model_name
        self.generation_config = GenerationConfig(**config)
        self.system_prompt = system_prompt
        self.client = GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            system_instruction=system_prompt,
        )

    def run(
        self,
        text: str,
        image: ndarray[Any, dtype[uint8]],
        use_vision: bool = True,
    ) -> str:
        if use_vision:
            messages = [
                {
                    "role": "user",
                    "parts": [
                        text,
                        {"mime_type": "image/jpeg", "data": bytes(image)},
                    ],
                }
            ]
        else:
            messages = [
                {
                    "role": "user",
                    "parts": [text],
                }
            ]
        response = self.client.generate_content(messages)
        return response.text.strip()
