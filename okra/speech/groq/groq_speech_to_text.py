from groq import Groq
from speech_recognition.audio import AudioData

from ..speech_to_text import SpeechToText


class GroqSpeechToText(SpeechToText):

    def __init__(self, model_name: str = "whisper-large-v3") -> None:
        self.client = Groq()
        self.model_name = model_name

    def transcribe(self, audio: AudioData) -> str:
        transcription = self.client.audio.transcriptions.create(
            file=("test.wav", audio.get_wav_data()),
            model=self.model_name,
            language="en",
            temperature=0,
        )
        return transcription.text.strip()
