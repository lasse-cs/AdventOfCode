import argparse
from pathlib import Path

from dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    @staticmethod
    def parse(input_string: str) -> "Range":
        start_str, end_str = input_string.split("-")
        return Range(int(start_str), int(end_str))

    def doubles(self) -> list[int]:
        return self.repeats(2)

    def repeats(self, repeat_times) -> list[int]:
        start_str = str(self.start)
        num_start_digits = len(start_str)
        if num_start_digits % repeat_times == 0:
            chunk_length = num_start_digits // repeat_times
            chunks = [
                int(start_str[i * chunk_length : (i + 1) * chunk_length])
                for i in range(repeat_times)
            ]
            non_equals = [x for x in chunks if x != chunks[0]]
            if len(non_equals) == 0:
                lowest = chunks[0]
            elif chunks[0] < non_equals[0]:
                lowest = chunks[0] + 1
            else:
                lowest = chunks[0]
        else:
            lowest = 10 ** ((num_start_digits - 1) // repeat_times)

        end_str = str(self.end)
        num_end_digits = len(end_str)
        if num_end_digits % repeat_times == 0:
            chunk_length = num_end_digits // repeat_times
            chunks = [
                int(end_str[i * chunk_length : (i + 1) * chunk_length])
                for i in range(repeat_times)
            ]
            non_equals = [x for x in chunks if x != chunks[0]]
            if len(non_equals) == 0:
                highest = chunks[0]
            elif chunks[0] > non_equals[0]:
                highest = chunks[0] - 1
            else:
                highest = chunks[0]
        else:
            highest = 10 ** ((num_end_digits - 1) // repeat_times) - 1

        return [int(str(x) * repeat_times) for x in range(lowest, highest + 1)]

    def all_repeats(self) -> set[int]:
        max_times = len(str(self.end))
        result = set()
        for x in range(2, max_times + 1):
            repeats = self.repeats(x)
            for n in repeats:
                result.add(n)
        return result


def parse_ranges(input_text: str) -> list[Range]:
    return [Range.parse(x.strip()) for x in input_text.split(",")]


def sum_doubles(ranges: list[Range]) -> int:
    result = 0
    for r in ranges:
        for d in r.doubles():
            result += d
    return result


def sum_repeats(ranges: list[Range]) -> int:
    result = 0
    for r in ranges:
        for d in r.all_repeats():
            result += d
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()
    input_text = args.filename.read_text()
    ranges = parse_ranges(input_text)
    double_sum = sum_doubles(ranges)
    print(double_sum)
    repeat_sum = sum_repeats(ranges)
    print(repeat_sum)


if __name__ == "__main__":
    main()
