from argparse import ArgumentParser

root_parser = ArgumentParser(
  prog="pssim",
  description="Process Scheduling and Memeory Allocation Simulator.",
)

root_parser.add_argument(
  "command",
  choices=[
    "run",
    "show-config",
    "set-num-processes",
    "set-burst-time-range",
    "set-arrival-time-range",
    "set-memory-requirements-range",
    "set-scheduling-algo",
    "set-memory-allocation-algo",
    "set-memory-size",
  ],
  help="Run a pssim command.",
)

root_parser.add_argument("arguments", nargs="*", help="Commands' arguments.")
