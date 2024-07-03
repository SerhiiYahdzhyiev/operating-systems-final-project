
# PSSim

PSSim (Process Scheduling Simulator) is a project meant to be a submission for the final assignment of GISMA University of Applied Sciences's Operating Systems module.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

## Prerequisites

In order to set up and run the project you need to have [Python3](https://www.python.org/downloads/) installed on your computer:

## Dependencies

The project requires the following Python packages:

- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [pydantic](https://docs.pydantic.dev/latest/)

These dependencies are specified in the `pyproject.toml` and `requirements.txt` files and can be installed using the instructions below.

**Note:** If you're using Windows you will probably need to install some specific python package for using `curses`.


## Installation

To set up the project, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/SerhiiYahdzhyiev/operating-systems-final-project.git pssim
   cd pssim
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Make editable install of the project:**
   ```sh
   pip install -e . 
   ```

   **Note:** The concrete commands may differ depending on your python toolchain. The repository holds also a Make file that can be used to simplify/combine some commands.

## Usage

### Command Line Interface (CLI)

PSSim provides a command-line interface (CLI) to configure and run the simulation. Below are the available commands and how to use them:

### Running the Simulation

To run the simulation with the current configuration, use the following command:

```sh
pssim run
```

### Configuring the Simulation

You can configure various aspects of the simulation through the CLI commands before running the simulation. Below are the commands available for configuration:

#### Show Current Configuration

To display the current configuration settings:

```sh
pssim show-config
```

#### Set Number of Processes

To set the number of processes to be generated in the simulation:

```sh
pssim set-num-processes <number>
```

Replace `<number>` with the desired number of processes.

#### Set Burst Time Range

To set the range for burst times of processes:

```sh
pssim set-burst-time-range <start> <end>
```

Replace `<start>` and `<end>` with the desired range values.

#### Set Arrival Time Range

To set the range for arrival times of processes:

```sh
pssim set-arrival-time-range <start> <end>
```

Replace `<start>` and `<end>` with the desired range values.

#### Set Memory Requirements Range

To set the range for memory requirements of processes:

```sh
pssim set-memory-requirements-range <start> <end>
```

Replace `<start>` and `<end>` with the desired range values.

#### Set Scheduling Algorithm

To set the scheduling algorithm used in the simulation:

```sh
pssim set-scheduling-algo <algorithm>
```

Replace `<algorithm>` with one of the following options:
- `FCFS` (First Come - First Served)
- `SJF` (Shortest Job First)
- `SRTF` (Shortest Remaining Time First)
- `RR` (Round Robin)

#### Set Memory Allocation Algorithm

To set the memory allocation algorithm used in the simulation:

```sh
pssim set-memory-allocation-algo <algorithm>
```

Replace `<algorithm>` with one of the following options:
- `FF` (First Fit)
- `BF` (Best Fit)

### Example Usage

Below is an example sequence of commands to configure and run the simulation:

1. Set the number of processes:
   ```sh
   pssim set-num-processes 10
   ```

2. Set the burst time range:
   ```sh
   pssim set-burst-time-range 5 15
   ```

3. Set the arrival time range:
   ```sh
   pssim set-arrival-time-range 1 10
   ```

4. Set the memory requirements range:
   ```sh
   pssim set-memory-requirements-range 20 100
   ```

5. Set the scheduling algorithm:
   ```sh
   pssim set-scheduling-algo FCFS
   ```

6. Set the memory allocation algorithm:
   ```sh
   pssim set-memory-allocation-algo FF
   ```

7. Show the current configuration:
   ```sh
   pssim show-config
   ```

8. Run the simulation:
   ```sh
   pssim run
   ```

### Notes

- Ensure that the values provided for configuration commands are valid and within reasonable ranges.
- You can interrupt the simulation run using `Ctrl+C`.

By following these instructions, you can effectively configure and run the PSSim project to simulate different process scheduling scenarios and memory allocation strategies.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Please review and adjust the project structure section and any other details specific to your project as necessary. If there are additional files or information you'd like to include, feel free to provide them, and I can update the README accordingly.
