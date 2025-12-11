"""Day 04: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day04(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=4)

    def solve_part1(self, data: list[str]) -> str:
        accessableRolls = 0
        # for each line we need to also look at the previous and next lines as well
        for index, line in enumerate(data):
            line = line.strip()
            prev_line = None
            next_line = None
            if not line:
                continue
            if (index > 0):
                prev_line = data[index - 1].strip()
            else:
                prev_line = None
            if (index < len(data) - 1):
                next_line = data[index + 1].strip()
            else:
                next_line = None
                
            # print(f"Processing line {index}: {line}, prev: {prev_line}, next: {next_line}")
            for char_index, char in enumerate(line):
                if char == '@':
                    neighborsCount = 0
                    for i in range(char_index - 1, char_index + 2):
                        if i < 0 or i >= len(line):
                            continue
                        if prev_line and prev_line[i] == '@':
                            # print(f"Found neighbor above at index {i} for char index {char_index}")
                            neighborsCount += 1
                        if next_line and next_line[i] == '@':
                            # print(f"Found neighbor below at index {i} for char index {char_index}")
                            neighborsCount += 1
                        if char_index != i and line[i] == '@':
                            # print(f"Found neighbor side at index {i} for char index {char_index}")
                            neighborsCount += 1
                    if neighborsCount < 4:
                        accessableRolls += 1
        
        return f"Accessable Rolls: {accessableRolls}"

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day04
