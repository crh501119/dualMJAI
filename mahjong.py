import random
from collections import Counter
from typing import List, Tuple

SUITS = ['A', 'B', 'C']
TILE_IDS = list(range(27))  # 0-8 A, 9-17 B, 18-26 C


def tile_to_string(t: int) -> str:
    suit = SUITS[t // 9]
    num = t % 9 + 1
    return f"{suit}{num}"


def build_deck() -> List[int]:
    deck = []
    for t in TILE_IDS:
        deck.extend([t] * 3)
    random.shuffle(deck)
    return deck


def draw_tile(deck: List[int]) -> int:
    return deck.pop()


def remove_tiles(hand: Counter, tiles: List[int]):
    for t in tiles:
        hand[t] -= 1
        if hand[t] == 0:
            del hand[t]


def can_form_sets(hand: Counter) -> bool:
    if not hand:
        return True
    t = min(hand)
    if hand[t] >= 3:
        hand[t] -= 3
        if hand[t] == 0:
            del hand[t]
        if can_form_sets(hand):
            return True
        hand[t] = hand.get(t, 0) + 3
    # sequence
    suit = t // 9
    idx = t % 9
    if idx <= 6:
        seq = [suit * 9 + idx + i for i in range(3)]
        if all(hand.get(s, 0) >= 1 for s in seq):
            for s in seq:
                hand[s] -= 1
                if hand[s] == 0:
                    del hand[s]
            if can_form_sets(hand):
                return True
            for s in seq:
                hand[s] = hand.get(s, 0) + 1
    return False


def is_standard_win(hand_tiles: List[int]) -> bool:
    hand = Counter(hand_tiles)
    for t in list(hand.keys()):
        if hand[t] >= 2:
            hand[t] -= 2
            if hand[t] == 0:
                del hand[t]
            if can_form_sets(hand.copy()):
                return True
            hand[t] = hand.get(t, 0) + 2
    return False


def is_seven_pairs(hand_tiles: List[int]) -> bool:
    c = Counter(hand_tiles)
    return len(hand_tiles) == 14 and all(v == 2 for v in c.values())


def is_pure_suit(hand_tiles: List[int]) -> bool:
    return len(set(t // 9 for t in hand_tiles)) == 1


def is_all_triplets(hand_tiles: List[int]) -> bool:
    c = Counter(hand_tiles)
    pairs = [t for t, v in c.items() if v == 2]
    triplets = [t for t, v in c.items() if v == 3]
    return len(hand_tiles) == 14 and len(pairs) == 1 and len(triplets) == 4


def score_hand(hand_tiles: List[int], winning_tile: int, dora: int, turn: int) -> int:
    if is_seven_pairs(hand_tiles):
        base = 2
    elif is_all_triplets(hand_tiles):
        base = 3
    elif is_pure_suit(hand_tiles):
        base = 3
    elif is_standard_win(hand_tiles):
        base = 1
    else:
        return 0
    if turn == 0:
        base = max(base, 4)
    if winning_tile == dora:
        base += 2
    return base
