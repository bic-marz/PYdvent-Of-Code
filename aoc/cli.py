"""Command-line entry point for the Advent of Code helper."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .runner import format_results, load_challenge, run_challenge


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions without hassle.")
    parser.add_argument("year", type=int, help="Target year, e.g. 2025")
    parser.add_argument("day", type=int, help="Target day, e.g. 1")
    parser.add_argument(
        "--part",
        choices=["1", "2", "both"],
        default="both",
        help="Choose a specific part or run both.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Optional path to override the default input file.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    challenge = load_challenge(args.year, args.day, input_path=args.input)
    results = run_challenge(challenge, part=args.part)
    print(format_results(results))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
