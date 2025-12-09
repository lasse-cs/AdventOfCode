import argparse
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Tile:
    column: int
    row: int

    @staticmethod
    def parse(text: str) -> "Tile":
        return Tile(*(int(x) for x in text.split(",")))

    def area(self, other: "Tile") -> int:
        return abs((self.row - other.row + 1) * (self.column - other.column + 1))


def get_maximum_area(tiles: list[Tile]) -> int:
    current_max = 0
    for t1, t2 in combinations(tiles, 2):
        area = t1.area(t2)
        if area > current_max:
            current_max = area
    return current_max


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    tiles = [Tile.parse(x) for x in text.splitlines()]
    max_area = get_maximum_area(tiles)
    print(max_area)


if __name__ == "__main__":
    main()
