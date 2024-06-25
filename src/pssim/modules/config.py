import os
import yaml
from pydantic import BaseModel

class RangeModel(BaseModel):
    start: int
    end: int

class ProcessRangesModel(BaseModel):
    arrival: RangeModel
    burst: RangeModel
    memory: RangeModel

class ProcessConfigModel(BaseModel):
    range: ProcessRangesModel

config_path = os.path.dirname(os.path.abspath(__file__))

with open(f"{config_path}/../config/process.yaml") as f:
    raw_yaml_conf = yaml.safe_load(f)

    process_config = ProcessConfigModel(**raw_yaml_conf)
