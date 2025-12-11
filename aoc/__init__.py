"""Advent of Code helper utilities."""

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
YEARS_DIR = PACKAGE_ROOT / "years"

__all__ = ["YEARS_DIR", "PROJECT_ROOT"]
