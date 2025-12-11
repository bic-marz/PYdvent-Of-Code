"""Day 1: Circular Navigation."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day01(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=1)

    @staticmethod
    def _parse_moves(data: list[str]) -> list[tuple[str, int]]:
        moves: list[tuple[str, int]] = []
        for line in data:
            line = line.strip()
            if not line:
                continue
            direction = line[0]
            distance = int(line[1:])
            if direction not in {"L", "R"}:
                continue
            moves.append((direction, distance))
        return moves

    def solve_part1(self, data: list[str]) -> str:
        loc = 50
        zeroCnt = 0
        for direction, distance in self._parse_moves(data):
            if direction == "L":
                loc = (loc - distance) % 100
            else:
                loc = (loc + distance) % 100
                
            if (loc == 0): zeroCnt+=1
            
        return f"Final loc: {loc}, final counter: {zeroCnt}"

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day01
