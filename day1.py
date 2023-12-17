from util import *

lines = read_lines("inputs/day1.txt")

def replace_words(line: str):
    conversion = {"one": "o1e", "two": "t2o", "three": "t3e", "four": "f4r", "five": "f5e", "six": "s6x", "seven": "s7n", "eight": "e8t", "nine": "n9n"}
    for word, digit in conversion.items():
        line = line.replace(word, digit)
    return line

def extract_digits(line):
    return [int(x) for x in split(line) if x.isdigit()]

all_ints = [extract_digits(replace_words(line)) for line in lines]
all_ints = [ints[0]*10 + ints[-1] for ints in all_ints]
print(sum(all_ints))
