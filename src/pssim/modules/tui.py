import curses
import re

from typing import List

from pssim.interfaces.process import IProcess
from pssim.interfaces.ui import IUi
from pssim.modules.config import sim_config, process_config, mem_config


class UI(IUi):
  __process_table_header = (
    "\tPID\tSTATUS\t\tARRIVED\tBTIME\tLEFT\tWAITED\tMEMORY\n"
  )

  def __init__(self):
    self._screen = curses.initscr()
    self._height, self._width = self._screen.getmaxyx()

    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
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
    self._screen.keypad(True)

  def update(
    self,
    timer: int,
    processes: List[IProcess],
    memory,
  ):
    waiting = sum([p.waiting_time for p in processes]) / (
      len(processes) or 1
    )
    service = sum([p.service_time for p in processes]) / (
      len(processes) or 1
    )
    turnaround = sum(
      [p.service_time + p.waiting_time for p in processes]
    ) / (len(processes) or 1)
    self._screen.clear()
    self._screen.addstr(
      0, 0, f"Scheduling Algorithm: {sim_config['scheduling_strategy']}"
    )
    self._screen.addstr(
      1, 0, f"Memory Allocation Algorithm: {mem_config['management_strategy']}"
    )
    self._screen.addstr(2, 0, f"Processes: {sim_config['num_processes']}")
    self._screen.addstr(3, 0, f"Time: {timer}")
    self._screen.addstr(4, 0, "\n", curses.A_REVERSE)
    self._screen.addstr(5, 0, self.__process_table_header, curses.A_REVERSE)

    for process in processes:
      self._addstr(str(process))

    self._screen.addstr(
      int(self._height - 8), 0, f"Memory Free: {memory.free}"
    )

    if sim_config["scheduling_strategy"] == "RR":
      time_quantum = round(
        (
          process_config["range"]["burst"]["end"]
          - process_config["range"]["burst"]["start"]
        )
        / 2
      )
      self._screen.addstr(
        int(self._height - 7), 0, f"Time quantum: {time_quantum}"
      )
    self._screen.addstr(
      int(self._height - 6), 0, f"Average waiting time: {waiting:.2f}"
    )
    self._screen.addstr(
      int(self._height - 5),
      0,
      f"Average service time (cpu utilization): {service:.2f}",
    )
    self._screen.addstr(
      int(self._height - 4), 0, f"Average turnaround time: {turnaround:.2f}"
    )
    self._screen.addstr(int(self._height - 3), 0, "\n")
    self._screen.addstr(
      int(self._height - 1), 0, "PRESS CTRL+C TO TERMINATE", curses.A_REVERSE
    )
    self._screen.refresh()

  def _addstr(self, str_: str):
    colors = {
      "CREATED": curses.COLOR_WHITE,
      "READY": curses.COLOR_RED,
      "WAITING": curses.COLOR_CYAN,
      "EXECUTING": curses.COLOR_YELLOW,
      "FINISHED": curses.COLOR_GREEN,
    }
    pattern: str = r"({0:s})".format(
      "|".join(r"\b{0:s}\b".format(word) for word in colors.keys())
    )
    chars: list[str] = re.split(pattern, str_)
    for c in chars:
      self._screen.addstr(c, curses.color_pair(colors.get(c, 0)))
