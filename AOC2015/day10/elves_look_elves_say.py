import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    digit: int
    number: int

    def can_merge(self, other: "Block") -> bool:
        return self.digit == other.digit

    def evolve(self) -> tuple["Block", "Block"]:
        return Block(self.number, 1), Block(self.digit, 1)

    def merge(self, other: "Block") -> "Block":
        return Block(digit=self.digit, number=self.number + other.number)

    @staticmethod
    def parse_into_blocks(text: str) -> list["Block"]:
        blocks = []
        digits = [int(i) for i in text]
        previous_digit = None
        number = 0
        i = 0
        while i < len(text):
            current_digit = digits[i]
            if previous_digit and previous_digit != current_digit:
                blocks.append(Block(previous_digit, number))
                number = 0
            previous_digit = current_digit
            number += 1
            i += 1
        blocks.append(Block(current_digit, number))
        return blocks


def evolve_list_of_blocks(blocks: list[Block]) -> list[Block]:
    result = []
    previous_block = None
    for block in blocks:
        a, b = block.evolve()
        if previous_block:
            if not previous_block.can_merge(a):
                result.append(previous_block)
            else:
                a = a.merge(previous_block)
        if not a.can_merge(b):
            result.append(a)
        else:
            b = a.merge(b)
        previous_block = b
    result.append(b)
    return result


def evolve_times(blocks: list[Block], times: int) -> list[Block]:
    b = blocks
    for _ in range(times):
        b = evolve_list_of_blocks(b)
    return b


def digit_count(blocks: list[Block]) -> int:
    return sum(b.number for b in blocks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    num = args.input

    blocks = Block.parse_into_blocks(num)
    evolved = evolve_times(blocks, 40)
    digits = digit_count(evolved)
    print(digits)
    evolved = evolve_times(blocks, 50)
    digits = digit_count(evolved)
    print(digits)


if __name__ == "__main__":
    main()
