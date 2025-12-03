import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Bank:
    batteries: list[int]

    def joltage(self, num_allowed) -> int:
        return self._joltage(num_allowed, 0, len(self.batteries))

    def _joltage(self, num_allowed, start, end):
        if num_allowed <= 0:
            return None
        if end <= start:
            return None
        if num_allowed > end - start:
            return None
        if num_allowed == end - start:
            return int("".join(str(self.batteries[i]) for i in range(start, end)))

        maximum, idx = self._max_with_index(start, end)
        num_on_right = min(end - idx - 1, num_allowed - 1)
        num_on_left = num_allowed - num_on_right - 1
        right_joltage = self._joltage(num_on_right, idx + 1, end)
        left_joltage = self._joltage(num_on_left, start, idx)
        result = str(left_joltage) if left_joltage else ""
        result += str(maximum)
        result += str(right_joltage) if right_joltage else ""
        return int(result)

    def _max_with_index(self, start: int, end: int) -> tuple[int, int]:
        curr_max = self.batteries[start]
        curr_max_idx = start
        for idx, battery in enumerate(self.batteries[start:end], start=start):
            if battery > curr_max:
                curr_max = battery
                curr_max_idx = idx
        return curr_max, curr_max_idx


def total_joltage(banks: list[Bank], num_allowed) -> int:
    return sum(bank.joltage(num_allowed) for bank in banks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    lines = args.filename.read_text().split("\n")
    banks = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        batteries = [int(x) for x in line]
        banks.append(Bank(batteries=batteries))

    two_joltage = total_joltage(banks, 2)
    print(two_joltage)
    twelve_joltage = total_joltage(banks, 12)
    print(twelve_joltage)


if __name__ == "__main__":
    main()
