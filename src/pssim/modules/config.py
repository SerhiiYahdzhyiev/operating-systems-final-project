import os
import yaml
from pydantic import BaseModel

class SimulatorConfig(BaseModel):
    num_processes: int
    scheduling_strategy: str

class MemoryConfig(BaseModel):
    size: int

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
    process_config = yaml.safe_load(f)

    _ = ProcessConfigModel(**process_config)

with open(f"{config_path}/../config/sim.yaml") as f:
    sim_config = yaml.safe_load(f)

    _ = SimulatorConfig(**sim_config)

with open(f"{config_path}/../config/mem.yaml") as f:
    mem_config = yaml.safe_load(f)

    _ = MemoryConfig(**mem_config)

def show_config():
    print("Simulation\n")
    print(yaml.dump(sim_config))
    print("Memeory\n")
    print(yaml.dump(mem_config))
    print("Process\n")
    print(yaml.dump(process_config))

def dump_configs():
    with open(f"{config_path}/../config/sim.yaml", "w") as f:
        yaml.dump(sim_config, f)
    with open(f"{config_path}/../config/process.yaml", "w") as f:
        yaml.dump(process_config, f)
    with open(f"{config_path}/../config/mem.yaml", "w") as f:
        yaml.dump(mem_config, f)

def _set_config(config: dict, key: str, value: int):
    config[key] = value
    dump_configs()

def set_num_porcesses(value: int):
    assert value > 0
    _set_config(process_config, "num_processes", value)
