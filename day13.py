import util
import numpy as np
from copy import deepcopy

grids = util.read_file("inputs/day13.txt").strip().split("\n\n")
grids = [util.to_numpy_grid(g) for g in grids]


def find_split_length(grid: np.ndarray, axis: int, forbid: int = -1) -> int:
    candidates = []
    grid = grid if axis == 0 else grid.transpose()
    rows, _ = grid.shape
    for row in range(rows-1):
        if row != forbid and np.all(grid[row,:] == grid[row+1,:]):
            candidates.append(row)
    
    if len(candidates) == 0:
        return 0

    for candidate in candidates:
        valid_candidate = True
        if candidate == 0:
            return 1

        if candidate == (rows-2):
            return rows - 1

        for delta in range(1, rows):
            upper = candidate - delta
            lower = candidate + 1 + delta
            if 0 <= upper < rows and 0 <= lower < rows:
                upper_row = grid[upper,:]
                lower_row = grid[lower,:]
                if not np.all(upper_row == lower_row):
                    valid_candidate = False
            else:
                break

        if valid_candidate:
            return candidate + 1

    return 0


old_results = []

for i, grid in enumerate(grids):
    rows, cols = grid.shape
    a = find_split_length(grid, axis=0)
    b = find_split_length(grid, axis=1)
    old_results.append((a, b))

s = 0
for i, grid in enumerate(grids):
    rows, cols = grid.shape
    found_one = False
    for row in range(rows):
        for col in range(cols):
            if found_one:
                continue
            test_grid = deepcopy(grid)
            if test_grid[row, col] == ".":
                test_grid[row, col] = "#"
            else:
                test_grid[row, col] = "."

            old_a, old_b = old_results[i]
            a = find_split_length(test_grid, axis=0, forbid=old_a-1)
            b = find_split_length(test_grid, axis=1, forbid=old_b-1)

            if a > 0 and not found_one:
                s += 100 * a
                found_one = True
            if b > 0 and not found_one:
                s += b
                found_one = True



print(s)
