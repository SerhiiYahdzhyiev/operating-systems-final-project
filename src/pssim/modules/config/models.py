from pydantic import BaseModel


class SimulatorConfig(BaseModel):
  num_processes: int
  scheduling_strategy: str


class MemoryConfig(BaseModel):
  size: int
  management_strategy: str


class RangeModel(BaseModel):
  start: int
  end: int


class ProcessRangesModel(BaseModel):
  arrival: RangeModel
  burst: RangeModel
  memory: RangeModel


class ProcessConfigModel(BaseModel):
  range: ProcessRangesModel
