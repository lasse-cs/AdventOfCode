from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple, Callable, Iterable
from operator import add, mul


Operator = Callable[[int, int], int]


def concat(a: int, b: int) -> int:
    x: int = b
    count: int = 0
    while x > 0:
        x = x // 10
        count += 1
    return (10**count) * a + b


BASE_OPERATORS: list[Operator] = [add, mul]
EXTENDED_OPERATORS: list[Operator] = [*BASE_OPERATORS, concat]


class Callibration(NamedTuple):
    target: int
    items: list[int]

    def is_possible(self, operators: list[Operator] | None = None) -> bool:
        if operators is None:
            operators = BASE_OPERATORS
        return self._is_possible(0, add, 0, operators)

    def _is_possible(
        self,
        accumulator: int,
        operator: Operator,
        index: int,
        operators: list[Operator],
    ) -> bool:
        if index == len(self.items):
            return accumulator == self.target

        accumulator = operator(accumulator, self.items[index])
        return any(
            (
                self._is_possible(accumulator, op, index + 1, operators)
                for op in operators
            )
        )


def total_possible_callibrations(callibrations: list[Callibration]) -> int:
    possible_callibrations: Iterable[int] = (
        callibration.target
        for callibration in callibrations
        if callibration.is_possible()
    )
    return sum(possible_callibrations)


def total_extended_possible_callibrations(callibrations: list[Callibration]) -> int:
    possible_callibrations: Iterable[int] = (
        callibration.target
        for callibration in callibrations
        if callibration.is_possible() or callibration.is_possible(EXTENDED_OPERATORS)
    )
    return sum(possible_callibrations)


def parse(file: Path) -> list[Callibration]:
    with open(file, "r") as f:
        return [parse_callibration(line.strip()) for line in f]


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
