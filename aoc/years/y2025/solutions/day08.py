"""Day 08: Description TBD."""

from __future__ import annotations

from aoc.base import BaseChallenge, ChallengeIdentity


class Day08(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=8)
    
    def get3Ddistance (self, point1: tuple[int, int, int], point2: tuple[int, int, int]) -> float:
        x1, y1, z1 = point1
        x2, y2, z2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5


    def solve_part1(self, data: list[str]) -> str:
        """might be a bit more complex than an optimal solution... 
        kinda bruteforced it, it is midnight after all"""
        
        # we need to compute the n shortest paths between all points in 3D space
        points: list[tuple[int, int, int]] = []
        for line in data:
            line = line.strip()
            if not line:
                continue
            
            xStr, yStr, zStr = line.split(",")
            point = (int(xStr), int(yStr), int(zStr))
            points.append(point)
            
        """this will hold a mapping of the index of 2 points to their distance"""    
        pointsToDistances: dict[tuple[int, int], float] = {}
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distance = self.get3Ddistance(points[i], points[j])
                pointsToDistances[(i, j)] = distance

        circuits: list[set[int]] = []
        # sort the distances
        sortedDistances = sorted(pointsToDistances.items(), key=lambda item: item[1])
        madeConnections = 0
        # take the first *numberOfDesiredConnections* shortest distances and build circuits with the points
        numberOfDesiredConnections = 1000
        for (pointIndices, distance) in sortedDistances[:numberOfDesiredConnections]:
            i, j = pointIndices
            # print( f"Processing points {points[i]} and {points[j]} with distance {distance}" )
            foundCircuit = False
            for circuit in circuits:
                if i in circuit or j in circuit:
                    # case 1: both points already in the circuit
                    if i in circuit and j in circuit:
                        foundCircuit = True
                        break
                    
                    # case 2a: one point in the circuit, one in another circuit
                    if i in circuit:
                        otherCircuit = None
                        for c in circuits:
                            if j in c:
                                otherCircuit = c
                                break
                        if otherCircuit is not None:
                            # merge the two circuits
                            circuit.update(otherCircuit)
                            circuits.remove(otherCircuit)
                        else:
                            circuit.add(j)
                        foundCircuit = True
                        madeConnections += 1
                        break
                    
                    # case 2b
                    if j in circuit:
                        otherCircuit = None
                        for c in circuits:
                            if i in c:
                                otherCircuit = c
                                break
                        if otherCircuit is not None:
                            # merge the two circuits
                            circuit.update(otherCircuit)
                            circuits.remove(otherCircuit)
                        else:
                            circuit.add(i)
                        foundCircuit = True
                        madeConnections += 1
                        break
                        
            if not foundCircuit:
                circuits.append(set([i, j]))
                madeConnections += 1
                
            # print( f"Current circuits: {circuits}" )
        
        # print( f"Formed {len(circuits)} circuits after {madeConnections} connections." )
        # print( f"Circuits: {circuits}" )
        
        # now multiply the sizes of the three largest circuits together
        largestCircuits = sorted(circuits, key=lambda c: len(c), reverse=True)[:3]
        # print( f"Largest circuits: {largestCircuits}" )
        result = 1
        for circuit in largestCircuits:
            result *= len(circuit)
            
        return str(result)

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day08
