from typing import Tuple
from random import randint

from modules.common.types import Range

from .core import Process
from ..config import process_config as config


class ProcessFactory:
    __next_pid: int = 1

    __arrival_times_range: Range  = (config.range.arrival.start, config.range.arrival.end)
    __burst_times_range: Range  = (config.range.burst.start, config.range.burst.end)
    __memory_requirements_range: Range  = (config.range.memory.start, config.range.memory.end)

    @classmethod
    def set_arrival_times_range(cls, new_range: Range) -> None:
        # TODO: Add specific validations for new range
        cls.__arrival_times_range = new_range

    @classmethod
    def set_burst_times_range(cls, new_range: Range) -> None:
        # TODO: Add specific validations for new range
        cls.__burst_times_range = new_range

    @classmethod
    def set_memory_requirements_range(cls, new_range: Range) -> None:
        # TODO: Add specific validations for new range
        cls.__memory_requirements_range = new_range

    @classmethod
    def create(cls) -> Process:
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
