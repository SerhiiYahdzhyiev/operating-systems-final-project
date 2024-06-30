from abc import ABC, abstractmethod
from typing import List

from pssim.interfaces.process import IProcess


class IUi(ABC):
    @abstractmethod
    def update(self, timer: int, processes: List[IProcess]):
        ...
