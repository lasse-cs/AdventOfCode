from argparse import ArgumentParser
from collections.abc import Callable
from collections import defaultdict
from pathlib import Path
from typing import TypeAlias, NamedTuple

Pebbles: TypeAlias = dict[int, int]


class Rule(NamedTuple):
    predicate: Callable[[int], bool]
    operation: Callable[[int], list[int]]


def is_even_length(num: int) -> bool:
    return len(str(num)) % 2 == 0


def split_in_two(num: int) -> list[int]:
    number_string: str = str(num)
    half_length: int = len(number_string) // 2
    return [int(number_string[:half_length]), int(number_string[half_length:])]


replace_zero: Rule = Rule(lambda x: x == 0, lambda _: [1])
split_even_in_half: Rule = Rule(is_even_length, split_in_two)
multiply_by_2024: Rule = Rule(lambda _: True, lambda x: [x * 2024])

RULES: list[Rule] = [replace_zero, split_even_in_half, multiply_by_2024]


def length_after_multiple_blinks(
    initial: Pebbles, num_blinks: int, rules: list[Rule]
) -> int:
    pebbles: Pebbles = initial
    for _ in range(num_blinks):
        pebbles = blink(pebbles, rules)
    return length_of_pebbles(pebbles)


def blink(pebbles: Pebbles, rules: list[Rule]) -> Pebbles:
    new_pebbles: Pebbles = defaultdict(int)
    for pebble, count in pebbles.items():
        for rule in rules:
            if not rule.predicate(pebble):
                continue

            generated_pebbles: list[int] = rule.operation(pebble)
            for gen_peb in generated_pebbles:
                new_pebbles[gen_peb] += count
            break
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
    final_length: int = length_after_multiple_blinks(initial, 25, RULES)
    print(f"The final length after 25 blinks is {final_length}")

    final_length = length_after_multiple_blinks(initial, 75, RULES)
    print(f"The final length after 75 blinks is {final_length}")
