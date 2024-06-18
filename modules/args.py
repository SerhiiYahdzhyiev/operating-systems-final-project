from argparse import ArgumentParser

root_parser = ArgumentParser(
        prog="pssim",
        description="Processes Scheduling and Memory Management Simulator",
        )

root_parser.add_argument("command")
command_parsers = root_parser.add_subparsers(title="commands", dest="command")

run_parser = command_parsers.add_parser("run", help="Runs the simulation")
