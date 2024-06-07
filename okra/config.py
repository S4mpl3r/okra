from .llm import Gemini, GroqLLM
from .speech import DeepgramTextToSpeech, GroqSpeechToText
from .types import GlobalConfig, Monitor, VoiceRecorderConfig


def get_global_config(system_prompt: str) -> GlobalConfig:
    """The main configuration for the assistant"""
    config: GlobalConfig = {
        "use_vision": True,
        "talk": True,
        "image_source": "screen",
        "llm": Gemini(
            model_name="models/gemini-1.5-flash-latest",
            system_prompt=system_prompt,
        ),
        "speech_to_text": GroqSpeechToText(),
        "text_to_speech": DeepgramTextToSpeech(),
    }
    return config


def get_voice_recorder_config() -> VoiceRecorderConfig:
    """
    This config has two parameters:
    - dynamic_energy_threshold (bool): Determines if the voice recognition library should dynamically adjust for noise in each run or not.
    - phrase_time_limit (int | None): Max number of seconds that the voice recorder will record your voice. If None, it will record as long as you speak.
    """
    config: VoiceRecorderConfig = {
        "dynamic_energy_threshold": False,
        "phrase_time_limit": 10,
    }
    return config


def get_monitor_config() -> Monitor:
    """Your monitor resolution goes here, by default, we assume it's full-hd"""
    config: Monitor = {
        "top": 0,
        "left": 0,
        "width": 1920,
        "height": 1080,
    }
    return config
