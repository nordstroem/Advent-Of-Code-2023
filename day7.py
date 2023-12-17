import util
from dataclasses import dataclass

@dataclass
class Hand:
    cards: tuple[int]
    bid: int

def string_to_values(string: str) -> tuple[int]:
    value_map = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2
    }
    chars = util.split(string)
    return tuple(int(value_map[char]) for char in chars)

def get_type_rank(cards: tuple[int]):
    counts = {}
    for card in cards:
        count = util.count_if(cards, lambda c: c == card)
        counts[card] = count

    def replace_jokers(counts: dict) -> dict:
        if 1 not in counts.keys():
            return counts
        joker_counts = counts[1]
        if joker_counts == 5:
            return {14: 5}
        best_count_and_card = (-1, -1)
        for card, count in counts.items():
            if card == 1:
                continue
            count_card = (count, card)
            if count_card > best_count_and_card:
                best_count_and_card = count_card
        del counts[1]

        counts[best_count_and_card[1]] += joker_counts
        return counts
    
    counts = replace_jokers(counts)
    counts = counts.values()
    if util.count_if(counts, lambda c: c == 5) == 1: # five of a kind
        return 7
    if util.count_if(counts, lambda c: c == 4) == 1: # four of a knd
        return 6
    if util.count_if(counts, lambda c: c == 3) == 1 and util.count_if(counts, lambda c: c == 2) == 1: # full house
        return 5
    if util.count_if(counts, lambda c: c == 3) == 1: # three of a kind
        return 4
    if util.count_if(counts, lambda c: c == 2) == 2: # two pair
        return 3
    if util.count_if(counts, lambda c: c == 2) == 1: # one pair
        return 2
    return 1
    
def key_func(a: Hand):
    return (get_type_rank(a.cards), *a.cards)
    

hands = []
for row in util.read_lines("inputs/day7.txt"):
    cards, bid = row.split(" ")
    hands.append(Hand(string_to_values(cards), int(bid)))

hands = sorted(hands, key=key_func, reverse=False)
s = 0
for i, hand in enumerate(hands, start=1):
    s += i * hand.bid

print(s)

