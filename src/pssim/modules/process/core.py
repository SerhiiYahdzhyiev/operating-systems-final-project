from pssim.interfaces.memory import IMemoryChunk
from pssim.interfaces.process import IProcess
from .status import ProcessStatus


class Process(IProcess):
  def __init__(
    self,
    pid: int,
    arrival_time: int,
    burst_time: int,
    memory_required: int,
  ):
    self.pid = pid
    self.arrival_time = arrival_time
    self.burst_time = burst_time
    self.memory_required = memory_required
    self.status = ProcessStatus.CREATED

    self._burst_time_left = self.burst_time
    self._time_waited = 0
    self._time_executed = 0
    self._memory = None

  def __repr__(self) -> str:
    repr_str = (
      f"<Process\n\tpid={self.pid}\n\tstatus={self.status.value}"
      f"\n\tarrival_time={self.arrival_time}"
      f"\n\tburst_time={self.burst_time}\n\tmemory_required={self.memory_required}\n>\n"
    )
    return repr_str

  def __str__(self) -> str:
    _str = (
      f"\t{self.pid}\t{self.status.value}"
      f"\t{self.arrival_time}"
      f"\t{self.burst_time}\t{self._burst_time_left}\t{self._time_waited}\t{self.memory_required}\n"
    )
    return _str

  def execute(self, time: int = 1):
    if self._burst_time_left > 0:
      self.status = ProcessStatus.EXECUTING
      self._burst_time_left -= time
      if self._burst_time_left == 0:
        self.status = ProcessStatus.FINISHED
      self._time_executed += 1

  def wait(self, time: int):
    self.status = ProcessStatus.WAITING
    self._time_waited += time

  def set_ready(self):
    self.status = ProcessStatus.READY

  def set_waiting(self):
    self.status = ProcessStatus.WAITING

  def aquire_memory(self, chunk: IMemoryChunk):
    self._memory = chunk

  @property
  def memory(self) -> IMemoryChunk | None:
    return self._memory

  @property
  def finished(self) -> bool:
    return bool(not self._burst_time_left)

  @property
  def waiting_time(self) -> int:
    return self._time_waited

  @property
  def service_time(self) -> int:
    return self._time_executed
