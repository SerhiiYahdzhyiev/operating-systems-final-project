import yaml
from .loaded import config_path, sim_config, process_config, mem_config


def _set_config(config: dict, key: str, value: int):
  config[key] = value
  dump_configs()


def _set_process_range(key: str, args: list):
  assert len(args) >= 2 or print("pssim: error: arguments list too short")
  assert int(args[0]) or print(
    "pssim: error: first argument should be positive integer"
  )
  assert int(args[1]) or print(
    "pssim: error: second argument should be positive integer"
  )
  assert int(args[0]) > 0 or print(
    "pssim: error: first argument should be positive integer"
  )
  assert int(args[1]) >= int(args[0]) or print(
    "pssim: error: invalid range provided"
  )
  _set_config(process_config["range"][key], "start", int(args[0]))
  _set_config(process_config["range"][key], "end", int(args[1]))
  print(f"pssim: set processes {key} range to {args[0]} - {args[1]}")


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
  with open(f"{config_path}/../../config/sim.yaml", "w") as f:
    yaml.dump(sim_config, f)
  with open(f"{config_path}/../../config/process.yaml", "w") as f:
    yaml.dump(process_config, f)
  with open(f"{config_path}/../../config/mem.yaml", "w") as f:
    yaml.dump(mem_config, f)

def set_memory_size(args: list):
  assert len(args) or print(
    "pssim: error: argument required - positive integer"
  )
  assert int(args[0]) or print(
    "pssim: error: argument should be positive integer"
  )
  assert int(args[0]) > 0 or print(
    "pssim: error: argument should be positive integer"
  )
  _set_config(mem_config, "size", int(args[0]))
  print(f"pssim: set memory size to {args[0]}")


def set_num_processes(args: list):
  assert len(args) or print(
    "pssim: error: argument required - positive integer"
  )
  assert int(args[0]) or print(
    "pssim: error: argument should be positive integer"
  )
  assert int(args[0]) > 0 or print(
    "pssim: error: argument should be positive integer"
  )
  _set_config(sim_config, "num_processes", int(args[0]))
  print(f"pssim: set generate process number to {args[0]}")


def set_memory_allocation_algo(args: list):
  assert len(args) or print(
    "pssim: error: argument required for set-scheduling-algo"
  )
  assert args[0] in ["FF", "BF"] or print(
    "pssim: error: argument should be in ['FF','BF']"
  )
  get_full_algo_name_by = {
    "FF": "First Fit",
    "BF": "Best Fit",
  }
  _set_config(mem_config, "management_strategy", args[0])
  print(
    f"pssim: set memory alocation strategy to {get_full_algo_name_by[args[0]]}"
  )


def set_scheduling_algo(args: list):
  assert len(args) or print(
    "pssim: error: argument required for set-scheduling-algo"
  )
  assert args[0] in ["FCFS", "SJF", "SRTF", "RR"] or print(
    "pssim: error: argument should be in ['FCFS','SJF','SRTF','RR']"
  )
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
