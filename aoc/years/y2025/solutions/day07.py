"""Day 07: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day07(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=7)

    def solve_part1(self, data: list[str]) -> str:
        splittersDict: dict[int, bool] = {}
        splitsCount = 0
        
        for line in data:
            line = line.strip()
            if not line:
                continue
            
            for index, char in enumerate(line):
                if char == "S":
                    # starter
                    splittersDict[index] = True
                    continue # safely continue, we know S is only at the start
                if char == "^" and splittersDict.get(index, False):
                    # valid splitter
                    splitsCount += 1
                    if index - 1 >= 0:
                        splittersDict[index - 1] = True
                    if index + 1 < len(line):
                        splittersDict[index + 1] = True
                    splittersDict[index] = False
        
        return f"Splitscount: {splitsCount}"

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day07
