import util
import re

line = util.read_file("inputs/day15.txt").strip()
steps = line.split(",")

def hash(string: str):
    current_value = 0
    for char in string:
        current_value  += ord(char)
        current_value *= 17
        current_value = current_value % 256
    return current_value

boxes = []
for i in range(256):
    boxes.append([])

s = 0
for step in steps:
    if "=" in step:
        label, f = step.split("=")
        box = hash(label)
        box_index = hash(label)
        new_box = []
        replaced = False
        for test_label, test_f in boxes[box_index]:
            if label == test_label:
                new_box.append((label,f))
                replaced = True
            else:
                new_box.append((test_label, test_f))

        if replaced:
            boxes[box_index] = new_box
        else:
            boxes[box_index].append((label, f))
    else:
        label = step[:-1]
        box_index = hash(label)
        boxes[box_index] = [(test_label, test_f) for (test_label, test_f) in boxes[box_index] if test_label != label]


s = 0
for i, box in enumerate(boxes):
    for j, (label, f) in enumerate(box, 1):
        s += (1 + i) * j * int(f)
print(s)
