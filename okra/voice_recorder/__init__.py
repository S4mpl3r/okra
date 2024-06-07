import threading

from rich.status import Status
from speech_recognition import AudioSource, Microphone, Recognizer
from speech_recognition.audio import AudioData
from speech_recognition.exceptions import WaitTimeoutError
from typing_extensions import Callable

from ..utils import ConsoleManager


class VoiceRecorder:
    """This class handles voice recognition and recording"""

    def __init__(
        self,
        dynamic_energy_threshold: bool = False,
        phrase_time_limit: int = 10,
    ):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.dynamic_energy_threshold = dynamic_energy_threshold
        self.phrase_time_limit = phrase_time_limit

    def _listen_in_background(
        self,
        source: AudioSource,
        callback: Callable[[Recognizer, AudioData, Status], None],
        phrase_time_limit: int | None = None,
    ):
        """
        Spawns a thread to repeatedly record phrases from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance and call ``callback`` with that ``AudioData`` instance as soon as each phrase are detected.

        Returns a function object that, when called, requests that the background listener thread stop. The background thread is a daemon and will not stop the program from exiting if there are no other non-daemon threads. The function accepts one parameter, ``wait_for_stop``: if truthy, the function will wait for the background listener to stop before returning, otherwise it will return immediately and the background listener thread might still be running for a second or two afterwards. Additionally, if you are using a truthy value for ``wait_for_stop``, you must call the function from the same thread you originally called ``listen_in_background`` from.

        Phrase recognition uses the exact same mechanism as ``recognizer_instance.listen(source)``. The ``phrase_time_limit`` parameter works in the same way as the ``phrase_time_limit`` parameter for ``recognizer_instance.listen(source)``, as well.

        The ``callback`` parameter is a function that should accept two parameters - the ``recognizer_instance``, and an ``AudioData`` instance representing the captured audio. Note that ``callback`` function will be called from a non-main thread.
        """
        assert isinstance(source, AudioSource), "Source must be an audio source"
        running = [True]

        def threaded_listen():
            with source as s:
                with ConsoleManager.status(
                    ":studio_microphone: Listening...",
                    spinner_style="bright_black",
                    speed=2,
                ) as status:
                    while running[0]:
                        try:  # listen for 1 second, then check again if the stop function has been called
                            audio = self.recognizer.listen(s, 1, phrase_time_limit)
                        except WaitTimeoutError:  # listening timed out, just try again
                            pass
                        else:
                            if running[0]:
                                callback(self.recognizer, audio, status)

        def stopper(wait_for_stop=True):
            running[0] = False
            if wait_for_stop:
                listener_thread.join()  # block until the background thread is done, which can take around 1 second

        listener_thread = threading.Thread(target=threaded_listen)
        listener_thread.daemon = True
        listener_thread.start()
        return stopper

    def start_listening(
        self, callback: Callable[[Recognizer, AudioData, Status], None]
    ) -> Callable[[bool], None]:
        with ConsoleManager.status(
            "[green]Adjusting for ambient noise...", spinner="dots4", speed=2
        ) as _:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            self.recognizer.energy_threshold = int(
                self.recognizer.energy_threshold * 2.5
            )
            self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold

        ConsoleManager.console().log(
            f"Set minimum energy threshold to [u]{self.recognizer.energy_threshold}[/u]",
            style="bright_black",
            highlight=False,
        )

        stop_listening = self._listen_in_background(
            self.microphone,
            callback,
            phrase_time_limit=self.phrase_time_limit,
        )
        return stop_listening
