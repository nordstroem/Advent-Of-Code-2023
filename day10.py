import util
import numpy as np
from shapely import Polygon, Point

grid = util.to_numpy_grid(util.read_file("inputs/day10.txt"))
loop = np.zeros_like(grid, dtype=int)

# build the graph
G = {}
rows, cols = grid.shape
spaces = []
start = tuple[int, int] | None
for row in range(rows):
    for col in range(cols):
        ch = grid[row, col]
        connected: list[tuple[int, int]] = []
        N = (row-1, col)
        S = (row+1, col)
        W = (row, col-1)
        E = (row, col+1)
        match ch:
            case "|":
                connected.append(N)
                connected.append(S)
            case "-":
                connected.append(E)
                connected.append(W)
            case "L": 
                connected.append(N)
                connected.append(E)
            case "J":
                connected.append(N)
                connected.append(W)
            case "7":
                connected.append(S)
                connected.append(W)
            case "F":
                connected.append(S)
                connected.append(E)
            case "S":
                start = (row, col)
                match grid[*W]:
                    case "-" | "L" | "F":
                        connected.append(W)
                match grid[*E]:
                    case "-" | "J" | "7":
                        connected.append(E)
                match grid[*S]:
                    case "|" | "L" | "J":
                        connected.append(S)
                match grid[*N]:
                    case "|" | "7" |"F":
                        connected.append(N)
            case ".":
                spaces.append((row, col))

        G[(row, col)] = connected
                        
assert start is not None

coords = [start]
Q = [start]

while Q:
    v = Q.pop(-1)
    for w in G[v]:
        if w not in coords:
            coords.append(w)
            Q.append(w)


loop_polygon = Polygon(coords)

s = 0
for row in range(rows):
    for col in range(cols):
        v = (row, col)
        if v not in coords and loop_polygon.contains(Point(v)):
            s += 1
print(s)
