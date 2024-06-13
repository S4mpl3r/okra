from groq import Groq
from numpy import dtype, ndarray, uint8
from typing_extensions import Any, Optional

from ..llm import LLM


class GroqLLM(LLM):

    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        max_history_length: Optional[int] = 10,
        config: dict = {"temperature": 0.5, "max_tokens": 512},
    ) -> None:
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.config = config
        self.client = Groq()
        self.max_history_length = max_history_length
        self.history = [{"role": "system", "content": self.system_prompt}]

    def _append_message_to_history(self, message: dict):
        self.history.append(message)
        # if max_history_length is set, then make sure the chat history length does not exceed the max
        if self.max_history_length is not None:
            if len(self.history) > self.max_history_length:
                self.history = self.history[-self.max_history_length :]

    def run(
        self, text: str, image: ndarray[Any, dtype[uint8]], use_vision: bool = True
    ) -> str:
        self._append_message_to_history(
            {"role": "user", "content": text},
        )
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.history,
            **self.config,
        )
        response_text = response.choices[0].message.content.strip()
        self._append_message_to_history({"role": "assistant", "content": response_text})
        return response_text
