from abc import ABC, abstractmethod
from typing import List

from pssim.interfaces.memory import IMemory
from pssim.interfaces.process import IProcess


class IUi(ABC):
    @abstractmethod
    def display_processes(self, processes: List[IProcess]):
        ...

    @abstractmethod
    def display_memory(self, memory: IMemory):
        ...
