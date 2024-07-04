from typing import List
from asyncio import sleep
from pssim.interfaces.scheduler import ICpu
from pssim.modules.config import sim_config as config
from pssim.modules.process.factory import ProcessFactory
from pssim.modules.scheduler.core import Scheduler
from pssim.modules.tui import UI
from pssim.interfaces.process import IProcess
from pssim.modules.scheduler.strategy import get_scheduling_strategy
from pssim.modules.memory.core import Memory


class CPU(ICpu):
  _cycle_time = 1

  def execute(self, process: IProcess):
    process.execute(self._cycle_time)

  @property
  def cycle_time(self) -> int:
    return self._cycle_time


class SimulationEvironment:
  _num_processes = config["num_processes"]
  _timer = 0

  def __init__(self):
    self.ui = UI()
    _scheduling_strategy = get_scheduling_strategy[
      config["scheduling_strategy"]
    ]()
    self.scheduler = Scheduler(_scheduling_strategy)
    self.cpu = CPU()
    self.memory = Memory()

  async def run(self):
    _processes = []
    for _ in range(self._num_processes):
      _processes.append(ProcessFactory.create())

    arrives = {}

    for process in _processes:
      if not arrives.get(process.arrival_time, False):
        arrives[process.arrival_time] = [process]
      else:
        arrives[process.arrival_time].append(process)

    processes = []
    current: IProcess | None = None

    def set_current(next: IProcess):
      nonlocal current
      current = next

    waiting_for_memory: List[IProcess] = []

    def reschedule():
      scheduled = False
      for process in waiting_for_memory:
        try:
          process.aquire_memory(
            self.memory.allocate(process.memory_required)
          )
          waiting_for_memory.remove(process)
          self.scheduler.schedule(process, current, set_current)
          processes.append(process)
          scheduled = True
        except MemoryError:
          continue
      return scheduled

    while True:
      for p in self.scheduler.waiting:
        p.wait(1)

      for p in waiting_for_memory:
        p.wait(1)
        p.arrival_time += 1

      arrived: List[IProcess] = arrives.get(self._timer, [])

      if arrived:
        for process in arrived:
          try:
            process.aquire_memory(
              self.memory.allocate(process.memory_required)
            )
          except MemoryError:
            waiting_for_memory.append(process)
            continue
          processes.append(process)
          self.scheduler.schedule(process, current, set_current)
          if len(waiting_for_memory):
            reschedule()
      elif len(waiting_for_memory):
        if not (reschedule()):
          self.scheduler.update(current, set_current)
      else:
        self.scheduler.update(current, set_current)

      if current and not current.finished:
        self.cpu.execute(current)
        if current.finished:
          self.memory.deallocate(current.memory)

      self._timer += 1
      self.ui.update(
        self._timer,
        processes,
        self.memory,
      )
      await sleep(self.cpu.cycle_time)
