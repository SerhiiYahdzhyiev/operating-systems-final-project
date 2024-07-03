import os

from .models import MemoryConfig, ProcessConfigModel, SimulatorConfig
from .helpers import load_config

config_path = os.path.dirname(os.path.abspath(__file__))

process_config = load_config(
  f"{config_path}/../../config/process.yaml", ProcessConfigModel
)
sim_config = load_config(
  f"{config_path}/../../config/sim.yaml", SimulatorConfig
)
mem_config = load_config(f"{config_path}/../../config/mem.yaml", MemoryConfig)
