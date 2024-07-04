import curses

from asyncio import run

from pssim.modules.args import root_parser
from pssim.modules.config.commands import (
  show_config,
  set_num_processes,
  set_burst_time_range,
  set_arrival_time_range,
  set_memory_requirements_range,
  set_scheduling_algo,
  set_memory_allocation_algo,
  set_memory_size,
)
from pssim.modules.simenv import SimulationEvironment


async def run_():
  simenv = SimulationEvironment()
  await simenv.run()


get_action_by = {
  "show-config": show_config,
  "set-num-processes": set_num_processes,
  "set-burst-time-range": set_burst_time_range,
  "set-arrival-time-range": set_arrival_time_range,
  "set-memory-requirements-range": set_memory_requirements_range,
  "set-scheduling-algo": set_scheduling_algo,
  "set-memory-allocation-algo": set_memory_allocation_algo,
  "set-memory-size": set_memory_size,
}


async def main():
  args = root_parser.parse_args()

  if args.command == "run":
    await run_()
    return

  try:
    get_action_by[args.command](args.arguments or None)
  except AssertionError:
    pass


def run_main():
  try:
    run(main())
  except KeyboardInterrupt:
    curses.endwin()
    print("Exitting...")
    exit(0)


if __name__ == "__main__":
  run_main()
