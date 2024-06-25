import curses

from asyncio import sleep, run

from pssim.modules.args import root_parser
from pssim.modules.process.factory import ProcessFactory
from pssim.modules.tui import UI


# TODO: Decompose, customize, rewrite, refactor...
async def main():
    # TODO: Realize proper mechanism to config the simulation
    args = root_parser.parse_args()

    ui = UI()

    processes = []

    for _ in range(10):
        processes.append(ProcessFactory.create())

    while (True):
        for process in processes:
            process.execute()
        ui.display_processes(processes)
        await sleep(1)

def run_main():
    try:
        run(main())
    except KeyboardInterrupt:
        curses.endwin()
        # TODO: Extend gracefull exit (if needed)

if __name__ == "__main__":
    run_main()
