import curses

from asyncio import run

from pssim.modules.args import root_parser
from pssim.modules.config import show_config
from pssim.modules.simenv import SimulationEvironment


async def main():
    # TODO: Realize proper mechanism to config the simulation
    args = root_parser.parse_args()

    if args.command == "show-config":
        show_config()

    if args.command == "run":
        simenv = SimulationEvironment()
        await simenv.run()

def run_main():
    try:
        run(main())
    except KeyboardInterrupt:
        # TODO: Extend gracefull exit (if needed)
        curses.endwin()
        print("Exitting...")
        exit(0)

if __name__ == "__main__":
    run_main()
