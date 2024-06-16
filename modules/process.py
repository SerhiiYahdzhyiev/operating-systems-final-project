from typing import Tuple
from enum import Enum
from random import randint

class ProcessStatus(Enum):
    CREATED = 1,
    READY = 2,
    WAITING = 3,
    EXECUTING = 4,
    FINISED = 5


class Process:
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

    def __repr__(self) -> str:
        repr_str = f"<Process\n\tpid={self.pid}\n\tstatus={self.status.name}" \
                   f"\n\tarrival_time={self.arrival_time}" \
                   f"\n\tburst_time{self.burst_time}\n\tmemory_required={self.memory_required}\n>\n"
        return repr_str


class ProcessFactory:
    __next_pid: int = 1

    __arrival_times_range: Tuple[int, int]  = (1, 100)
    __burst_times_range: Tuple[int, int]  = (1, 15)
    __memory_requirements_range: Tuple[int, int]  = (10, 100)

    @classmethod
    def set_arrival_times_range(cls, new_range: Tuple[int, int]) -> None:
        # TODO: Add specific validations for new range
        cls.__arrival_times_range = new_range

    @classmethod
    def set_burst_times_range(cls, new_range: Tuple[int, int]) -> None:
        # TODO: Add specific validations for new range
        cls.__burst_times_range = new_range

    @classmethod
    def set_memory_requirements_range(cls, new_range: Tuple[int, int]) -> None:
        # TODO: Add specific validations for new range
        cls.__memory_requirements_range = new_range
    
    @classmethod
    def create_process(cls) -> Process:
        arrival_time = randint(*cls.__arrival_times_range)
        burst_time = randint(*cls.__burst_times_range)
        memory_required = randint(*cls.__memory_requirements_range)

        process = Process(
                cls.__next_pid,
                arrival_time,
                burst_time,
                memory_required,
            )

        cls.__next_pid += 1

        return process
