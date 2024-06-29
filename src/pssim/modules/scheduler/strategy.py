from asyncio import sleep
from typing import List, Tuple
from queue import SimpleQueue
from pssim.interfaces.memory import IMemory, IMemoryManager
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ICpu, ISchedulingStrategy
from pssim.interfaces.ui import IUi

class BaseStrategy(ISchedulingStrategy):
    def __init__(self, ui: IUi):
        self.ui = ui


# TODO: Realize strategies
class FCFS(BaseStrategy):
    async def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[SimpleQueue, SimpleQueue]
    ):
        sorted_ = list(sorted(processes, key=lambda p: p.arrival_time))

        for process in sorted_:
            process.set_ready()
            queues[0].put(process)

        while not queues[0].empty():
            process = queues[0].get()
            while not process.finished:
                cpu.execute(process);
                await sleep(cpu.cycle_time)
                self.ui.display_processes(processes)



class SJF(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[SimpleQueue, SimpleQueue]
    ):
        ...

class SRTF(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[SimpleQueue, SimpleQueue]
    ):
        ...

class RR(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[SimpleQueue, SimpleQueue]
    ):
        ...

get_scheduling_strategy = {
    "FCFS": FCFS,
    "SJF": SJF,
    "SRTF": SRTF,
    "RR": RR,
}
