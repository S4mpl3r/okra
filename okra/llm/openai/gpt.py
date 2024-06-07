import base64

from numpy import dtype, ndarray, uint8
from openai import OpenAI
from typing_extensions import Any

from ..llm import LLM


class GPT(LLM):

    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        config: dict = {"temperature": 0.5, "max_tokens": 512},
    ) -> None:
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.config = config
        self.client = OpenAI()

    def _encode_image(self, image: bytes) -> str:
        return base64.b64encode(image).decode("utf-8")

    def run(
        self, text: str, image: ndarray[Any, dtype[uint8]], use_vision: bool = True
    ) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        if use_vision and "gpt-4" in self.model_name:
            base64_image = self._encode_image(bytes(image))
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            )
        else:
            messages.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **self.config,
        )
        return response.choices[0].message.content.strip()
