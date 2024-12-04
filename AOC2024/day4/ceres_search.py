from typing import NamedTuple, Optional
from argparse import ArgumentParser
from pathlib import Path
from enum import Enum


class Cell(Enum):
    X = 0
    M = 1
    A = 2
    S = 3

    def get_next_cell(self) -> Optional["Cell"]:
        if self.value == len(Cell) - 1:
            return None
        return Cell(self.value + 1)


class CellLocation(NamedTuple):
    row: int
    column: int


class Direction(NamedTuple):
    row: int
    column: int


DIRECTIONS = [
    Direction(1, 0),
    Direction(1, 1),
    Direction(1, -1),
    Direction(-1, 0),
    Direction(-1, 1),
    Direction(-1, -1),
    Direction(0, 1),
    Direction(0, -1),
]


class WordSearch:
    def __init__(self, cells: list[list[Cell]]):
        self.cells = cells

    def count_words(self) -> int:
        total: int = 0
        for row_index, row in enumerate(self.cells):
            for column_index, cell in enumerate(row):
                if cell != Cell.X:
                    continue
                total += self._search_x_cell(CellLocation(row_index, column_index))
        return total

    def _search_x_cell(self, cl: CellLocation) -> int:
        total: int = 0
        for d in DIRECTIONS:
            if self._is_xmas_in_direction(cl, d):
                total += 1
        return total

    def _is_xmas_in_direction(self, cl: CellLocation, d: Direction):
        cur_loc: CellLocation = cl
        cur_cell: Cell = self.cells[cur_loc.row][cur_loc.column]
        while cur_cell != Cell.S:
            next_location = CellLocation(cur_loc.row + d.row, cur_loc.column + d.column)
            if not self._is_cell_location_valid(next_location):
                return False
            next_cell = self.cells[next_location.row][next_location.column]
            if next_cell != cur_cell.get_next_cell():
                return False
            cur_loc = next_location
            cur_cell = next_cell
        return True

    def count_crosses(self) -> int:
        total: int = 0
        for row_index, row in enumerate(self.cells):
            for column_index in range(len(row)):
                if self._is_location_cross(CellLocation(row_index, column_index)):
                    total += 1
        return total

    CROSS_SET = {Cell.S, Cell.M}

    def _is_location_cross(self, cl: CellLocation) -> bool:
        if self.cells[cl.row][cl.column] != Cell.A:
            return False
        if cl.row == 0 or cl.column == 0:
            return False
        if cl.row == len(self.cells) - 1:
            return False
        if cl.column == len(self.cells[cl.row - 1]) - 1:
            return False
        if cl.column == len(self.cells[cl.row + 1]) - 1:
            return False

        diag_one = {
            self.cells[cl.row - 1][cl.column - 1],
            self.cells[cl.row + 1][cl.column + 1],
        }
        diag_two = {
            self.cells[cl.row - 1][cl.column + 1],
            self.cells[cl.row + 1][cl.column - 1],
        }

        return diag_one == WordSearch.CROSS_SET and diag_two == WordSearch.CROSS_SET

    def _is_cell_location_valid(self, cl: CellLocation) -> bool:
        if cl.row < 0 or cl.row >= len(self.cells):
            return False
        if cl.column < 0 or cl.column >= len(self.cells[cl.row]):
            return False
        return True

    @staticmethod
    def parse(input_file: Path) -> "WordSearch":
        cells: list[list[Cell]] = []
        with open(input_file) as f:
            for line in f:
                cells.append(WordSearch._parse_word_search_row(line.strip()))
        return WordSearch(cells)

    @staticmethod
    def _parse_word_search_row(input: str) -> list[Cell]:
        row: list[Cell] = []
        for letter in input:
            row.append(Cell[letter])
        return row


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    word_search: WordSearch = WordSearch.parse(file)
    word_count: int = word_search.count_words()
    print(f"The word search contains {word_count} words")

    cross_count: int = word_search.count_crosses()
    print(f"The word search contains {cross_count} crosses")
