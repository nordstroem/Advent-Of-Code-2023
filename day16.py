import util
from dataclasses import dataclass
grid = util.to_numpy_grid(util.read_file("inputs/day16.txt").strip())
rows, cols = grid.shape

@dataclass(frozen=True)
class Beam:
    pos: tuple[int, int]
    dir: tuple[int, int]

top = list(zip((0,) * cols, range(cols)))
bot = list(zip((rows-1,) * cols, range(cols)))
left = list(zip(range(rows), (0,) * rows))
right = list(zip(range(rows), (cols-1,) * rows))

best = 0
for (coords, dir) in [(top, (1, 0)), (bot, (-1, 0)), (left, (0, 1)), (right, (0,-1))]:
    for coord in coords:
        energized = set()
        energized.add(coord)
        start_beam = Beam(pos=coord, dir=dir)
        energized_states = {start_beam}
        tracked_beams = [start_beam]
        while tracked_beams:
            next_tracked_beams = []
            for beam in tracked_beams:
                energized_states.add(beam)
                energized.add(beam.pos)

                next_pos = (beam.pos[0] + beam.dir[0], beam.pos[1] + beam.dir[1])
                in_grid = 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols
                if not in_grid:
                    continue

                match (grid[next_pos], beam.dir):
                    case (".", _):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=beam.dir))
                    case ("\\", (1, 0)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(0, 1)))
                    case ("\\", (-1, 0)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(0, -1)))
                    case ("\\", (0, 1)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(1, 0)))
                    case ("\\", (0, -1)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(-1, 0)))
                
                    case ("/", (1, 0)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(0, -1)))
                    case ("/", (-1, 0)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(0, 1)))
                    case ("/", (0, 1)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(-1, 0)))
                    case ("/", (0, -1)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(1, 0)))
                
                    case ("|", (0, 1)) | ("|", (0, -1)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(1, 0)))
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(-1, 0)))
                    case ("|", d):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=d))
                    case ("-", (1, 0)) | ("-", (-1, 0)):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(0, 1)))
                        next_tracked_beams.append(Beam(pos=next_pos, dir=(0, -1)))
                    case ("-", d):
                        next_tracked_beams.append(Beam(pos=next_pos, dir=d))
                    case _:
                        assert False

            tracked_beams = [beam for beam in next_tracked_beams if beam not in energized_states]
        best = max(best, len(energized))

print(best)
