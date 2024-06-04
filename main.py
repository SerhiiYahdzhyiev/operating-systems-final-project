from typing import Any
import curses
import threading
import signal
import time

# TODO: Decompose, customize, rewrite, refactor...
class StatusUpdater(threading.Thread):
    def __init__(self, entities):
        super().__init__()
        self.entities = entities
        self.interval = 2
        self.running = True

    def run(self):
        while self.running:
            for entity, status in self.entities.items():
                # TODO: Update status based on your logic
                pass
            time.sleep(self.interval)

    def stop(self):
        self.running = False


def main():
    # Mock
    entities = {"Server1": "Running", "Database": "Operational", "Network": "Up"}

    # Initialize curses
    stdscr = curses.initscr()
    curses.cbreak()  # Disable line buffering
    curses.noecho()  # Don't echo key presses

    # Create StatusUpdater thread
    status_updater = StatusUpdater(entities)
    status_updater.start()

    # Define signal handler for graceful termination
    def sigint_handler(signal, frame):
        status_updater.stop()
        curses.nocbreak()  # Re-enable line buffering
        curses.echo()  # Re-enable echo
        curses.endwin()
        print("Exiting...")
        exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    # Main loop for rendering and handling input
    while True:
        # Clear screen and print entity headers
        stdscr.clear()
        stdscr.addstr("Entity\t\tStatus\n", curses.A_BOLD)

        # Print entities and their statuses
        y = 1  # Track row position
        for entity, status in entities.items():
            stdscr.addstr(y, 0, f"{entity:<20}\t{status}\n")
            y += 1

        stdscr.refresh()

        # Check for user input (e.g., 'q' to quit)
        key = stdscr.getch()
        if key == ord('q'):
            break

    status_updater.join()  # Wait for thread to finish


if __name__ == "__main__":
    main()
