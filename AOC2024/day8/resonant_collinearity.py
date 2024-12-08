from argparse import ArgumentParser
from typing import NamedTuple
from collections import defaultdict
from pathlib import Path
from itertools import combinations
from math import gcd


class Location(NamedTuple):
    row: int
    column: int

    def direction_to(self, other: "Location") -> "Direction":
        return Direction(other.row - self.row, other.column - self.column)

    def move_in(self, direction: "Direction") -> "Location":
        return Location(self.row + direction.row, self.column + direction.column)


class Direction(NamedTuple):
    row: int
    column: int

    def __neg__(self) -> "Direction":
        return Direction(-self.row, -self.column)

    def reduce(self) -> "Direction":
        common_div: int = gcd(self.row, self.column)
        return Direction(self.row // common_div, self.column // common_div)


class Map(NamedTuple):
    rows: int
    columns: int
    antenna_locations: dict[str, list[Location]]

    def find_point_antinodes(self) -> set[Location]:
        antinodes: set[Location] = set()
        for antenna_list in self.antenna_locations.values():
            for combination in combinations(antenna_list, r=2):
                first_antenna, second_antenna = combination
                direction = first_antenna.direction_to(second_antenna)

                first_antinode = second_antenna.move_in(direction)
                if self._is_location_on_map(first_antinode):
                    antinodes.add(first_antinode)

                second_antinode = first_antenna.move_in(-direction)
                if self._is_location_on_map(second_antinode):
                    antinodes.add(second_antinode)

        return antinodes

    def find_line_antinodes(self) -> set[Location]:
        antinodes: set[Location] = set()
        for antenna_list in self.antenna_locations.values():
            for combination in combinations(antenna_list, r=2):
                first_antenna, second_antenna = combination
                direction = first_antenna.direction_to(second_antenna)
                forward_direction = direction.reduce()
                backward_direction = -forward_direction
                current_location: Location = first_antenna

                # First go forwards
                while self._is_location_on_map(current_location):
                    antinodes.add(current_location)
                    current_location = current_location.move_in(forward_direction)

                # Then go backwards
                current_location = first_antenna
                while self._is_location_on_map(current_location):
                    antinodes.add(current_location)
                    current_location = current_location.move_in(backward_direction)

        return antinodes

    def _is_location_on_map(self, location: Location) -> bool:
        if location.row < 0 or location.row >= self.rows:
            return False
        return location.column >= 0 and location.column < self.columns


def parse(file: Path) -> Map:
    with open(file, "r") as f:
        return _parse(f.readlines())


def _parse(lines: list[str]) -> Map:
    rows: int = len(lines)
    columns: int = len(lines[0].strip()) if rows > 0 else 0
    antenna_locations: defaultdict[str, list[Location]] = defaultdict(list)

    for row_index, row in enumerate(lines):
        for column_index, cell in enumerate(row.strip()):
            if cell == ".":
                continue
            antenna: Location = Location(row_index, column_index)
            antenna_locations[cell].append(antenna)
    return Map(rows, columns, dict(antenna_locations))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    map: Map = parse(file)
    antinodes: set[Location] = map.find_point_antinodes()
    number_point_antinodes = len(antinodes)
    print(f"There are {number_point_antinodes} point antinodes on the map")

    line_antinodes: set[Location] = map.find_line_antinodes()
    number_line_antinodes = len(line_antinodes)
    print(f"There are {number_line_antinodes} line antinodes on the map")
