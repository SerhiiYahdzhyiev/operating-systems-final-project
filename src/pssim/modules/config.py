import os
import yaml
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

def show_config(*args):
    print("============")
    print("Simulation")
    print("============\n")
    print(yaml.dump(sim_config))
    print("============")
    print("Memory")
    print("============\n")
    print(yaml.dump(mem_config))
    print("============")
    print("Process")
    print("============\n")
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

def _set_process_range(key: str, args: list):
    assert len(args) >= 2
    assert int(args[0])
    assert int(args[1])
    assert int(args[0]) > 0
    assert int(args[1]) >= int(args[0])
    _set_config(process_config["range"][key], "start", int(args[0]))
    _set_config(process_config["range"][key], "end", int(args[1]))
    print(f"pssim: set processes {key} range to {args[0]} - {args[1]}")

def set_num_porcesses(args: list):
    assert len(args)
    assert int(args[0])
    assert int(args[0]) > 0
    _set_config(process_config, "num_processes", int(args[0]))
    print(f"pssim: set generate process number to {args[0]}")

def set_memory_allocation_algo(args: list): 
    assert len(args)
    assert args[0] in ["FF", "BF"]
    get_full_algo_name_by = {
            "FF": "First Fit",
            "BF": "Best Fit",
    }
    _set_config(mem_config, "management_strategy", args[0])
    print(f"pssim: set memory alocation strategy to {get_full_algo_name_by[args[0]]}")

def set_scheduling_algo(args: list): 
    assert len(args)
    assert args[0] in ["FCFS", "SJF", "SRTF", "RR"]
    get_full_algo_name_by = {
            "FCFS": "First Come - First Served",
            "SJF": "Shortest Job First",
            "SRTF": "Shortest Remaining Time First",
            "RR": "Round Robin",
    }
    _set_config(sim_config, "scheduling_strategy", args[0])
    print(f"pssim: set scheduling strategy to {get_full_algo_name_by[args[0]]}")

def set_arrival_time_range(args: list):
    _set_process_range("arrival", args)

def set_burst_time_range(args: list):
    _set_process_range("burst", args)

def set_memory_requirements_range(args: list):
    _set_process_range("memory", args)
