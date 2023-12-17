import math
from functools import reduce
import re
from typing import Callable, Any, List
import numpy as np
import numpy.typing as npt
import heapq
from collections import defaultdict
from dataclasses import dataclass


def read_lines(path, fun: Callable[[str], Any] = lambda x: x):
    with open(path, 'r') as inp:
        lines = inp.readlines()
        return [fun(l.strip()) for l in lines]


def read_file(path):
    with open(path, 'r') as inp:
        return inp.read()


def count_if(container, predicate):
    count = 0
    for element in container:
        if predicate(element):
            count = count + 1
    return count


def split(line, fun=lambda x: x):
    return [fun(char) for char in line]


def lcm(*args):
    return reduce(lambda a, b: a * b // math.gcd(a, b), args)


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def extract_positive_ints(string):
    return list(map(int, re.findall(r"\d+", string)))

def extract_ints(string):
    return list(map(int, re.findall(r"-?\d+", string)))



def to_numpy_grid(blob: str) -> npt.NDArray:
    lines = blob.split("\n")
    max_cols = len(max(lines, key=lambda l: len(l)))
    rows = list(map(lambda l: split(l.ljust(max_cols)), lines))
    grid = np.array(rows)
    return grid

def numpy_grid_to_string(grid: np.ndarray):
    row_strings = []
    for row in range(grid.shape[0]):
        row_string = "".join(grid[row, :])
        row_strings.append(row_string)
    return "\n".join(row_strings)

def a_star(start: Any, goal_func: Callable[[Any], bool], heuristic_func: Callable[[Any], float], neighbors_func: Callable[[Any], List[Any]]):
    open_set = []
    heapq.heappush(open_set, (0, 0, start))
    items_added = 1

    came_from = {}

    g_scores = defaultdict(lambda: math.inf)
    g_scores[start] = 0

    f_scores = defaultdict(lambda: math.inf)
    f_scores[start] = heuristic_func(start)

    visited = set()

    while open_set:
        _, _, current = heapq.heappop(open_set)
        visited.add(current)

        if goal_func(current):
            shortest_path = [current]
            while current in came_from.keys():
                current = came_from[current]
                shortest_path.insert(0, current)
            return shortest_path

        for neighbor, d in neighbors_func(current):
            tentative_g_score = g_scores[current] + d
            tentative_f_score = g_scores[current] + d + heuristic_func(neighbor)

            if tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = tentative_f_score
                if neighbor not in visited:
                    heapq.heappush(open_set, (tentative_f_score, items_added, neighbor))
                    items_added += 1

    return []
