import cv2
import numpy as np
from numpy import dtype, ndarray, uint8
from typing_extensions import Any


class WebcamRecorder:
    """This class handles everything related to webcam"""

    def __init__(self, webcam_index: int = 0):
        self.webcam_index = webcam_index

    def capture(self) -> tuple[ndarray, ndarray[Any, dtype[uint8]]]:
        """
        Captures a webcam image and returns it

        Returns:
            image, data (tuple): image is the captured image in np.array format, data is the image array in jpeg format
        """
        cap = cv2.VideoCapture(self.webcam_index)
        ret, frame = cap.read()
        cap.release()
        _, data = cv2.imencode(".jpeg", np.array(frame))
        return np.array(frame), data
