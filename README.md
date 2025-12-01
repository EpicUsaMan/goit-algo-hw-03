# Homework 03: Recursion and Algorithms

This project contains three Python programs that demonstrate the use of recursion for solving different computational problems.

## Python Version

Python 3.10 or higher required

## Project Structure

```
goit-algo-hw-03/
├── src/
│   └── utils/
│       ├── __init__.py
│       ├── file_copier.py      # Task 1: Recursive file organizer
│       ├── koch_snowflake.py   # Task 2: Koch snowflake fractal
│       └── hanoi_towers.py     # Task 3: Towers of Hanoi solver
├── tests/
│   ├── __init__.py
│   ├── test_file_copier.py
│   ├── test_koch_snowflake.py
│   └── test_hanoi_towers.py
├── requirements.txt
└── README.md
```

## Utilities

### 1. file_copier

Recursively copies files from a source directory to a destination directory, organizing them into subdirectories based on file extensions.

**Functions:**
- `parse_arguments(args)` - Parse command-line arguments for source and destination directories
- `get_file_extension(file_path)` - Extract file extension without the dot
- `copy_file_to_destination(file_path, destination_base)` - Copy a file to the destination directory organized by extension
- `process_directory_recursive(source_dir, destination_dir)` - Recursively process directory and copy all files
- `main()` - Main entry point that parses arguments and initiates the file copying process

**Usage:**
```bash
# Copy files from source_dir to destination_dir
python -m src.utils.file_copier source_dir destination_dir

# Copy files from source_dir to default 'dist' directory
python -m src.utils.file_copier source_dir
```

**Features:**
- Recursive directory traversal
- Automatic subdirectory creation based on file extensions
- Duplicate filename handling
- Comprehensive error handling
- Preserves file metadata

### 2. koch_snowflake

Generates and visualizes the Koch snowflake fractal using recursion and turtle graphics.

**Functions:**
- `koch_curve(t, length, level)` - Draw a Koch curve segment using recursion
- `draw_koch_snowflake(length, level)` - Draw a complete Koch snowflake with three sides
- `main()` - Main entry point that accepts recursion level as command-line argument

**Usage:**
```bash
# Draw Koch snowflake with recursion level 3
python -m src.utils.koch_snowflake 3

# Interactive mode (will prompt for recursion level)
python -m src.utils.koch_snowflake
```

**Features:**
- Recursive fractal generation
- Interactive turtle graphics visualization
- Configurable recursion depth (0-6 recommended)
- Warning for high recursion levels

**Note:** Requires `python3-tk` package for turtle graphics:
```bash
sudo apt-get install python3-tk  # On Ubuntu/Debian
```

### 3. hanoi_towers

Solves the classic Towers of Hanoi puzzle using recursion and displays the step-by-step solution.

**Functions:**
- `initialize_towers(n)` - Initialize three towers with n disks on tower A
- `move_disk(towers, source, destination)` - Move a disk from source to destination tower
- `print_tower_state(towers, message)` - Print the current state of all towers
- `hanoi_recursive(n, source, destination, auxiliary, towers, show_steps)` - Solve Towers of Hanoi using recursion
- `solve_hanoi(n, show_steps)` - Solve the puzzle and return final tower state
- `main()` - Main entry point that accepts number of disks as command-line argument

**Usage:**
```bash
# Solve for 3 disks
python -m src.utils.hanoi_towers 3

# Interactive mode (will prompt for number of disks)
python -m src.utils.hanoi_towers
```

**Features:**
- Recursive solution algorithm
- Step-by-step visualization
- Initial and final state display
- Validates moves according to Hanoi rules
- Warning for large numbers of disks

**Example Output:**
```
Initial state: {'A': [3, 2, 1], 'B': [], 'C': []}
Move disk from A to C: 1
Intermediate state: {'A': [3, 2], 'B': [], 'C': [1]}
...
Final state: {'A': [], 'B': [], 'C': [3, 2, 1]}
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd goit-algo-hw-03
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
sudo apt install python3-tk
```

## Running Tests

This project uses `pytest` for testing with comprehensive test coverage.

### Run tests with coverage:
```bash
# Run tests with coverage report
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Run coverage and generate badge
coverage run -m pytest
coverage-badge -o coverage.svg
```

## License

This project is created for educational purposes as part of GoIT Algorithm course.

