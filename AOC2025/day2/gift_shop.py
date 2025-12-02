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

    def _get_chunks(self, string: str, repeat_times: int) -> list[int]:
        chunk_length = len(string) // repeat_times
        return [
            int(string[i * chunk_length : (i + 1) * chunk_length])
            for i in range(repeat_times)
        ]

    def _get_first_different_chunk(self, chunks: list[int]) -> int | None:
        first_chunk = chunks[0]
        for c in chunks:
            if c != first_chunk:
                return c
        return None

    def _get_lowest_possible(self, repeat_times: int) -> int:
        start_str = str(self.start)
        num_start_digits = len(start_str)
        if num_start_digits % repeat_times == 0:
            chunks = self._get_chunks(start_str, repeat_times)
            first_different = self._get_first_different_chunk(chunks)
            if first_different is None or chunks[0] > first_different:
                lowest = chunks[0]
            else:
                lowest = chunks[0] + 1
        else:
            lowest = 10 ** ((num_start_digits - 1) // repeat_times)
        return lowest

    def _get_highest_possible(self, repeat_times: int) -> int:
        end_str = str(self.end)
        num_end_digits = len(end_str)
        if num_end_digits % repeat_times == 0:
            chunks = self._get_chunks(end_str, repeat_times)
            first_different = self._get_first_different_chunk(chunks)
            if first_different is None or chunks[0] < first_different:
                highest = chunks[0]
            else:
                highest = chunks[0] - 1
        else:
            highest = 10 ** ((num_end_digits - 1) // repeat_times) - 1
        return highest

    def repeats(self, repeat_times: int) -> list[int]:
        lowest = self._get_lowest_possible(repeat_times)
        highest = self._get_highest_possible(repeat_times)
        return [int(str(x) * repeat_times) for x in range(lowest, highest + 1)]

    def all_repeats(self) -> set[int]:
        max_times = len(str(self.end))
        return {n for x in range(2, max_times + 1) for n in self.repeats(x)}


def parse_ranges(input_text: str) -> list[Range]:
    return [Range.parse(x.strip()) for x in input_text.split(",")]


def sum_doubles(ranges: list[Range]) -> int:
    return sum(d for r in ranges for d in r.doubles())


def sum_repeats(ranges: list[Range]) -> int:
    return sum(d for r in ranges for d in r.all_repeats())


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
