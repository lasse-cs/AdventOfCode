from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple, Callable
from operator import add, mul
from itertools import product


Operator = Callable[[int, int], int]


def concat(a: int, b: int) -> int:
    x: int = b
    count: int = 0
    while x > 0:
        x = x // 10
        count += 1
    return (10**count) * a + b


BASE_OPERATORS = [add, mul]
EXTENDED_OPERATORS = [*BASE_OPERATORS, concat]


class Callibration(NamedTuple):
    target: int
    items: list[int]

    def is_possible(self, operators: list[Operator] | None = None) -> bool:
        if operators is None:
            operators = BASE_OPERATORS
        if len(self.items) == 1:
            return self.items[0] == self.target
        for combination in product(operators, repeat=len(self.items) - 1):
            acc: int = self.items[0]
            for i, op in enumerate(combination):
                acc = op(acc, self.items[i + 1])
            if acc == self.target:
                return True
        return False


def total_possible_callibrations(callibrations: list[Callibration]) -> int:
    total: int = 0
    for callibration in callibrations:
        if not callibration.is_possible():
            continue
        total += callibration.target
    return total


def total_extended_possible_callibrations(callibrations: list[Callibration]) -> int:
    total: int = 0
    extended_operations: list[Operator] = [add, mul, concat]
    for callibration in callibrations:
        if not callibration.is_possible():
            if not callibration.is_possible(extended_operations):
                continue
        total += callibration.target
    return total


def parse(file: Path) -> list[Callibration]:
    callibrations: list[Callibration] = []
    with open(file, "r") as f:
        for line in f:
            callibration: Callibration = parse_callibration(line.strip())
            callibrations.append(callibration)
    return callibrations


def parse_callibration(input: str) -> Callibration:
    parts: list[str] = input.split(":")
    target: int = int(parts[0])
    items: list[int] = [int(x) for x in parts[1].strip().split(" ")]
    return Callibration(target, items)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    callibrations: list[Callibration] = parse(file)
    total: int = total_possible_callibrations(callibrations)
    print(f"The total of possible callibrations is {total}")

    extended_total: int = total_extended_possible_callibrations(callibrations)
    print(f"The total of extended possible callibrations is {extended_total}")
