"""Day 10: Description TBD."""

from __future__ import annotations
from itertools import combinations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day10(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=10)

    def solve_part1(self, data: list[str]) -> str:
        requirementsToButtonsAndStartingSchematics: dict[set[int], tuple[list[set[int]], list[set[int]]]] = {}
        # Each line contains a single indicator light diagram in [square brackets], 
        # one or more button wiring schematics in (parentheses), 
        # and joltage requirements in {curly braces}, which we can ignore for the first part
        # Example line: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        
        # read each line of input data
        for line in data:
            if not line.strip():
                continue
            light_diagram = line[line.index('[')+1:line.index(']')]
            button_schematics = []
            start = line.index(']') + 1
            while '(' in line[start:]:
                open_paren = line.index('(', start)
                close_paren = line.index(')', open_paren)
                button_schematics.append(set(map(int, line[open_paren+1:close_paren].split(','))))
                start = close_paren + 1
            # requirements are ignored for part 1
            requirementsToButtonsAndStartingSchematics[light_diagram] = (button_schematics, [])
        
        # for each line our start sets to turn on the lights are the 
        # sets that contain the indices of '#' in the light diagram
        for light_diagram, (button_schematics, _) in requirementsToButtonsAndStartingSchematics.items():
            required_indices = {i for i, ch in enumerate(light_diagram) if ch == '#'}
            startingSchematics = []
            
            for schematic in button_schematics:
                if schematic.intersection(required_indices):
                    startingSchematics.append(schematic)
                requirementsToButtonsAndStartingSchematics[light_diagram] = (button_schematics, startingSchematics)
                
        # print(f"Starting schematics: {requirementsToButtonsAndStartingSchematics}")
        # now we have starting schematics, we can try to find the minimum button presses
        # start by pressing one button from the starting schematics for each line (light diagram), 
        # then all combinations of two, three etc., until we find the smallest set
        # that covers all, and only, the required indices
        currentTotalPresses = 0
        for light_diagram, (button_schematics, startingSchematics) in requirementsToButtonsAndStartingSchematics.items():
            required_indices = {i for i, ch in enumerate(light_diagram) if ch == '#'}
            # print(f"Finding solution for light diagram: {light_diagram} with required indices: {required_indices}")
            found = False
            currentPresses = 0
            while currentPresses < len(button_schematics) and not found:
                #  here we try all combinations of buttons, for size 1, we only 
                # consider startingSchematics, for size > 1 we consider all schematics, 
                # but we can optimize by ensuring at least one from startingSchematics is included,
                # otherwise we logically won't cover any required indices..
                currentPresses += 1
                # print(f"Trying combinations of size {currentPresses}")
                if currentPresses == 1:
                    combinationsToTry = combinations(startingSchematics, currentPresses)
                else:
                    combinationsToTry = combinations(button_schematics, currentPresses)
                    # filter combinations to ensure at least one from startingSchematics is included
                    combinationsToTry = [combo for combo in combinationsToTry if any(schematic in startingSchematics for schematic in combo)]
                
                # print(f"Combinations to try: {combinationsToTry}")
                for combo in combinationsToTry:
                    # for single schematic, just check if it matches required indices
                    # for multiple, we need to intersect them and see if the total number
                    # of times each index is covered that matches required indices is odd 
                    # and all others are even. For example, if required_indices = {1,3} 
                    # and we have schematics {1,2} and {2,3}, then index 1 is covered once (odd), 
                    # index 2 is covered twice (even), and index 3 is covered once (odd) 
                    # -> this is valid. If we have a more complex combination, like {1,2}, {2,3}, {1,3},
                    # then index 1 is covered twice (even), index 2 is covered twice (even), 
                    # index 3 is covered twice (even) -> this is invalid.
                    coverage_count: dict[int, int] = {}
                    for schematic in combo:
                        for index in schematic:
                            coverage_count[index] = coverage_count.get(index, 0) + 1
                    # print(f"Coverage count for combo {combo}: {coverage_count}")
                    valid = True
                    for index in range(len(light_diagram)):
                        count = coverage_count.get(index, 0)
                        if index in required_indices:
                            if count % 2 == 0:
                                valid = False
                                break
                        else:
                            if count % 2 != 0:
                                valid = False
                                break
                    if valid:
                        print(f"Diagram {light_diagram:<10} - found combination {combo} with size {currentPresses}")
                        currentTotalPresses += currentPresses
                        found = True
                        break
            if not found:
                print(f"No valid combination found for light diagram: {light_diagram}")
                
                
        return str(currentTotalPresses)

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day10
