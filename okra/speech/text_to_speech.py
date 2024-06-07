from abc import ABC, abstractmethod


class TextToSpeech(ABC):

    @abstractmethod
    def speak(self, text: str) -> bytes:
        pass
