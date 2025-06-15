import random
from collections import Counter
from mahjong import build_deck, draw_tile, score_hand, is_standard_win, is_seven_pairs, tile_to_string


def choose_discard(hand: Counter) -> int:
    # simple heuristic: discard tile with lowest count
    min_tile = None
    min_count = 4
    for t in hand:
        if hand[t] < min_count:
            min_tile = t
            min_count = hand[t]
    return min_tile


def play_game(rng: random.Random) -> int:
    deck = build_deck()
    rng.shuffle(deck)
    dora = draw_tile(deck)
    hands = [[], []]
    for _ in range(13):
        hands[0].append(draw_tile(deck))
        hands[1].append(draw_tile(deck))
    turn = 0
    while deck:
        player = turn % 2
        tile = draw_tile(deck)
        hands[player].append(tile)
        if is_standard_win(hands[player]) or is_seven_pairs(hands[player]):
            score = score_hand(hands[player], tile, dora, 0 if turn == 0 else 1)
            return score if player == 0 else 0
        hand_counter = Counter(hands[player])
        discard = choose_discard(hand_counter)
        hands[player].remove(discard)
        turn += 1
    return 0


def main():
    rng = random.Random(42)
    rounds = 100
    total = 0
    for _ in range(rounds):
        total += play_game(rng)
    print(f"Average dealer points over {rounds} rounds: {total/rounds:.3f}")


if __name__ == "__main__":
    main()
