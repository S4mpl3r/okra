from os import environ

from deepgram import DeepgramClient, SpeakOptions

from ..text_to_speech import TextToSpeech


class DeepgramTextToSpeech(TextToSpeech):

    def __init__(self, model_name: str = "aura-asteria-en"):
        self.client = DeepgramClient(api_key=environ.get("DEEPGRAM_API_KEY"))
        self.options = SpeakOptions(
            model=model_name,
            encoding="linear16",
            container="wav",
        )

    def speak(self, text: str) -> bytes:
        response = self.client.speak.v("1").stream({"text": text}, self.options)
        return b"".join(response["stream"])
