from typing import Optional
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ISchedulingStrategy
from pssim.modules.config import process_config


class BaseStrategy(ISchedulingStrategy):
  _waiting = []

  @property
  def waiting(self) -> list[IProcess]:
    return self._waiting

  def update(self, current: IProcess | None, set_current):
    if len(self.waiting):
      next = self.waiting[0]
      if not current or current.finished:
        self.waiting.remove(next)
        next.set_ready()
        set_current(next)


class FCFS(BaseStrategy):
  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    set_current,
  ):
    if current and not current.finished:
      process.set_waiting()
      self.waiting.append(process)
      return

    next = process
    if len(self.waiting):
      next = self.waiting[0]
      self.waiting.remove(next)
      process.set_waiting()
      self.waiting.append(process)

    next.set_ready()
    set_current(next)


class SJF(BaseStrategy):
  def update(self, current: IProcess | None, set_current):
    self.waiting.sort(key=lambda p: p.burst_time)
    super().update(current, set_current)

  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    set_current,
  ):
    if current and not current.finished:
      process.set_waiting()
      self.waiting.append(process)
      return

    next = process
    if len(self.waiting):
      self.waiting.sort(key=lambda p: p.burst_time)
      next = self.waiting[0]
      self.waiting.remove(next)
      process.set_waiting()
      self.waiting.append(process)

    next.set_ready()
    set_current(next)


class SRTF(BaseStrategy):
  def update(self, current: IProcess | None, set_current):
    next = None
    if len(self.waiting):
      self.waiting.sort(key=lambda p: p._burst_time_left)
      next = self.waiting[0]

    if next:
      if not current or current.finished:
        self.waiting.remove(next)
        set_current(next)
        return
      if current._burst_time_left > next._burst_time_left:
        current.set_waiting()
        self.waiting.append(current)
        self.waiting.remove(next)
        set_current(next)

  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    set_current,
  ):
    process.set_waiting()
    self.waiting.append(process)
    self.waiting.sort(key=lambda p: p._burst_time_left)
    next = self.waiting[0]

    if not current or current.finished:
      self.waiting.remove(next)
      set_current(next)
      return

    if current._burst_time_left > next._burst_time_left:
      current.set_waiting()
      self.waiting.append(current)
      self.waiting.remove(next)
      set_current(next)


class RR(BaseStrategy):
  _time_quantum: int = round(
    (
      process_config["range"]["burst"]["end"]
      - process_config["range"]["burst"]["start"]
    )
    / 2
  )

  def update(self, current: IProcess | None, set_current):
    if len(self.waiting):
      next = self.waiting[0]

      if not current or current.finished:
        self.waiting.remove(next)
        next.set_ready()
        set_current(next)
        return

      if current.service_time % self._time_quantum == 0:
        current.set_waiting()
        self.waiting.append(current)
        self.waiting.remove(next)
        next.set_ready()
        set_current(next)

  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    set_current,
  ):
    if not current or current.finished:
      if not len(self.waiting):
        process.set_ready()
        set_current(process)
        return
      process.set_waiting()
      self.waiting.append(process)
      next = self.waiting[0]
      self.waiting.remove(next)
      next.set_ready()
      set_current(next)
      return

    self.waiting.append(process)

    if current.service_time % self._time_quantum == 0:
      next = self.waiting[0]
      self.waiting.remove(next)
      current.set_waiting()
      self.waiting.append(current)
      next.set_ready()
      set_current(next)


get_scheduling_strategy = {
  "FCFS": FCFS,
  "SJF": SJF,
  "SRTF": SRTF,
  "RR": RR,
}
