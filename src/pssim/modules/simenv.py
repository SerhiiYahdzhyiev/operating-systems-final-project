import asyncio
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
    # TODO: Realize
    pass

    def execute(self, process: IProcess):
        process.execute(self._cycle_time)


class SimulationEvironment:
    _num_processes = config["num_processes"] 

    _scheduling_strategy = get_scheduling_strategy[config["scheduling_strategy"]]()

    def __init__(self):
        self.ui = UI()
        self.shcheduler = Scheduler(self._scheduling_strategy)
        self.cpu = CPU()

    async def run(self): 
        processes = []
        for _ in range(self._num_processes):
            processes.append(ProcessFactory.create())

        while (True):
            for process in processes:
                self.cpu.execute(process)
            self.ui.display_processes(processes)
            await sleep(1)
