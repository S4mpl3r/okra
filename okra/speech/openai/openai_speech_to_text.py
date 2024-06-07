from openai import OpenAI
from speech_recognition.audio import AudioData

from ..speech_to_text import SpeechToText


class OpenAISpeechToText(SpeechToText):
    def __init__(self, model_name: str = "whisper-1") -> None:
        self.client = OpenAI()
        self.model_name = model_name

    def transcribe(self, audio: AudioData) -> str:
        transcription = self.client.audio.transcriptions.create(
            file=audio.get_wav_data(),
            model=self.model_name,
            language="en",
            temperature=0,
        )
        return transcription.text.strip()
