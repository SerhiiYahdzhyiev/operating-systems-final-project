from pssim.interfaces.memory import IMemory, IMemoryChunk
from pssim.modules.config import mem_config as config


class MemoryChunk(IMemoryChunk):
  _start: int
  _end: int
  _size: int

  def __init__(self, start: int, end: int):
    self._start = start
    self._end = end
    self._size = end - start

  @property
  def size(self) -> int:
    return self._size

  @property
  def start(self) -> int:
    return self._start

  @property
  def end(self) -> int:
    return self._end


class Memory(IMemory):
  _size: int = config["size"]
  _free: int = config["size"]
  _mem = []

  def __init__(self):
    self._free_chunks = [MemoryChunk(0, self._size)]

  @property
  def size(self) -> int:
    return self._size

  @property
  def free(self) -> int:
    return self._free

  def allocate(self, size: int) -> IMemoryChunk:
    if size > self.free:
      raise MemoryError("Not enough memory to allocate!")
    if config["management_strategy"] == "FF":
      return self._first_fit_allocate(size)
    elif config["management_strategy"] == "BF":
      return self._best_fit_allocate(size)
    else:
      raise ValueError("Unknown memory management strategy")

  def _first_fit_allocate(self, size: int) -> IMemoryChunk:
    for chunk in self._free_chunks:
      if chunk.size >= size:
        allocated_chunk = MemoryChunk(chunk.start, chunk.start + size)
        chunk._start += size
        if chunk.size == 0:
          self._free_chunks.remove(chunk)
        self._free -= size
        return allocated_chunk
    raise MemoryError("Not enough memory to allocate")

  def _best_fit_allocate(self, size: int) -> IMemoryChunk:
    best_chunk = None
    for chunk in self._free_chunks:
      if chunk.size >= size and (
        best_chunk is None or chunk.size < best_chunk.size
      ):
        best_chunk = chunk
    if best_chunk is not None:
      allocated_chunk = MemoryChunk(best_chunk.start, best_chunk.start + size)
      best_chunk._start += size
      if best_chunk.size == 0:
        self._free_chunks.remove(best_chunk)
      self._free -= size
      return allocated_chunk
    raise MemoryError("Not enough memory to allocate")

  def deallocate(self, chunk: IMemoryChunk):
    position = 0
    for i, free_chunk in enumerate(self._free_chunks):
      if free_chunk.start > chunk.end:
        position = i
        break
    else:
      position = len(self._free_chunks)

    self._free_chunks.insert(position, MemoryChunk(chunk.start, chunk.end))
    self._free += chunk.size

    self._merge_free_chunks()

  def _merge_free_chunks(self):
    merged_chunks = []
    previous_chunk = None
    for chunk in self._free_chunks:
      if previous_chunk is None:
        previous_chunk = chunk
      else:
        if previous_chunk.end == chunk.start:
          previous_chunk._end = chunk.end
        else:
          merged_chunks.append(previous_chunk)
          previous_chunk = chunk
    if previous_chunk is not None:
      merged_chunks.append(previous_chunk)
    self._free_chunks = merged_chunks
