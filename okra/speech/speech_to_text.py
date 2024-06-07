from abc import ABC, abstractmethod

from speech_recognition.audio import AudioData


class SpeechToText(ABC):

    @abstractmethod
    def transcribe(self, audio: AudioData) -> str:
        pass
