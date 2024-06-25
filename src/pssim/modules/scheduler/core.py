from typing import List
from queue import SimpleQueue

from pssim.interfaces.process import IProcess
from pssim.interfaces.memory import IMemoryManager, IMemory
from pssim .interfaces.scheduler import ICpu, ISchedulingStrategy

class Scheduler():
    ready = SimpleQueue()
    waiting = SimpleQueue()

    def __init__(self, strategy: ISchedulingStrategy):
        self.strategy = strategy
        # TODO: Relize queues
        self.queues = (self.ready, self.waiting)

    def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
    ):
        self.strategy.schedule(
            processes,
            cpu,
            mem_manager,
            memory,
            self.queues
        )
