import cv2
import numpy as np
from mss import mss
from numpy import dtype, ndarray, uint8
from typing_extensions import Any

from ..types import Monitor


class ScreenRecorder:
    """This class handles everything related to screen recording"""

    def __init__(self, monitor: Monitor):
        self.monitor = monitor

    def capture(self) -> tuple[ndarray, ndarray[Any, dtype[uint8]]]:
        """
        Captures a screenshot and returns it

        Returns:
            image, data (tuple): image is the captured image in np.array format, data is the image array in jpeg format
        """
        with mss() as sct:
            screen = sct.grab(self.monitor)
        _, data = cv2.imencode(".jpeg", np.array(screen))
        return np.array(screen), data
