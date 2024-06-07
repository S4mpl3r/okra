import os
import wave
from threading import Lock, Thread

from pyaudio import PyAudio, Stream, paInt16
from rich.console import Console
from rich.control import Control
from rich.segment import ControlType
from rich.status import Status

from ..types import Codes

codes: Codes = {
    "CARRIAGE_RETURN": Control(ControlType.CARRIAGE_RETURN),
    "ERASE_LINE": Control((ControlType.ERASE_IN_LINE, 2)),
    "HIDE_CURSOR": Control(ControlType.HIDE_CURSOR),
    "CURSOR_UP": Control((ControlType.CURSOR_UP, 1)),
}


class WavePlayer(Thread):
    CHUNK = 1024

    def __init__(self, filepath, loop=True, **kwargs):
        super(WavePlayer, self).__init__(**kwargs)
        self.filepath = os.path.abspath(filepath)
        self.loop = loop

    def run(self):
        player = PyAudio()
        with wave.open(self.filepath, "rb") as wf:
            stream = player.open(
                format=player.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )

            # PLAYBACK LOOP
            data = wf.readframes(self.CHUNK)
            while self.loop:
                stream.write(data)
                data = wf.readframes(self.CHUNK)
                if data == b"":  # If file is over then rewind.
                    wf.rewind()
                    data = wf.readframes(self.CHUNK)

        stream.close()
        player.terminate()

    def stop(self):
        self.loop = False


class _SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class _ConsoleWrapper(metaclass=_SingletonMeta):
    console: Console = None

    def __init__(self) -> None:
        self.console = Console()

    def get_console(self) -> Console:
        return self.console

    def get_status(self, *args, **kwargs) -> Status:
        return self.console.status(*args, **kwargs)


class ConsoleManager:
    @staticmethod
    def console() -> Console:
        return _ConsoleWrapper().get_console()

    @staticmethod
    def status(*args, **kwargs) -> Status:
        return _ConsoleWrapper().get_status(*args, **kwargs)


def get_audio_player() -> tuple[Stream, PyAudio]:
    player = PyAudio()
    stream = player.open(format=paInt16, channels=1, rate=24000, output=True)
    return stream, player
