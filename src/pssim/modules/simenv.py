from asyncio import sleep
from pssim.interfaces.scheduler import ICpu
from pssim.modules.config import sim_config as config
from pssim.modules.process.factory import ProcessFactory
from pssim.modules.scheduler.core import Scheduler
from pssim.modules.tui import UI
from pssim.interfaces.process import IProcess
from pssim.modules.scheduler.strategy import get_scheduling_strategy


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

    while True:
      arrived = arrives.get(self._timer, None)

      if arrived:
        for process in arrived:
          processes.append(process)
        self.scheduler.schedule(arrived)

      current = self.scheduler.get_current()

      if current:
        self.cpu.execute(current)

      self.scheduler.update()
      self._timer += 1
      self.ui.update(self._timer, processes)
      await sleep(self.cpu.cycle_time)
