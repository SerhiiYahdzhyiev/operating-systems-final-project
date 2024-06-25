from typing import List, Tuple
from queue import Queue
from pssim.interfaces.memory import IMemory, IMemoryManager
from pssim.interfaces.process import IProcess
from pssim.interfaces.scheduler import ICpu, ISchedulingStrategy


# TODO: Realize strategies
class FCFS(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[Queue, Queue]
    ):
        ...

class SJF(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[Queue, Queue]
    ):
        ...

class SRTF(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[Queue, Queue]
    ):
        ...

class RR(ISchedulingStrategy):
    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
        queues: Tuple[Queue, Queue]
    ):
        ...

get_scheduling_strategy = {
    "FCFS": FCFS,
    "SJF": SJF,
    "SRTF": SRTF,
    "RR": RR,
}
