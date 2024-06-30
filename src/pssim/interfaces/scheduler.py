from queue import SimpleQueue
from typing import Optional
from abc import ABC, abstractmethod

from pssim.interfaces.process import IProcess


class ICpu(ABC):
    @abstractmethod
    def execute(self, process: IProcess):
        ...

    @property
    @abstractmethod
    def cycle_time(self) -> int:
        ...


class ISchedulingStrategy(ABC):
    @abstractmethod
    def schedule(
        self,
        process: IProcess,
        current: Optional[IProcess],
    ):
        ...

    @abstractmethod
    def update(
        self,
        current: Optional[IProcess],
    ):
        ...

    @property
    @abstractmethod
    def ready(self) -> SimpleQueue:
        ...

    @property
    @abstractmethod
    def waiting(self) -> SimpleQueue:
        ...
