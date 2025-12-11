#!/usr/bin/env python3
"""Scaffold a new Advent of Code day in Python."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[1]
YEARS_DIR = REPO_ROOT / "aoc" / "years"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create boilerplate for a new AoC day.")
    parser.add_argument("year", type=int, help="Year, e.g. 2025")
    parser.add_argument("day", type=int, help="Day, e.g. 2")
    return parser


def render_template(year: int, day: int) -> str:
    return dedent(
        f"""
        \"\"\"Day {day:02d}: Description TBD.\"\"\"

        from __future__ import annotations

        from aoc.base import BaseChallenge, ChallengeIdentity


        class Day{day:02d}(BaseChallenge):
            identity = ChallengeIdentity(year={year}, day={day})

            def solve_part1(self, data: list[str]) -> str:
                # TODO: implement part 1
                return "not implemented"

            def solve_part2(self, data: list[str]) -> str:
                # TODO: implement part 2
                return "not implemented"


        Challenge = Day{day:02d}
        """
    ).strip() + "\n"


def ensure_year_structure(year: int) -> tuple[Path, Path, Path]:
    year_pkg = YEARS_DIR / f"y{year}"
    year_pkg.mkdir(parents=True, exist_ok=True)

    init_file = year_pkg / "__init__.py"
    if not init_file.exists():
        init_file.write_text(
            f"\"\"\"Solutions for Advent of Code {year}.\"\"\"\n", encoding="utf-8"
        )

    solutions_dir = year_pkg / "solutions"
    solutions_dir.mkdir(exist_ok=True)
    solutions_init = solutions_dir / "__init__.py"
    if not solutions_init.exists():
        solutions_init.write_text(
            f"\"\"\"Solutions for Advent of Code {year}.\"\"\"\n", encoding="utf-8"
        )

    inputs_dir = year_pkg / "inputs"
    inputs_dir.mkdir(exist_ok=True)

    return year_pkg, solutions_dir, inputs_dir


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not (1 <= args.day <= 25):
        raise SystemExit("Day must be between 1 and 25.")

    _, solutions_dir, inputs_dir = ensure_year_structure(args.year)
    day_file = solutions_dir / f"day{args.day:02}.py"
    input_file = inputs_dir / f"day{args.day:02}.txt"

    if day_file.exists():
        print(f"Skipping creation: {day_file} already exists.")
    else:
        day_file.write_text(render_template(args.year, args.day), encoding="utf-8")
        print(f"Created {day_file.relative_to(REPO_ROOT)}")

    if input_file.exists():
        print(f"Input already present: {input_file.relative_to(REPO_ROOT)}")
    else:
        input_file.write_text("", encoding="utf-8")
        print(f"Created empty input at {input_file.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
