import util
import numpy as np
from dataclasses import dataclass
from itertools import pairwise

grid = util.to_numpy_grid(util.read_file("inputs/day17.txt").strip()).astype(int)
rows, cols = grid.shape

c_to_rc = lambda c: (int(c.imag), int(c.real))

@dataclass(frozen=True)
class State:
    pos: complex
    dir: complex
    num_consecutive: int

    def get_rc(self) -> tuple[int, int]:
        return int(self.pos.imag), int(self.pos.real)
    
    def get_cost(self, r, c):
        if 0 <= r < rows and 0 <= c < cols:
            return grid[r, c]
        return -1
    

    def get_neighbors(self) -> list[tuple["State", int]]:
        neighbors: list[tuple[State, int]] = []
        

        if self.num_consecutive < 10:
            min_distance = max(1, 4 - self.num_consecutive)
            max_distance = max(1, 11 - self.num_consecutive)

            distances = list(range(min_distance, max_distance))
            costs = [self.get_cost(*c_to_rc(self.pos + d * self.dir)) for d in range(1, 11)]
            cum_cost = np.cumsum(costs)[min_distance-1:]

            for d, cost in zip(distances, cum_cost):
                new_state = State(pos=(self.pos + d * self.dir), dir=self.dir, num_consecutive=self.num_consecutive+d)
                r, c = new_state.get_rc()
                if 0 <= r < rows and 0 <= c < cols:
                    neighbors.append((new_state, cost))
            
        for rot in (1j, -1j):
            distances = list(range(4, 11))
            costs = [self.get_cost(*c_to_rc(self.pos + d * self.dir*rot)) for d in range(1, 11)]
            cum_cost = np.cumsum(costs)[3:]

            for d, cost in zip(distances, cum_cost):
                new_dir = self.dir * rot
                new_pos = self.pos + d*new_dir
                new_state = State(pos=new_pos, dir=new_dir, num_consecutive=d)
                r, c = new_state.get_rc()
                if 0 <= r < rows and 0 <= c < cols:
                    neighbors.append((new_state, cost))

        return neighbors
    
start_state = State(pos=0+0j, dir=1 + 0j, num_consecutive=0)
goal_r, goal_c = (rows-1, cols-1)

def neighbors_func(state: State) -> list[tuple[State, int]]:
    return state.get_neighbors()

def heuristic_func(state: State) -> int:
    r, c = state.get_rc()
    return abs(r - goal_r) + abs(c - goal_c)

def goal_func(state: State) -> bool:
    r, c = state.get_rc()
    return r == goal_r and c == goal_c


p = util.a_star(start_state, goal_func=goal_func, heuristic_func=heuristic_func, neighbors_func=neighbors_func)
s = 0
for (a, b) in pairwise(p):
    end = b.pos
    start = a.pos
    dir = (end-start)/abs(end-start)
    test_pos = end
    while abs(test_pos - start) > 0.01:
        r, c = c_to_rc(test_pos)
        s += grid[r, c]
        test_pos -= dir

print(s)
