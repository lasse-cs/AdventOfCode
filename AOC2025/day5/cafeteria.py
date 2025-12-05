import argparse
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __contains__(self, ingredient: int) -> bool:
        return self.start <= ingredient <= self.end

    def __len__(self):
        return self.end - self.start + 1

    @staticmethod
    def parse(text: str) -> "Range":
        start, end = [int(x.strip()) for x in text.split("-")]
        return Range(start=start, end=end)

    def can_merge(self, other: "Range") -> bool:
        return other.start in self or other.end in self

    def merge(self, other: "Range") -> "Range":
        new_start = min(self.start, other.start)
        new_end = max(self.end, other.end)
        return Range(new_start, new_end)


def parse_input(text: str) -> tuple[list[Range], list[int]]:
    is_range = True
    ranges = []
    ingredients = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            is_range = False
        elif is_range:
            ranges.append(Range.parse(line))
        elif line:
            ingredients.append(int(line))
    return ranges, ingredients


def get_fresh_ingredients(ranges: list[Range], ingredients: list[int]) -> list[int]:
    fresh = []
    for ingredient in ingredients:
        for r in ranges:
            if ingredient in r:
                fresh.append(ingredient)
                break
    return fresh


def merge_ranges(ranges: list[Range]) -> list[Range]:
    any_merges = True
    result = ranges
    while any_merges:
        any_merges = False
        n = []
        merged = set()
        for r1, r2 in combinations(result, 2):
            if not r1.can_merge(r2):
                continue
            any_merges = True
            merged.add(r1)
            merged.add(r2)
            n.append(r1.merge(r2))
            break
        n.extend(r for r in result if r not in merged)
        result = n
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    ranges, ingredients = parse_input(args.filename.read_text())
    merged_ranges = merge_ranges(ranges)
    fresh_ingredients = get_fresh_ingredients(merged_ranges, ingredients)
    print(len(fresh_ingredients))
    print(sum(len(r) for r in merged_ranges))


if __name__ == "__main__":
    main()
