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
        self.queues = (self.ready, self.waiting)

    async def schedule(
        self,
        processes: List[IProcess],
        cpu: ICpu,
        mem_manager: IMemoryManager,
        memory: IMemory,
    ):
        await self.strategy.schedule(
            processes,
            cpu,
            mem_manager,
            memory,
            self.queues,
        )

