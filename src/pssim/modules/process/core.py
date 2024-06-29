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

    def __repr__(self) -> str:
        repr_str = f"<Process\n\tpid={self.pid}\n\tstatus={self.status.value}" \
                   f"\n\tarrival_time={self.arrival_time}" \
                   f"\n\tburst_time={self.burst_time}\n\tmemory_required={self.memory_required}\n>\n"
        return repr_str

    def __str__(self) -> str:
        _str = f"\t{self.pid}\t{self.status.value}" \
                   f"\t{self.arrival_time}" \
                   f"\t{self._burst_time_left}\t{self.memory_required}\n"
        return _str

    def execute(self, time: int = 1):
        if (self._burst_time_left > 0):
            self.status = ProcessStatus.EXECUTING
            self._burst_time_left -= time
            if self._burst_time_left == 0:
                self.status = ProcessStatus.FINISHED

    def wait(self, time: int):
        self.status = ProcessStatus.WAITING
        self._time_waited += time

    def set_ready(self):
        self.status = ProcessStatus.READY

    @property
    def finished(self) -> bool:
        return bool(not self._burst_time_left)
