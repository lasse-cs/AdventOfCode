import argparse
from dataclasses import dataclass
from pathlib import Path


DIGITS = "0123456789"
DIRECTIONS = [
    (1, 1),
    (1, 0),
    (1, -1),
    (0, 1),
    (0, -1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
]


@dataclass(frozen=True)
class Symbol:
    symbol: str
    row: int
    column: int

    def is_gear(self) -> bool:
        return self.symbol == "*"


class Grid:
    def __init__(self, grid: list[str], symbols: list[Symbol]):
        self.grid = grid
        self.symbols = symbols

    def _is_on_grid(self, row: int, column: int) -> bool:
        if row < 0 or row >= len(self.grid):
            return False
        return 0 <= column < len(self.grid[row])

    def get_part_number_sum(self) -> int:
        total = 0
        seen_locations: set[tuple[int, int]] = set()
        for symbol in self.symbols:
            deduped_parts = self._get_parts_for_symbol(symbol, seen_locations)
            total += sum(deduped_parts)
        return total

    def _get_parts_for_symbol(
        self, symbol: Symbol, seen_locations: set[tuple[int, int]]
    ) -> list[int]:
        parts = []
        for d in DIRECTIONS:
            row, column = symbol.row + d[0], symbol.column + d[1]
            if not self._is_on_grid(row, column):
                continue
            s = self.grid[row][column]
            if s in DIGITS:
                part = self._get_part(row, column, seen_locations)
                if part:
                    parts.append(part)
        return parts

    def _get_part(
        self, row: int, column: int, seen_locations: set[tuple[int, int]]
    ) -> int | None:
        if (row, column) in seen_locations:
            return None
        digits = ""
        left = 0
        while (
            self._is_on_grid(row, column - left)
            and self.grid[row][column - left] in DIGITS
        ):
            digits = self.grid[row][column - left] + digits
            seen_locations.add((row, column - left))
            left += 1
        right = 1
        while (
            self._is_on_grid(row, column + right)
            and self.grid[row][column + right] in DIGITS
        ):
            digits += self.grid[row][column + right]
            seen_locations.add((row, column + right))
            right += 1
        return int(digits)

    def get_gear_ratio_sum(self) -> int:
        total = 0
        for symbol in self.symbols:
            if not symbol.is_gear():
                continue
            parts = self._get_parts_for_symbol(symbol, set())
            if len(parts) == 2:
                total += parts[0] * parts[1]
        return total

    def parse(text: str) -> "Grid":
        grid = []
        symbols = []
        for r_idx, row in enumerate(text.splitlines()):
            grid.append(row.strip())
            for c_idx, s in enumerate(row.strip()):
                if s == "." or s in DIGITS:
                    continue
                symbols.append(Symbol(symbol=s, row=r_idx, column=c_idx))
        return Grid(grid=grid, symbols=symbols)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    grid = Grid.parse(text)
    part_sum = grid.get_part_number_sum()
    print(part_sum)
    gear_sum = grid.get_gear_ratio_sum()
    print(gear_sum)


if __name__ == "__main__":
    main()
