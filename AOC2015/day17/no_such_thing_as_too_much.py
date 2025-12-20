import argparse
from dataclasses import dataclass
from pathlib import Path


TARGET = 150


@dataclass(frozen=True)
class Box:
    number: int
    size: int

    @staticmethod
    def parse(text: str, number: int) -> "Box":
        return Box(number, int(text))


def combinations(boxes: list[Box], target: int) -> dict[int, int]:
    combos = {}
    current = []
    _combinations(boxes, target, current, 0, combos)
    return combos


def _combinations(
    boxes: list[Box],
    target: int,
    current: list[Box],
    index: int,
    combos: dict[int, int],
):
    if target < 0:
        return
    if target == 0:
        if len(current) not in combos:
            combos[len(current)] = 0
        combos[len(current)] += 1
        return
    if index == len(boxes):
        return
    current.append(boxes[index])
    _combinations(boxes, target - boxes[index].size, current, index + 1, combos)
    current.pop()
    _combinations(boxes, target, current, index + 1, combos)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()

    boxes = []
    for i, line in enumerate(text.splitlines()):
        boxes.append(Box.parse(line, i))
    combos = combinations(boxes, TARGET)
    number_of_combos = sum(combos.values())
    print(number_of_combos)
    minimum_combinations = combos[min(combos)]
    print(minimum_combinations)


if __name__ == "__main__":
    main()
