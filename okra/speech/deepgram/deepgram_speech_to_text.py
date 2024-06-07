from os import environ

from deepgram import DeepgramClient, PrerecordedOptions
from speech_recognition.audio import AudioData

from ..speech_to_text import SpeechToText


class DeepgramSpeechToText(SpeechToText):

    def __init__(self, model_name: str = "nova-2") -> None:
        self.client = DeepgramClient(api_key=environ.get("DEEPGRAM_API_KEY"))
        self.model_name = model_name
        self.options = PrerecordedOptions(
            model=model_name,
            smart_format=True,
            language="en",
        )

    def transcribe(self, audio: AudioData) -> str:
        response = self.client.listen.prerecorded.v("1").transcribe_file(
            {"buffer": audio.get_wav_data()},
            self.options,
        )
        return response["results"]["channels"][0]["alternatives"][0][
            "transcript"
        ].strip()
