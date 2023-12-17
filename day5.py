import util
from dataclasses import dataclass

f = util.read_file("inputs/day5.txt").strip()

seeds, *group_mappings = f.split("\n\n")
seeds = util.extract_ints(seeds)

@dataclass
class MapRange:
    to_start: int
    from_start: int
    range_length: int

    def get_to(self, from_value: int) -> int | None:
        if from_value >= self.from_start and from_value < (self.from_start + self.range_length):
            return self.to_start + (from_value-self.from_start)
        return None
    
    def get_possible_continuations(self, from_value: int, from_length: int) -> tuple[list[tuple[int, int]],...]:
        continuations = []
        # Outside the range
        if from_value >= (self.from_start + self.range_length) or from_value + from_length <= self.from_start:
            return ([], [(from_value, from_length)])
        
        length_to_start = self.from_start - from_value
        remaining_to_test = []
        # Stub in the beginning
        if length_to_start > 0:
            remaining_to_test.append((from_value, length_to_start))

        # overlap
        new_start = from_value + max(0, length_to_start)
        rem_length = from_length - max(0, length_to_start)
        continuations.append((self.get_to(new_start), min(self.range_length, rem_length)))

        if rem_length > self.range_length:
            remaining_to_test.append((self.from_start + self.range_length, (rem_length - self.range_length)))
        return continuations, remaining_to_test

@dataclass
class Mapping:
    from_name: str
    to_name: str
    ranges: list[MapRange]

    def get_to(self, from_value: int):
        for range in self.ranges:
            if to_value := range.get_to(from_value):
                return to_value
        return from_value

    def get_possible_continuations(self, from_value: int, length: int):
        continuations = []
        to_test_ranges = [(from_value, length)]
        for range in self.ranges:
            
            even_more_to_test = []
            for to_test in to_test_ranges:
                new_continuations, more_to_test = range.get_possible_continuations(*to_test)
                continuations += new_continuations
                even_more_to_test += more_to_test
            
            to_test_ranges = even_more_to_test 
        return continuations + to_test_ranges

all_mappings: list[Mapping] = []
for group_mapping in group_mappings:
    map_name, *mappings = group_mapping.split("\n")
    from_name, to_name = map_name[:-5].split("-to-")
    ranges = []
    for mapping in mappings:
        dst_start, src_start, length = util.extract_ints(mapping)
        ranges.append(MapRange(from_start=src_start, to_start=dst_start, range_length=length))
    all_mappings.append(Mapping(from_name=from_name, to_name=to_name, ranges=ranges))

possible_continuations = list(util.batched(seeds, n=2))
for mapping in all_mappings:
    next_batch = []
    for continuation in possible_continuations:
        next_batch += mapping.get_possible_continuations(*continuation)
    possible_continuations = next_batch

values = []
for cont in possible_continuations:
    values.append(cont[0]) 
print(min(values))
