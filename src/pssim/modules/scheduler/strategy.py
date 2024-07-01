from typing import Optional
from queue import SimpleQueue
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ISchedulingStrategy


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


# TODO: Realize
class RR(BaseStrategy):
  def schedule(
    self,
    process: IProcess,
    current: Optional[IProcess],
  ): ...


get_scheduling_strategy = {
  "FCFS": FCFS,
  "SJF": SJF,
  "SRTF": SRTF,
  "RR": RR,
}
