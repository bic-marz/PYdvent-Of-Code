"""Day 12: Description TBD."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Iterable

from aoc.base import BaseChallenge, ChallengeIdentity

def _parse_input(lines: list[str]) -> tuple[list[list[str]], list[tuple[int, int, list[int]]]]:
    """
    Returns:
      shapes: list indexed by shape id, each is list[str] rows of '.'/'#'
      regions: list of (W, H, counts)
    """
    shape_header = re.compile(r"^(\d+):$")
    region_line = re.compile(r"^(\d+)x(\d+):\s*(.*)$")

    raw_shapes: dict[int, list[str]] = {}
    regions: list[tuple[int, int, list[int]]] = []

    i = 0
    n = len(lines)

    # Parse shapes until we hit the first region line.
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue

        m_region = region_line.match(s)
        if m_region:
            break

        m_shape = shape_header.match(s)
        if not m_shape:
            raise ValueError(f"Unexpected line while parsing shapes: {lines[i]!r}")

        idx = int(m_shape.group(1))
        i += 1

        grid: list[str] = []
        while i < n:
            row = lines[i].rstrip("\n")
            if not row.strip():
                i += 1
                if grid:
                    break
                continue
            row_stripped = row.strip()
            if row_stripped and row_stripped[0] in ".#":
                grid.append(row_stripped)
                i += 1
            else:
                break

        if not grid:
            raise ValueError(f"Shape {idx} has no rows.")
        raw_shapes[idx] = grid

    if not raw_shapes:
        raise ValueError("No shapes parsed.")

    max_id = max(raw_shapes.keys())
    shapes: list[list[str]] = []
    for sid in range(max_id + 1):
        if sid not in raw_shapes:
            raise ValueError(f"Missing shape id {sid} (shape ids must be contiguous 0..N-1).")
        shapes.append(raw_shapes[sid])

    # Parse regions from remaining lines.
    while i < n:
        s = lines[i].strip()
        i += 1
        if not s:
            continue
        m = region_line.match(s)
        if not m:
            raise ValueError(f"Unexpected line while parsing regions: {s!r}")
        w = int(m.group(1))
        h = int(m.group(2))
        rest = m.group(3).strip()
        counts = list(map(int, rest.split())) if rest else []
        regions.append((w, h, counts))

    return shapes, regions


def _shape_cells(shape_grid: list[str]) -> list[tuple[int, int]]:
    cells: list[tuple[int, int]] = []
    for y, row in enumerate(shape_grid):
        for x, ch in enumerate(row):
            if ch == "#":
                cells.append((x, y))
    if not cells:
        raise ValueError("Shape has zero '#' cells.")
    return cells


def _normalize(points: Iterable[tuple[int, int]]) -> tuple[tuple[tuple[int, int], ...], int, int]:
    pts = list(points)
    min_x = min(x for x, _ in pts)
    min_y = min(y for _, y in pts)
    shifted = [(x - min_x, y - min_y) for x, y in pts]
    max_x = max(x for x, _ in shifted)
    max_y = max(y for _, y in shifted)
    shifted_sorted = tuple(sorted(shifted))
    w = max_x + 1
    h = max_y + 1
    return shifted_sorted, w, h


def _orientations(cells: list[tuple[int, int]]) -> list[tuple[tuple[tuple[int, int], ...], int, int]]:
    """
    Generate unique orientations under D4 (rotations + flips).
    Returns list of (points, w, h) where points are normalized and sorted.
    """
    uniq: set[tuple[tuple[int, int], ...]] = set()
    out: list[tuple[tuple[tuple[int, int], ...], int, int]] = []

    for flip in (False, True):
        pts0 = [(-x, y) if flip else (x, y) for x, y in cells]
        for rot in range(4):
            pts = pts0
            for _ in range(rot):
                # rotate 90°: (x, y) -> (y, -x)
                pts = [(y, -x) for x, y in pts]
            norm_pts, w, h = _normalize(pts)
            if norm_pts not in uniq:
                uniq.add(norm_pts)
                out.append((norm_pts, w, h))

    return out


def _placements_for_region(
    W: int,
    H: int,
    oriented: list[tuple[tuple[tuple[int, int], ...], int, int]],
) -> list[int]:
    """
    For a fixed region WxH, return all placement bitmasks of a shape across all orientations.
    Bit i corresponds to cell index i = y*W + x.
    """
    placements: list[int] = []
    for pts, w, h in oriented:
        if w > W or h > H:
            continue
        for oy in range(H - h + 1):
            base_row = oy * W
            for ox in range(W - w + 1):
                mask = 0
                for dx, dy in pts:
                    bit_index = (base_row + dy * W) + (ox + dx)
                    mask |= 1 << bit_index
                placements.append(mask)
    return placements


def _can_fit_region(
    W: int,
    H: int,
    counts: list[int],
    shape_orients: list[list[tuple[tuple[tuple[int, int], ...], int, int]]],
    shape_areas: list[int],
) -> bool:
    N = len(shape_orients)
    counts_padded = counts[:] + [0] * max(0, N - len(counts))
    counts_padded = counts_padded[:N]

    total_area = sum(counts_padded[i] * shape_areas[i] for i in range(N))
    if total_area == 0:
        return True
    if total_area > W * H:
        return False

    placements: list[list[int]] = []
    for i in range(N):
        if counts_padded[i] > 0:
            plist = _placements_for_region(W, H, shape_orients[i])
            if not plist:
                return False
            placements.append(plist)
        else:
            placements.append([])

    counts_t = tuple(counts_padded)
    board_area = W * H

    @lru_cache(maxsize=None)
    def dfs(occupied: int, remaining: tuple[int, ...]) -> bool:
        remaining_area = 0
        for i, c in enumerate(remaining):
            if c:
                remaining_area += c * shape_areas[i]

        if remaining_area == 0:
            return True

        free_cells = board_area - occupied.bit_count()
        if remaining_area > free_cells:
            return False

        # Choose the most constrained shape type (fewest non-overlapping placements).
        best_i = -1
        best_opts: list[int] | None = None

        for i, c in enumerate(remaining):
            if c == 0:
                continue
            opts = [m for m in placements[i] if (m & occupied) == 0]
            if not opts:
                return False
            if best_opts is None or len(opts) < len(best_opts):
                best_i = i
                best_opts = opts
                if len(best_opts) == 1:
                    break

        assert best_opts is not None and best_i >= 0

        rem_list = list(remaining)
        rem_list[best_i] -= 1
        next_remaining = tuple(rem_list)

        for m in best_opts:
            if dfs(occupied | m, next_remaining):
                return True
        return False

    return dfs(0, counts_t)


class Day12(BaseChallenge):
    identity = ChallengeIdentity(year=2025, day=12)

    def solve_part1(self, data: list[str]) -> str:
        # each shape starts with its index and a colon; then, 
        # the shape is displayed visually, in a 2D grid,
        # where # is part of the shape and . is not.
        
        # The second section lists the regions under the trees. 
        # Each line starts with the width and length of the region; 
        # 12x5 means the region is 12 units wide and 5 units long. 
        # The rest of the line describes the presents 
        # that need to fit into that region by listing the quantity 
        # of each shape of present; 1 0 1 0 3 2 means you need 
        # to fit one present with shape index 0, no presents with 
        # shape index 1, one present with shape index 2, etc.
        shapes: dict[int, list[str]] = {}
        regions: list[tuple[int, int, list[int]]] = []
        currentShapeIndex: int | None = None
        currentShapeLines: list[str] = []
        previousLineWasSpace: bool = False
        parsingRegions: bool = False
        
        for line in data:
            if not line.strip():
                previousLineWasSpace = True
                continue
            if line.endswith(":"):
                # new shape starts
                if currentShapeIndex is not None:
                    shapes[currentShapeIndex] = currentShapeLines
                currentShapeIndex = int(line[:-1])
                currentShapeLines = []
                previousLineWasSpace = False
            else:
                if previousLineWasSpace:
                    # here the regions are listed; stop parsing shapes
                    if currentShapeIndex is not None:
                        shapes[currentShapeIndex] = currentShapeLines
                    currentShapeIndex = None
                    currentShapeLines = []
                    parsingRegions = True
                    previousLineWasSpace = False
                if parsingRegions:
                    # parse region line
                    parts = line.split()
                    dimensions = parts[0].split('x')
                    width = int(dimensions[0])
                    length = int(dimensions[1].strip(":"))
                    shapeCounts = list(map(int, parts[1:]))
                    regions.append((width, length, shapeCounts))
                else:
                    # continue parsing current shape
                    currentShapeLines.append(line.strip())
                
            if currentShapeIndex is not None:
                shapes[currentShapeIndex] = currentShapeLines    
                        
        # print(f"Parsed shapes: {shapes}")
        # print(f"Parsed regions: {regions}")
        
        # The second region, 12x5: 1 0 1 0 2 2, is 12 units wide 
        # and 5 units long. In that region, you need to try to fit 
        # one present with shape index 0, one present 
        # with shape index 2, two presents with shape index 4, 
        # and two presents with shape index 5.
        # Presents can be rotated and flipped as necessary 
        # to make them fit in the available space
        # So our approach will be to try to fit the required shapes
        # into each region, and see if we can find a valid arrangement.
        # This is a complex packing problem but we will solve it in a 
        # simplified brute force manner, 
        # since optimization is not the focus here for now.
        
        # After some experimentation, it turns out that you can fit both presents in this region. Here is one way to do it, using A to represent one present and B to represent the other:

        # AAA.
        # ABAB
        # ABAB
        # .BBB
        
        # so our approach will be to try to fit the required shapes
        # into each region, and see if we can find a valid arrangement.
        # This is a complex packing problem but we will solve it in a 
        # simplified brute force manner, 
        # since optimization is not the focus here for now.
        # Precompute cells/orientations/areas per shape.
        shapes, regions = _parse_input(data)
        base_cells = [_shape_cells(g) for g in shapes]
        shape_areas = [len(c) for c in base_cells]
        shape_orients = [_orientations(c) for c in base_cells]

        ok = 0
        for W, H, counts in regions:
            if _can_fit_region(W, H, counts, shape_orients, shape_areas):
                ok += 1
        return str(ok)

    def solve_part2(self, data: list[str]) -> str:
        # TODO: implement part 2
        return "not implemented"


Challenge = Day12
