import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Button:
    positions: list[int]
    bit_pattern: int

    @staticmethod
    def parse(text) -> "Button":
        positions = [int(c) for c in text[1:-1].split(",")]
        bit_pattern = 0
        for i in positions:
            bit_pattern += 2**i
        return Button(positions, bit_pattern)


def bit_pattern_from_indicator(text: str) -> int:
    b = 0
    for i, c in enumerate(text[1:-1]):
        if c == "#":
            b += 2**i
    return b


@dataclass(frozen=True)
class ManualLine:
    target: int
    buttons: list[Button]
    joltage_requirements: tuple

    @staticmethod
    def parse(text: str) -> "ManualLine":
        parts = text.strip().split(" ")
        target = bit_pattern_from_indicator(parts[0])
        buttons = [Button.parse(x) for x in parts[1:-1]]
        joltage_requirements = tuple(int(x) for x in parts[-1][1:-1].split(","))
        return ManualLine(target, buttons, joltage_requirements)

    def minimum_to_configure(self) -> int | None:
        turns = 0
        queue: list[int] = [0]
        seen: set[int] = {0}
        while queue:
            turns += 1
            queue_length = len(queue)
            for _ in range(queue_length):
                state = queue.pop(0)
                for button in self.buttons:
                    new_state = state ^ button.bit_pattern
                    if new_state == self.target:
                        return turns
                    if new_state in seen:
                        continue
                    seen.add(new_state)
                    queue.append(new_state)
        return None

    def minimum_to_get_joltage(self) -> int | None:
        turns = 0
        initial = tuple([0] * len(self.joltage_requirements))
        queue: list[tuple] = [initial]
        seen: set[tuple] = {initial}
        while queue:
            turns += 1
            queue_length = len(queue)
            for _ in range(queue_length):
                state = queue.pop(0)
                for button in self.buttons:
                    new_state = tuple(
                        x + 1 if i in button.positions else x
                        for i, x in enumerate(state)
                    )
                    if new_state == self.joltage_requirements:
                        return turns
                    if new_state in seen:
                        print("seen")
                        continue
                    if any(
                        new_state[i] > self.joltage_requirements[i]
                        for i in range(len(self.joltage_requirements))
                    ):
                        continue
                    seen.add(new_state)
                    queue.append(new_state)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    manual_lines = [ManualLine.parse(x) for x in text.splitlines()]
    minimum_for_all = sum(ml.minimum_to_configure() for ml in manual_lines)
    print(minimum_for_all)

    minimum_for_all_joltage = 0
    for i, ml in enumerate(manual_lines):
        minimum_for_all_joltage += ml.minimum_to_get_joltage()
        print(f"Done {i}")
    print(minimum_for_all_joltage)


if __name__ == "__main__":
    main()
