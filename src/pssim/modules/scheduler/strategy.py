from typing import Optional
from queue import SimpleQueue
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ISchedulingStrategy
from pssim.modules.config import process_config


class BaseStrategy(ISchedulingStrategy):
  _ready = SimpleQueue()
  _waiting_queue = SimpleQueue()

  _waiting = []

  @property
  def ready(self) -> SimpleQueue:
    return self._ready

  @property
  def waiting(self) -> SimpleQueue:
    return self._waiting_queue

  def update(self, current: IProcess | None, **kwargs):
    if not self.waiting.empty():
      for p in self._waiting:
        p.wait(1)

    if not current:
      if not self.waiting.empty():
        next = self._waiting_queue.get()
        self._waiting.remove(next)
        next.set_ready()
        self.ready.put(next)


class FCFS(BaseStrategy):
  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    **kwargs,
  ):
    if not current or current.finished:
      if not self.waiting.empty():
        next = self.waiting.get()
        self._waiting.remove(next)
        next.set_ready()
        self.ready.put(next)
        process.set_waiting()
        self.waiting.put(process)
        self._waiting.append(process)
        return
      process.set_ready()
      self.ready.put(process)
      return
    process.set_waiting()
    self.waiting.put(process)
    self._waiting.append(process)


class SJF(BaseStrategy):
  def update(self, current: IProcess | None, **kwargs):
    if len(self._waiting):
      for p in self._waiting:
        p.wait(1)

    if not current:
      if len(self._waiting):
        self._waiting.sort(reverse=True, key=lambda p: p.burst_time)
        next = self._waiting[-1]
        self._waiting.remove(next)
        next.set_ready()
        self.ready.put(next)

  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    **kwargs,
  ):
    if not current or current.finished:
      if len(self._waiting):
        self._waiting.sort(reverse=True, key=lambda p: p.burst_time)
        next = self._waiting[-1]
        self._waiting.remove(next)
        next.set_ready()
        self.ready.put(next)
        process.set_waiting()
        self._waiting.append(process)
        return
      process.set_ready()
      self.ready.put(process)
      return
    process.set_waiting()
    self._waiting.append(process)


class SRTF(BaseStrategy):
  def update(self, current: IProcess | None, **kwargs):
    self._waiting.sort(reverse=True, key=lambda p: p._burst_time_left)
    if len(self._waiting):
      next = self._waiting[-1]
      if not current:
        self._waiting.remove(next)
        next.set_ready()
        self.ready.put(next)
      else:
        if next._burst_time_left < current._burst_time_left:
          kwargs.get("set_current", lambda x: ...)(next)
          self.ready.put(next)
          self._waiting.remove(next)
          current.set_waiting()
          self._waiting.append(current)
    for p in self._waiting:
      p.wait(1)

  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    **kwargs,
  ):
    if not current or current.finished:
      if len(self._waiting):
        self._waiting.sort(reverse=True, key=lambda p: p._burst_time_left)
        next = self._waiting[-1]
        self._waiting.remove(next)
        next.set_ready()
        self.ready.put(next)
        process.set_waiting()
        self._waiting.append(process)
        return
      process.set_ready()
      self.ready.put(process)
      return
    if len(self._waiting):
      self._waiting.sort(reverse=True, key=lambda p: p._burst_time_left)
      next = self._waiting[-1]
      if next._burst_time_left < current._burst_time_left:
        kwargs.get("set_current", lambda x: ...)(next)
        self.ready.put(next)
        current.set_waiting()
        self._waiting.append(current)
    process.set_waiting()
    self._waiting.append(process)


class RR(BaseStrategy):
  _time_quantum: int = round(
    (
      process_config["range"]["burst"]["end"]
      - process_config["range"]["burst"]["start"]
    )
    / 2
  )

  def update(self, current: IProcess | None, **kwargs):
    if len(self._waiting):
      for p in self._waiting:
        p.wait(1)

    if not current:
      if self.ready.empty():
        return
      next = self.ready.get()
      if next in self._waiting:
        self._waiting.remove(next)
      kwargs.get("set_current", lambda x: ...)(next)
      return

    if current.finished:
      if self.ready.empty():
        kwargs.get("set_current", lambda x: ...)(None)
        return
      next = self.ready.get()
      kwargs.get("set_current", lambda x: ...)(next)
      if next in self._waiting:
        self._waiting.remove(next)
      return

    if current.service_time % self._time_quantum == 0:
      if not self.ready.empty():
        next = self.ready.get()
        kwargs.get("set_current", lambda x: ...)(next)
        current.set_ready()
        self._waiting.append(current)
        self.ready.put(current)

  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
    **kwargs,
  ):
    process.set_ready()
    self.ready.put(process)
    if (
      current
      and not current.finished
      and not current.service_time % self._time_quantum == 0
    ):
      self._waiting.append(process)


get_scheduling_strategy = {
  "FCFS": FCFS,
  "SJF": SJF,
  "SRTF": SRTF,
  "RR": RR,
}
