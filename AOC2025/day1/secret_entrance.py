import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self


@dataclass(frozen=True)
class Instruction:
    direction: Literal["L", "R"]
    distance: int

    @staticmethod
    def parse(input: str) -> "Self":
        return Instruction(direction=input[0], distance=int(input[1:]))


class Dial:
    def __init__(self, start: int = 50, size: int = 100):
        self.position = start
        self.size = size

    def turn(self, instruction: Instruction) -> int:
        amount = instruction.distance
        turns = amount // self.size
        amount = amount % self.size
        if instruction.direction == "L":
            amount = -amount
        start_zero = self.position == 0
        self.position += amount
        if self.position <= 0 or self.position >= self.size:
            self.position = (self.position + self.size) % self.size
            if not start_zero:
                turns += 1
        return turns

    def password(self, instructions: list[Instruction]):
        zero_stops = 0
        total_turns = 0
        for instruction in instructions:
            total_turns += self.turn(instruction)
            if self.position == 0:
                zero_stops += 1
        return zero_stops, total_turns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()
    input_file = args.filename

    instructions = [
        Instruction.parse(line) for line in input_file.read_text().split("\n") if line
    ]
    dial = Dial()
    password = dial.password(instructions)
    print(password)


if __name__ == "__main__":
    main()
