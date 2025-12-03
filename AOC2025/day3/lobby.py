import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Bank:
    batteries: list[int]

    def joltage(self, num_allowed) -> int:
        joltage_array = self._joltage(num_allowed, 0, len(self.batteries))
        return sum(num * 10**i for i, num in enumerate(reversed(joltage_array)))

    def _joltage(self, num_allowed, start, end):
        if num_allowed <= 0 or num_allowed > end - start:
            return []
        if num_allowed == end - start:
            return self.batteries[start:end]

        maximum, idx = self._max_with_index(start, end)
        num_on_right = min(end - idx - 1, num_allowed - 1)
        num_on_left = num_allowed - num_on_right - 1
        return (
            self._joltage(num_on_left, start, idx)
            + [maximum]
            + self._joltage(num_on_right, idx + 1, end)
        )

    def _max_with_index(self, start: int, end: int) -> tuple[int, int]:
        curr_max, curr_max_idx = self.batteries[start], start
        for idx, battery in enumerate(self.batteries[start:end], start=start):
            if battery > curr_max:
                curr_max, curr_max_idx = battery, idx
        return curr_max, curr_max_idx


def total_joltage(banks: list[Bank], num_allowed) -> int:
    return sum(bank.joltage(num_allowed) for bank in banks)


def parse_banks(text: str) -> list[Bank]:
    banks = []
    for line in text:
        line = line.strip()
        if not line:
            continue
        batteries = [int(x) for x in line]
        banks.append(Bank(batteries=batteries))
    return banks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    lines = args.filename.read_text().split("\n")
    banks = parse_banks(lines)

    two_joltage = total_joltage(banks, 2)
    print(two_joltage)
    twelve_joltage = total_joltage(banks, 12)
    print(twelve_joltage)


if __name__ == "__main__":
    main()
