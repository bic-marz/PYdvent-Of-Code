"""Day 05: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day05(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=5)

    def solve_part1(self, data: list[str]) -> str:
        # first we "collect" all the fresh ingredients in one bool list
        freshIngredientsRanges: list[tuple[int, int]] = []
        lastRangesIndex = 0
        freshIngredientsCount = 0 
        for index, line in enumerate(data):
            line = line.strip()
            if not line:
                lastRangesIndex = index
                break # stop at empty line (separates fresh-ranges from available ingredients)
            
            start, stop = line.split('-')
            freshIngredientsRanges.append((int(start), int(stop)))
                
        for line in data[lastRangesIndex+1:]:
            line = line.strip()
            if not line:
                continue
            
            for rangeStart, rangeEnd in freshIngredientsRanges:
                ingredient = int(line)
                if rangeStart <= ingredient <= rangeEnd:
                    freshIngredientsCount += 1
                    break # found in one of the ranges, no need to check further
                
        return f"Fresh Ingredients Count: {freshIngredientsCount}"

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day05
