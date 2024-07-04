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

  @abstractmethod
  def deallocate(self, chunk: IMemoryChunk): ...
