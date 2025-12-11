# Advent of Code – Python Toolkit

A lightweight Python workflow for solving [Advent of Code](https://adventofcode.com/) puzzles inside VS Code, complete with scaffolding, linting, and a friendly CLI runner.

## Requirements

- Python 3.11+
- (Optional) `uv`, `pipx`, or `pip` for dependency management

## Setup

```bash
# Create a virtual environment however you prefer, then install deps
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Running a Solution

```bash
# Run both parts for Day 1 of 2025
python -m aoc 2025 1

# Run only part 2 with a custom input file
python -m aoc 2025 1 --part 2 --input path/to/sample.txt
```

The CLI dynamically imports `aoc.years.y<year>.solutions.day<day>` modules, so adding a new file is all you need.

## Creating a New Day

Use the helper script to scaffold both the Python module and an empty input file:

```bash
scripts/new_day.py 2025 02
```

This generates:

- `aoc/years/y2025/solutions/day02.py` – starter class that inherits from `BaseChallenge`
- `aoc/years/y2025/inputs/day02.txt` – placeholder for your puzzle input

## Project Layout

```
advent_of_code/
├── aoc/
│   ├── __init__.py
│   ├── base.py               # BaseChallenge utilities
│   ├── cli.py                # python -m aoc entry point
│   ├── runner.py             # dynamic loader + timings
│   └── years/
│       └── y2025/
│           ├── inputs/
│           │   └── day01.txt
│           └── solutions/
│               └── day01.py  # Example solution
├── scripts/
│   └── new_day.py            # Scaffolding helper
├── pyproject.toml            # Project + tooling config
├── README.md
└── QUICKSTART.md
```

## Tips

- Keep multiple inputs per day (sample vs real) by storing files next to the default `dayXX.txt` and pass `--input` when running.
- Lint with `ruff`: `ruff check .`
- Test helpers with `pytest` once you add unit tests for tricky parsing logic.

Happy puzzling! 🎄
