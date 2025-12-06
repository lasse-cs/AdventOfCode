import argparse
from operator import add, mul
from pathlib import Path
import re


class Problem:
    def __init__(self, operation, numbers):
        self.operation = self.parse_operation(operation)
        self.numbers = numbers

    def solve(self):
        result = None
        for num in self.numbers:
            if result is None:
                result = num
            else:
                result = self.operation(result, num)
        return result

    def parse_operation(self, symbol):
        if symbol == "*":
            return mul
        elif symbol == "+":
            return add

    def __eq__(self, other):
        return self.numbers == other.numbers and self.operation == other.operation

    def __repr__(self):
        return f"Problem({self.operation}, {self.numbers})"


def _get_operators(line: str) -> list[str]:
    return re.findall("\\+|\\*", line)


def parse(text: str) -> list[Problem]:
    lines = [t.strip() for t in text.split("\n") if t]
    numbers = [re.findall("\\d+", line) for line in lines[:-1]]
    operators = _get_operators(lines[-1])
    problems = []
    for i, o in enumerate(operators):
        ns = [int(n[i]) for n in numbers]
        problems.append(Problem(o, ns))
    return problems


def parse_column(text: str) -> list[Problem]:
    lines = [t for t in text.split("\n") if t]
    operators = _get_operators(lines[-1])
    numbers = []
    current: list[int] = []
    for cs in zip(*lines[:-1]):
        if all(c == " " for c in cs):
            numbers.append(current)
            current = []
        else:
            current.append(int("".join(cs)))
    else:
        numbers.append(current)
    return [Problem(o, n) for o, n in zip(operators, numbers)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()
    text = args.filename.read_text()

    problems = parse(text)
    grand_total = sum(p.solve() for p in problems)
    print(grand_total)
    cephalod_problems = parse_column(text)
    cephalod_total = sum(p.solve() for p in cephalod_problems)
    print(cephalod_total)


if __name__ == "__main__":
    main()
