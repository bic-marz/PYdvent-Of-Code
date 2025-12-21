"""Day 11: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day11(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=11)

    def solve_part1(self, data: list[str]) -> str:
        sourceToDeste: dict[str, list[str]] = {}
        
        for line in data:
            if not line.strip():
                continue
            parts = line.split(": ")
            source = parts[0].strip()
            dests = [dest.strip() for dest in parts[1].split()]
            sourceToDeste[source] = dests
        
        # print(f"Source to destinations mapping: {sourceToDeste}")    
        # we need to find all unique paths from 'you' to 'out', so we can use DFS or BFS
        finishedPaths: set[tuple[str, ...]] = set()
        pathsToExplore: list[list[str]] = [['you']]
        while pathsToExplore:
            currentPath = pathsToExplore.pop()
            # print(f"Exploring path: {currentPath}")
            currentNode = currentPath[-1]
            # print(f"Current node: {currentNode}")
            if currentNode == 'out':
                finishedPaths.add(tuple(currentPath))
                continue
            for neighbor in sourceToDeste.get(currentNode, []): 
                if neighbor not in currentPath: # avoid cycles
                    newPath = currentPath + [neighbor]
                    pathsToExplore.append(newPath)
        # print(f"Finished paths: {finishedPaths}")
        # print(f"Total unique paths from 'you' to 'out': {len(finishedPaths)}")
        
        return str("Finished calculating: " + str(len(finishedPaths)))

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day11
