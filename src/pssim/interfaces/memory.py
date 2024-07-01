from abc import abstractmethod, ABC


class IMemoryChunk(ABC):
  @property
  @abstractmethod
  def size(self) -> int: ...

  @property
  @abstractmethod
  def start(self) -> int: ...

  @property
  @abstractmethod
  def end(self) -> int: ...

class IMemory(ABC):
  @property
  @abstractmethod
  def size(self) -> int: ...

  @property
  @abstractmethod
  def free(self) -> int: ...

  @abstractmethod
  def allocate(self, size: int) -> IMemoryChunk: ...
  def dealocate(self, chunk: IMemoryChunk): ...


class IAllocationStrategy(ABC):
  @abstractmethod
  def alloc(self, ammount: int, memory: IMemory) -> IMemoryChunk: ...

  @abstractmethod
  def dealloc(self, chunk: IMemoryChunk, memory: IMemory): ...


class IMemoryManager(ABC):
  @abstractmethod
  def alloc(self, ammount: int, memory: IMemory) -> IMemoryChunk: ...

  @abstractmethod
  def dealloc(self, chunk: IMemoryChunk, memeory: IMemory): ...
