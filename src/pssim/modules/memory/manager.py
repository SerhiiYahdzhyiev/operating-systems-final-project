from pssim.interfaces.memory import IMemeoryManager, IMemory, IMemoryChunk


class MemeoryManager(IMemeoryManager):
    # TODO: Realize
    def alloc(self, ammount: int, memory: IMemory) -> IMemoryChunk:
        ...

    def delloc(self, chunk: IMemoryChunk, memory: IMemory):
        ...

