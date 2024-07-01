from pssim.interfaces.memory import IAllocationStrategy, IMemory, IMemoryChunk


class FirstFit(IAllocationStrategy):
  # TODO: Realize
  def alloc(self, ammount: int, memory: IMemory) -> IMemoryChunk: ...

  def delloc(self, chunk: IMemoryChunk, memory: IMemory): ...


class BestFit(IAllocationStrategy):
  # TODO: Realize
  def alloc(self, ammount: int, memory: IMemory) -> IMemoryChunk: ...

  def delloc(self, chunk: IMemoryChunk, memory: IMemory): ...
