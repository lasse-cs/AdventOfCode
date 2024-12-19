from argparse import ArgumentParser
from collections.abc import Iterable, Iterator
from pathlib import Path


def count_possibilities_for_pattern(
    towels: list[str], pattern: str, cache: dict[str, int]
) -> int:
    def _count_possibilities(pattern: str) -> int:
        if pattern in cache:
            return cache[pattern]

        if len(pattern) == 0:
            return 1

        count: int = 0
        for towel in towels:
            if pattern[: len(towel)] == towel:
                count += _count_possibilities(pattern[len(towel) :])
        cache[pattern] = count
        return count

    return _count_possibilities(pattern)


def count_possibles(towels: list[str], desired_patterns: list[str]) -> int:
    cache: dict[str, int] = {}
    possibilities: list[int] = [
        count_possibilities_for_pattern(towels, pattern, cache)
        for pattern in desired_patterns
    ]
    return sum(1 if count > 0 else 0 for count in possibilities)


def count_possibilities(towels: list[str], desired_patterns: list[str]) -> int:
    cache: dict[str, int] = {}
    possibilities: list[int] = [
        count_possibilities_for_pattern(towels, pattern, cache)
        for pattern in desired_patterns
    ]
    return sum(possibilities)


def parse(lines: Iterable[str]) -> tuple[list[str], list[str]]:
    line_iter: Iterator[str] = iter(lines)
    available_line: str = next(line_iter)
    available_towels: list[str] = [x.strip() for x in available_line.split(", ")]
    next(line_iter)
    desired_patterns: list[str] = [pattern.strip() for pattern in line_iter]
    return available_towels, desired_patterns


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    with file.open("r") as f:
        towels, desired_patterns = parse(f)
    total_possible = count_possibles(towels, desired_patterns)
    print(f"The total number of possible combinations are {total_possible}")
    all_possibles = count_possibilities(towels, desired_patterns)
    print(f"The total number of possibilites is {all_possibles}")
