from abc import ABC, abstractmethod
from typing import List

from pssim.interfaces.memory import IMemory
from pssim.interfaces.process import IProcess


class IUi(ABC):
  @abstractmethod
  def update(
    self,
    timer: int,
    processes: List[IProcess],
    memory: IMemory,
  ): ...
