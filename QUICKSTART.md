# Quick Start (Python)

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2. Create a new day

```bash
scripts/new_day.py 2025 02
```

You now have:

- `aoc/years/y2025/solutions/day02.py` – starter class
- `aoc/years/y2025/inputs/day02.txt` – empty input file

### 3. Add your puzzle input

Download from Advent of Code and paste it into `aoc/years/y2025/inputs/day02.txt`.

### 4. Implement your solution

Edit `aoc/years/y2025/solutions/day02.py` and fill in `solve_part1` / `solve_part2`.

### 5. Run it

```bash
python -m aoc 2025 2
# or only part 1
python -m aoc 2025 2 --part 1
```

### 6. Optional tooling

- `pytest` – run tests once you add them

That’s it! Every new day is a script away.
