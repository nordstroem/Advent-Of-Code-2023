import util
import numpy as np

string_grid = util.to_numpy_grid(util.read_file("inputs/day14.txt").strip())
rows, cols = string_grid.shape
grid = np.zeros_like(string_grid, dtype=int)
for row in range(rows):
    for col in range(cols):
        g = string_grid[row, col]
        if g == ".":
            grid[row,col] = 0
        elif g == "#":
            grid[row,col] = 1
        else:
            grid[row, col] = 2
        

def tilt(grid: np.ndarray, rot_n: int) -> np.ndarray:
    grid = np.rot90(grid, rot_n)
    while True:
        new_grid = grid.copy()
        for row in range(rows-1):
            for col in range(cols):
                g_current = new_grid[row, col]
                g_next = new_grid[row+1, col]
                if g_current == 0 and g_next == 2:
                    new_grid[row, col] = 2
                    new_grid[row+1, col] = 0

        if np.all(new_grid == grid):
            break
        grid = new_grid

    return np.rot90(grid, -rot_n)

def count_load(grid: np.ndarray) -> int:
    load = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 2:
                load += rows - row

    return load
seen_states = list()
seen_states_hash = list()
cyclic_length = 0
cyclic_start = 0
for cycle in range(1000000000):
    state = np.ravel(grid)
    done = False
    for i, seen_state in enumerate(seen_states):
        if np.all(state == seen_state):
            cyclic_start = i
            cyclic_length = cycle - cyclic_start
            done = True
            break
    if done:
        break
    seen_states.append(state)
    grid = tilt(grid, 0) # N
    grid = tilt(grid, 3) # W
    grid = tilt(grid, 2) # S
    grid = tilt(grid, 1) # E

N = 1000000000
print(cyclic_start, cyclic_length)
state = (N-cyclic_start) % cyclic_length + cyclic_start
print(count_load(np.reshape(seen_states[state], grid.shape)))
