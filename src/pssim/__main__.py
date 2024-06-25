import curses

from asyncio import run

from pssim.modules.args import root_parser
from pssim.modules.config import show_config
from pssim.modules.simenv import SimulationEvironment

simenv = SimulationEvironment()

# TODO: Decompose, customize, rewrite, refactor...
async def main():
    # TODO: Realize proper mechanism to config the simulation
    args = root_parser.parse_args()

    if args.command == "show-config":
        show_config()
        exit(0)

    if args.command == "run":
        await simenv.run()

def run_main():
    try:
        run(main())
    except KeyboardInterrupt:
        curses.endwin()
        # TODO: Extend gracefull exit (if needed)

if __name__ == "__main__":
    run_main()
