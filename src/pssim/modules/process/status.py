from enum import Enum


class ProcessStatus(Enum):
  CREATED = "CREATED  "
  READY = "READY    "
  WAITING = "WAITING  "
  EXECUTING = "EXECUTING"
  FINISHED = "FINISHED "
