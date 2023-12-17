import util
from copy import copy

lines = util.read_lines("inputs/day12.txt")

s = 0
for line in lines:
    initial_status, cgroups = line.split(" ")

    initial_status = "?".join([initial_status] * 5)
    cgroups = ",".join([cgroups] * 5)
    initial_cgroup = tuple(map(int, cgroups.split(",")))

    states = {}
    def dp(status: str, cgroup: tuple, cur_contiguous: int) -> int:
        state = (status, cgroup, cur_contiguous)
        if state in states:
            return states[state]

        if len(status) == 0 and len(cgroup) == 0 and cur_contiguous == 0:
            return 1
        if len(status) == 0 and len(cgroup) == 0:
            return 0
        if len(status) == 0 and len(cgroup) == 1 and cgroup[0] == cur_contiguous:
            return 1
        if len(status) == 0 and len(cgroup) >= 1:
            return 0
        if status[0] == ".":
            if cur_contiguous > 0:
                if len(cgroup) == 0:
                    return 0
                if cur_contiguous == cgroup[0]:
                    res = dp(status[1:], cgroup[1:], 0)
                    states[state] = res
                    return res
                else:
                    return 0
            else:
                res = dp(status[1:], cgroup, 0)
                states[state] = res
                return res
        if status[0] == "#":
            res = dp(status[1:], cgroup, cur_contiguous+1) 
            states[state] = res
            return res
        
        # question mark
        path_0 = "." + status[1:]
        path_1 = "#" + status[1:]
        res = dp(path_0, cgroup, cur_contiguous) + dp(path_1, cgroup, cur_contiguous)
        states[state] = res
        return res
    s += dp(initial_status, initial_cgroup, 0)

print(s)
