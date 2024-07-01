from typing import List
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ISchedulingStrategy


class Scheduler:
  _current: IProcess | None = None

  def __init__(self, strategy: ISchedulingStrategy):
    self.strategy = strategy

  def update(self):
    self.strategy.update(self._current, set_current=self.set_current())

  def schedule(
    self,
    processes: List[IProcess],
  ):
    current = self.get_current()
    for process in processes:
      self.strategy.schedule(process, current, set_current=self.set_current())

  def get_current(self) -> IProcess | None:
    if not self._current:
      if self.strategy.ready.empty():
        self._current = None
      else:
        self._current = self.strategy.ready.get()
    else:
      if self._current.finished:
        if self.strategy.ready.empty():
          self._current = None
        else:
          self._current = self.strategy.ready.get()

    return self._current

  def set_current(self):
    def callback(process):
      self._current = process

    return callback
