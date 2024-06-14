import warnings

warnings.filterwarnings("ignore", r".*audioop.*", category=DeprecationWarning)

import audioop

from rich.status import Status
from speech_recognition import Recognizer
from speech_recognition.audio import AudioData

from .config import get_global_config, get_monitor_config, get_voice_recorder_config
from .utils import ConsoleManager, get_audio_player
from .video_recorder import ScreenRecorder, WebcamRecorder
from .voice_recorder import VoiceRecorder


class Assistant:

    def __init__(self, system_prompt: str):
        config = get_global_config(system_prompt)
        self.use_vision = config.get("use_vision")
        self.talk = config.get("talk")
        self.voice_recorder = VoiceRecorder(**get_voice_recorder_config())
        if self.use_vision:
            self.image_source = (
                WebcamRecorder()
                if config.get("image_source") == "webcam"
                else ScreenRecorder(monitor=get_monitor_config())
            )
        self.speech_to_text = config.get("speech_to_text")
        self.text_to_speech = config.get("text_to_speech")
        self.llm = config.get("llm")

    def _speech_recognition_callback(
        self, recognizer: Recognizer, audio_data: AudioData, status: Status
    ) -> None:
        rms = audioop.rms(audio_data.get_raw_data(), audio_data.sample_width)
        # if it was quiet then return
        if rms < recognizer.energy_threshold:
            return
        try:
            status.update(
                "[bright_yellow]Transcribing...", spinner_style="bright_yellow", speed=2
            )
            ConsoleManager.console().log("Recognized speech", style="bright_black")
            image = None
            if self.use_vision:
                _, image = self.image_source.capture()

            text = self.speech_to_text.transcribe(audio_data)
            status.update(
                "[bright_yellow]Running inference...",
                spinner_style="bright_yellow",
                speed=2,
            )
            ConsoleManager.console().print(
                f"[green]User>[/green] {text}", highlight=False
            )
            response = self.llm.run(text, image, use_vision=self.use_vision)
            ConsoleManager.console().print(
                f"[dark_orange]Assistant>[/dark_orange] {response}", highlight=False
            )

            if self.talk:
                status.update(
                    "[bright_yellow]Getting speach ready...",
                    spinner_style="bright_yellow",
                    speed=2,
                )
                audio = self.text_to_speech.speak(response)
                status.update(
                    "[purple3]Playing audio",
                    spinner="point",
                    spinner_style="purple3",
                    speed=1.2,
                )
                output_stream, player = get_audio_player()
                output_stream.write(audio)
                output_stream.close()
                player.terminate()
        except Exception as e:
            ConsoleManager.console().log("[bold red] An error occured")
            ConsoleManager.console().print(f"[bold red] {e}")
        finally:
            status.update(
                ":studio_microphone: Listening...",
                spinner="dots",
                spinner_style="white",
                speed=2,
            )

    def chat(self) -> None:

        stopper = self.voice_recorder.start_listening(
            callback=self._speech_recognition_callback
        )
        while True:
            if input().strip().lower() in ["q", "quit", "exit"]:
                break

        stopper(wait_for_stop=True)
