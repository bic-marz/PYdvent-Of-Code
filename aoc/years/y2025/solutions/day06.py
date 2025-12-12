"""Day 06: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day06(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=6)

    def solve_part1(self, data: list[str]) -> str:
        numsAndOps: dict[int, list[str]] = {}
        finalSum = 0
        for line in data:
            line = line.strip()
            if not line:
                continue
            
            elements = line.split() # split by whitespace (split() splits on any number of consecutive whitespace)
            for index, element in enumerate(elements):
                if index not in numsAndOps:
                    numsAndOps[index] = []
                numsAndOps[index].append(element.strip())
        
        opIndex = len(numsAndOps.get(1, [])) - 1
        # print(f"Operation Index: {opIndex}")
        for index, elements in numsAndOps.items():
            # print(f"Index {index}: Elements: {elements}")
            
            if opIndex < 0 or opIndex >= len(elements):
                continue
            
            operation = elements[opIndex]
            numbers = [int(e) for i, e in enumerate(elements) if i != opIndex]
            
            if operation == "+":
                finalSum += sum(numbers)
            elif operation == "*":
                product = 1
                for n in numbers:
                    product *= n
                finalSum += product
            else:
                continue
        return str(finalSum)

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day06
