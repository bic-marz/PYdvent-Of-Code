"""Utilities for discovering and executing Advent of Code challenges."""

from __future__ import annotations

import importlib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from types import ModuleType

from .base import BaseChallenge, ChallengeIdentity


@dataclass(slots=True)
class PartResult:
    part: str
    answer: str
    duration_ms: float


def load_challenge(year: int, day: int, *, input_path: Path | None = None) -> BaseChallenge:
    """Dynamically import the requested challenge module and instantiate its class."""

    module_name = f"aoc.years.y{year}.solutions.day{day:02d}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:  # pragma: no cover - raised only for invalid requests
        raise ModuleNotFoundError(
            f"Could not locate module '{module_name}'. Did you scaffold the day yet?"
        ) from exc

    challenge_cls = _locate_challenge_class(module)
    identity = ChallengeIdentity(year=year, day=day)
    return challenge_cls(identity=identity, input_path=input_path)


def _locate_challenge_class(module: ModuleType) -> type[BaseChallenge]:
    candidate = getattr(module, "Challenge", None)
    if isinstance(candidate, type) and issubclass(candidate, BaseChallenge):
        return candidate

    # Fallback: find the first exported subclass of BaseChallenge.
    for value in vars(module).values():
        if isinstance(value, type) and issubclass(value, BaseChallenge) and value is not BaseChallenge:
            return value

    raise RuntimeError(
        f"Module {module.__name__} does not expose a Challenge subclass. "
        "Export a class named 'Challenge' or assign Challenge = YourClass."
    )


def run_challenge(challenge: BaseChallenge, *, part: str | None = None) -> list[PartResult]:
    """Execute the requested parts and collect timings."""

    raw_input = challenge.read_input()
    parts_to_run: list[str]
    if part is None or part == "both":
        parts_to_run = ["1", "2"]
    else:
        parts_to_run = [part]

    results: list[PartResult] = []
    for current_part in parts_to_run:
        solver = challenge.solve_part1 if current_part == "1" else challenge.solve_part2
        start = perf_counter()
        answer = solver(list(raw_input))
        duration_ms = (perf_counter() - start) * 1000
        results.append(PartResult(part=current_part, answer=answer, duration_ms=duration_ms))
    return results


def format_results(results: Iterable[PartResult]) -> str:
    """Return a printable string summarizing the results."""

    lines = ["===== Advent of Code ====="]
    for result in results:
        lines.append(f"Part {result.part}: {result.answer} ({result.duration_ms:.2f} ms)")
    lines.append("==========================")
    return "\n".join(lines)
