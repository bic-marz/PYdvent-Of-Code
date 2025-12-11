"""Day 02: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day02(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=2)
    
    @staticmethod
    def _parse_ranges(data: list[str]) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        for line in data:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            for part in parts:
                bounds = part.split("-")
                if len(bounds) != 2:
                    continue
                start, end = int(bounds[0]), int(bounds[1])
                ranges.append((start, end))
        return ranges
    
    @staticmethod
    def findInvalidIdsInRange(range_tuple: tuple[int, int]) -> list[int]:
        start, end = range_tuple
        invalid_ids = []
        for num in range(start, end + 1):
            str_num = str(num)
            len_num = len(str_num)
            # if the length of the id is an even number, it's skipped
            if len_num % 2 != 0:
                continue
            # if the first half of the digits is equal to the second half, it's invalid
            mid = len_num // 2
            # print(f"Checking ID {num}, len {len_num}, mid {mid}, first half {str_num[:mid]}, second half {str_num[mid:]}")
            if str_num[:mid] == str_num[mid:]:
                invalid_ids.append(num)    
        
        return invalid_ids
    
    def solve_part1(self, data: list[str]) -> str:
        ranges = self._parse_ranges(data)
        invalid_ids = []
        for range_tuple in ranges:
            invalid_ids.extend(self.findInvalidIdsInRange(range_tuple))
        ids_arr = str(len(invalid_ids))
        return f"{ids_arr} invalid IDs found: {invalid_ids}, with sum {sum(invalid_ids)}"

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day02
