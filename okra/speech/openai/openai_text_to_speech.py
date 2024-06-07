from openai import OpenAI

from ..text_to_speech import TextToSpeech


class OpenAITextToSpeech(TextToSpeech):

    def __init__(self, model_name: str = "tts-1", voice_name: str = "alloy") -> None:
        self.client = OpenAI()
        self.model_name = model_name
        self.voice_name = voice_name

    def speak(self, text: str) -> bytes:
        response = self.client.audio.speech.create(
            model=self.model_name,
            voice=self.voice_name,
            input=text,
            response_format="wav",
        )
        return response.content
