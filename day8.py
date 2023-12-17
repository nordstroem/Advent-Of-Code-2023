import util
from dataclasses import dataclass
from itertools import cycle

@dataclass
class Graph:
    left: str
    right: str

G = {}
all_lines = util.read_lines("inputs/day8.txt")
for line in all_lines[2:]:
    line = line.replace(" ", "").replace("(","").replace(")","")
    src, rest = line.split("=")
    left, right = rest.split(",")
    G[src] = Graph(left, right)

current_node = G["AAA"]
steps = 0
for dir in cycle(all_lines[0]):
    steps += 1
    if dir == "R":
        next_node_name = current_node.right 
    else:
        next_node_name = current_node.left 
    if next_node_name == "ZZZ":
        break
    current_node = G[next_node_name]
print(steps)
