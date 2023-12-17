import util
import numpy as np
from itertools import combinations

grid = util.to_numpy_grid(util.read_file("inputs/day11.txt").strip())
rows, cols = grid.shape

galaxies = []
index = 1
for row in range(rows):
    for col in range(cols):
        if grid[row, col] == "#":
            galaxies.append((row, col, index))
            index += 1
s = 0

row_is_empty = np.zeros(rows, dtype=bool)
col_is_empty = np.zeros(cols, dtype=bool)

for row in range(0, rows):
    if np.all(grid[row, :] == "."):
        row_is_empty[row] = True

for col in range(0, cols):
    if np.all(grid[:,col] == "."):
        col_is_empty[col] = True


for g1, g2 in combinations(galaxies, 2):
    rs = min(g1[0], g2[0])
    re = max(g1[0], g2[0])
    cs = min(g1[1], g2[1])
    ce = max(g1[1], g2[1])

    empty_rows = 0
    for row in range(rs+1, re):
        if row_is_empty[row]:
            empty_rows += 1

    empty_cols = 0
    for col in range(cs+1, ce):
        if col_is_empty[col]:
            empty_cols += 1

    scaling = (1000000-1)
    l = (re+empty_rows*scaling) - rs + (ce+empty_cols*scaling) - cs
    s += l
    
print(s)

# 519940427545 too high
# 519939907614
