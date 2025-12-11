"""Day 03: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day03(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=3)

    def solve_part1(self, data: list[str]) -> str:
        maxList: list[int] = []
        for line in data:
            line = line.strip()
            if not line:
                continue
            
            max1 = 0
            max2 = None
            # find two largest numbers (chars), max 1 can nopt be the last number in the line
            for i in range(len(line) - 1):
                num = int(line[i])
                if num > max1:
                    max2 = None # because max2 is only after max1
                    max1 = num
                elif max2 is None or num > max2:
                    max2 = num
            
            if max2 is None or max2 < int(line[-1]):
                max2 = int(line[-1]) # last number if max2 wasnt set or max1 found as before-last number or max2 is less than last number
                
            maxList.append(max1*10 + max2)
            
        return f"MaxList: {maxList}, Total Sum: {sum(maxList)}"

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day03
