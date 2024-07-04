from typing import Callable, Optional
from abc import ABC, abstractmethod

from pssim.interfaces.process import IProcess


class ICpu(ABC):
  @abstractmethod
  def execute(self, process: IProcess): ...

  @property
  @abstractmethod
  def cycle_time(self) -> int: ...


class ISchedulingStrategy(ABC):
  @abstractmethod
  def schedule(
    self,
    process: IProcess,
    current: IProcess | None,
    set_current: Callable,
  ): ...

  @abstractmethod
  def update(
    self,
    current: Optional[IProcess],
    set_current: Callable,
  ): ...

  @property
  @abstractmethod
  def waiting(self) -> list[IProcess]: ...
