import argparse
from dataclasses import dataclass
from pathlib import Path
import re

INSTRUCTION_REGEX = r"(turn on|toggle|turn off) (\d+),(\d+) through (\d+),(\d+)"


@dataclass
class Instruction:
    start: tuple[int, int]
    end: tuple[int, int]

    def apply_per_cell(self, grid, operation):
        for row_index in range(self.start[0], self.end[0] + 1):
            for column_index in range(self.start[1], self.end[1] + 1):
                grid[row_index][column_index] = operation(grid[row_index][column_index])


@dataclass
class ToggleInstruction(Instruction):
    def apply(self, grid: list[list[int]]):
        self.apply_per_cell(grid, lambda x: int(not x))

    def alternate_apply(self, grid: list[list[int]]):
        self.apply_per_cell(grid, lambda x: x + 2)


@dataclass
class TurnOffInstruction(Instruction):
    def apply(self, grid: list[list[int]]):
        self.apply_per_cell(grid, lambda x: 0)

    def alternate_apply(self, grid: list[list[int]]):
        self.apply_per_cell(grid, lambda x: max(0, x - 1))


@dataclass
class TurnOnInstruction(Instruction):
    def apply(self, grid: list[list[int]]):
        self.apply_per_cell(grid, lambda x: 1)

    def alternate_apply(self, grid: list[list[int]]):
        self.apply_per_cell(grid, lambda x: x + 1)


def parse_instruction(text: str) -> Instruction:
    matched = re.match(INSTRUCTION_REGEX, text)
    if not matched:
        raise ValueError
    instruction_type = matched.group(1)
    start = (int(matched.group(2)), int(matched.group(3)))
    end = (int(matched.group(4)), int(matched.group(5)))
    if instruction_type == "turn on":
        return TurnOnInstruction(start, end)
    elif instruction_type == "turn off":
        return TurnOffInstruction(start, end)
    else:
        return ToggleInstruction(start, end)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    instructions = [parse_instruction(x) for x in text.splitlines()]
    for instruction in instructions:
        instruction.apply(grid)
    total_on = sum(grid[r][c] for r in range(1000) for c in range(1000))
    print(total_on)

    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for instruction in instructions:
        instruction.alternate_apply(grid)
    total_brightness = sum(grid[r][c] for r in range(1000) for c in range(1000))
    print(total_brightness)


if __name__ == "__main__":
    main()
