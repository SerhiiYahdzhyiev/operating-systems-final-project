import curses
import re

from typing import List

from pssim.interfaces.process import IProcess
from pssim.interfaces.ui import IUi
from pssim.modules.config import sim_config


class UI(IUi):
    __process_table_header = f"\tPID\tSTATUS\t\tARRIVED\tBTIME\tLEFT\tWAITED\tMEMORY\n"

    def __init__(self):
        self._screen = curses.initscr()
        self._height, self._width = self._screen.getmaxyx()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(
            curses.COLOR_RED,
            curses.COLOR_RED,
            curses.COLOR_BLACK
        )
        curses.init_pair(
            curses.COLOR_GREEN,
            curses.COLOR_GREEN,
            curses.COLOR_BLACK,
        )
        curses.init_pair(
            curses.COLOR_YELLOW,
            curses.COLOR_YELLOW,
            curses.COLOR_BLACK,
        )
        curses.init_pair(
            curses.COLOR_CYAN,
            curses.COLOR_CYAN,
            curses.COLOR_BLACK,
        )
        # TODO: Setup rest of colors
        self._screen.keypad(True)


    def update(self, timer: int, processes: List[IProcess]):
        self._screen.clear()
        self._screen.addstr(0, 0, f"Scheduling Algorithm: {sim_config["scheduling_strategy"]}")
        self._screen.addstr(1, 0, f"Processes: {sim_config["num_processes"]}")
        self._screen.addstr(2, 0, f"Time: {timer}")
        self._screen.addstr(3, 0, "\n", curses.A_REVERSE)
        self._screen.addstr(4, 0, self.__process_table_header, curses.A_REVERSE)

        for process in processes:
            self._addstr(str(process))

        self._screen.addstr(int(self._height - 4), 0, "Footer mock: 5")
        self._screen.addstr(int(self._height - 3), 0, "Footer mock2: 10")
        self._screen.addstr(int(self._height - 2), 0, "\n")
        self._screen.addstr(int(self._height - 1), 0, "PRESS CTRL+C TO TERMINATE", curses.A_REVERSE)
        self._screen.refresh()

    def _addstr(self, str_: str):
        colors = {
            "CREATED": curses.COLOR_WHITE,
            "READY": curses.COLOR_RED,
            "WAITING": curses.COLOR_CYAN,
            "EXECUTING": curses.COLOR_YELLOW,
            "FINISHED": curses.COLOR_GREEN,
        }
        pattern: str = r'({0:s})'.format(
                '|'.join(r'\b{0:s}\b'.format(word) for word in colors.keys())
                )
        chars: list[str] = re.split(pattern, str_)
        for c in chars:
            self._screen.addstr(c,curses.color_pair(colors.get(c, 0)))
