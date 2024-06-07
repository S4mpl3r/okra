from abc import ABC, abstractmethod

from numpy import dtype, ndarray, uint8
from typing_extensions import Any


class LLM(ABC):

    @abstractmethod
    def run(
        self,
        text: str,
        image: ndarray[Any, dtype[uint8]],
        use_vision: bool = True,
    ) -> str:
        pass
