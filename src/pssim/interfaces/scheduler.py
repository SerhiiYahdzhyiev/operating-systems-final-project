from queue import Queue
from typing import List, Tuple
from abc import ABC, abstractmethod

from pssim.interfaces.memory import IMemoryManager, IMemory
from pssim.interfaces.process import IProcess
from pssim.modules.tui import UI

class ICpu(ABC):
    @abstractmethod
    def execute(self, process: IProcess):
        ...

class ISchedulingStrategy(ABC):
    @abstractmethod
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[Queue, Queue],
    ):
        ...
