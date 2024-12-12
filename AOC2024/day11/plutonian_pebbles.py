from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import TypeAlias

Pebbles: TypeAlias = dict[int, int]


def is_even_length(num: int) -> bool:
    return len(str(num)) % 2 == 0


def split_in_two(num: int) -> list[int]:
    number_string: str = str(num)
    half_length: int = len(number_string) // 2
    return [int(number_string[:half_length]), int(number_string[half_length:])]


def length_after_multiple_blinks(initial: Pebbles, num_blinks: int) -> int:
    pebbles: Pebbles = initial
    for _ in range(num_blinks):
        pebbles = blink(pebbles)
    return length_of_pebbles(pebbles)


def blink(pebbles: Pebbles) -> Pebbles:
    new_pebbles: Pebbles = defaultdict(int)
    for pebble, count in pebbles.items():
        if pebble == 0:
            new_pebbles[1] += count
        elif is_even_length(pebble):
            for half in split_in_two(pebble):
                new_pebbles[half] += count
        else:
            new_pebbles[2024 * pebble] += count
    return new_pebbles


def length_of_pebbles(pebbles: Pebbles) -> int:
    return sum(pebbles.values())


def parse(input: str) -> Pebbles:
    pebbles: Pebbles = defaultdict(int)
    for string_number in input.strip().split(" "):
        number = int(string_number)
        pebbles[number] += 1
    return pebbles


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    initial: Pebbles = parse(file.read_text())
    final_length: int = length_after_multiple_blinks(initial, 25)
    print(f"The final length after 25 blinks is {final_length}")

    final_length = length_after_multiple_blinks(initial, 75)
    print(f"The final length after 75 blinks is {final_length}")
