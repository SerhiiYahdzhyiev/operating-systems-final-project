from enum import Enum

class ProcessStatus(Enum):
    CREATED = 1,
    READY = 2,
    WAITING = 3,
    EXECUTING = 4,
    FINISHED = 5


