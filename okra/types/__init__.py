from rich.control import Control
from typing_extensions import Literal, Required, TypedDict

from ..llm.llm import LLM
from ..speech.speech_to_text import SpeechToText
from ..speech.text_to_speech import TextToSpeech


class GlobalConfig(TypedDict):
    use_vision: Required[bool]
    talk: Required[bool]
    image_source: Literal["webcam", "screen"]
    speech_to_text: Required[SpeechToText]
    text_to_speech: Required[TextToSpeech]
    llm: Required[LLM]


class Monitor(TypedDict):
    top: Required[int]
    left: Required[int]
    width: Required[int]
    height: Required[int]


class VoiceRecorderConfig(TypedDict):
    dynamic_energy_threshold: Required[bool]
    phrase_time_limit: Required[int]


class Codes(TypedDict):
    CARRIAGE_RETURN: Required[Control]
    ERASE_LINE: Required[Control]
    HIDE_CURSOR: Required[Control]
    CURSOR_UP: Required[Control]
