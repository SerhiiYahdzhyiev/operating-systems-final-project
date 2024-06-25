from argparse import ArgumentParser

root_parser = ArgumentParser(
    prog="pssim",
    description="Process Scheduling and Memeory Allocation Simulator"
)

root_parser.add_argument("command", choices=["run", "show-config"])
