"""Base classes and helpers for Advent of Code puzzles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from . import YEARS_DIR


@dataclass(slots=True, frozen=True)
class ChallengeIdentity:
    """Lightweight identifier for locating puzzle input files."""

    year: int
    day: int

    @property
    def slug(self) -> str:
        return f"y{self.year}-day{self.day:02d}"

    @property
    def default_input_path(self) -> Path:
        return YEARS_DIR / f"y{self.year}" / "inputs" / f"day{self.day:02d}.txt"


class BaseChallenge(ABC):
    """Common functionality shared by every daily puzzle implementation."""

    #: Override in subclasses or pass explicitly via ``identity``.
    identity = ChallengeIdentity(year=2025, day=1)

    def __init__(self, *, identity: ChallengeIdentity | None = None, input_path: Path | None = None):
        self.identity = identity or self.identity
        self._input_override = input_path

    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------
    def resolve_input_path(self, *, filename: str | None = None) -> Path:
        """Resolve the path to the input file, optionally pointing at a sibling file."""

        if self._input_override and filename is None:
            return self._input_override

        base_path = self._input_override or self.identity.default_input_path
        if filename is None:
            return base_path
        return base_path.parent / filename

    def read_input(self, *, filename: str | None = None) -> list[str]:
        """Read the requested input file and return a list of stripped lines."""

        path = self.resolve_input_path(filename=filename)
        if not path.exists():
            raise FileNotFoundError(
                f"Input file not found for {self.identity.slug}: {path}. "
                "Create it or supply --input when running the CLI."
            )
        return path.read_text(encoding="utf-8").splitlines()

    # ------------------------------------------------------------------
    # Solution contract
    # ------------------------------------------------------------------
    @abstractmethod
    def solve_part1(self, data: Sequence[str]) -> str:
        """Return the answer for part 1."""

    @abstractmethod
    def solve_part2(self, data: Sequence[str]) -> str:
        """Return the answer for part 2."""

    # ------------------------------------------------------------------
    # Convenience entry point
    # ------------------------------------------------------------------
    def run(self, *, part: str | None = None) -> dict[str, str]:
        """Execute one or both parts and return the answers."""

        lines = self.read_input()
        results: dict[str, str] = {}

        if part in (None, "1"):
            results["part1"] = self.solve_part1(lines)
        if part in (None, "2"):
            results["part2"] = self.solve_part2(lines)
        return results