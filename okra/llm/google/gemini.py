from os import environ

from google.generativeai import GenerationConfig, GenerativeModel, configure
from numpy import dtype, ndarray, uint8
from typing_extensions import Any, Optional

from ..llm import LLM


class Gemini(LLM):

    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        max_history_length: Optional[int] = 10,
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
        self.max_history_length = max_history_length
        self.history = []

    def _append_message_to_history(self, message: dict):
        self.history.append(message)
        # if max_history_length is set, then make sure the chat history length does not exceed the max
        if self.max_history_length is not None:
            if len(self.history) > self.max_history_length:
                self.history = self.history[-self.max_history_length :]

    def run(
        self,
        text: str,
        image: ndarray[Any, dtype[uint8]],
        use_vision: bool = True,
    ) -> str:
        if use_vision:
            self._append_message_to_history(
                {
                    "role": "user",
                    "parts": [
                        text,
                        {"mime_type": "image/jpeg", "data": bytes(image)},
                    ],
                }
            )
        else:
            self._append_message_to_history({"role": "user", "parts": [text]})

        response = self.client.generate_content(self.history)

        response_text = response.text.strip()
        self._append_message_to_history({"role": "model", "parts": [response_text]})
        return response_text
