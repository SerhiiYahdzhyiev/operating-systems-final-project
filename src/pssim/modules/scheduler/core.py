from typing import Callable
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ISchedulingStrategy


class Scheduler:
  def __init__(self, strategy: ISchedulingStrategy):
    self.strategy = strategy

  def update(self, current: IProcess | None, set_current):
    self.strategy.update(current, set_current)

  def schedule(
    self,
    process: IProcess,
    current: IProcess | None,
    set_current: Callable,
  ):
    self.strategy.schedule(process, current, set_current)

  @property
  def waiting(self) -> list[IProcess]:
    return self.strategy.waiting
