"""Day 09: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day09(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=9)

    def solve_part1(self, data: list[str]) -> str:
        # read the coordinates of points in 2D space from the input data
        points: list[tuple[int, int]] = []
        for line in data:
            line = line.strip()
            if not line:
                continue

            xStr, yStr = line.split(",")
            point = (int(xStr), int(yStr))
            points.append(point)
            
        #  for every pair of points that are not aligned either horizontally or vertically,
        #  compute the area of the rectangle if they were the opposite corners
        currentMaxArea: tuple[int, tuple[int, int]] = (0, (-1, -1))
        for pt1 in range(len(points)):
            for pt2 in range(pt1 + 1, len(points)):
                x1, y1 = points[pt1]
                x2, y2 = points[pt2]
                if x1 != x2 and y1 != y2:
                    # calculate area (+ 1 otherwise the edges are not included...)
                    area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                    if area > currentMaxArea[0]:
                        # print( f"New max area {area} found with points {points[pt1]} and {points[pt2]}" )
                        currentMaxArea = (area, (pt1, pt2))
                        
        return str(currentMaxArea)

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day09
