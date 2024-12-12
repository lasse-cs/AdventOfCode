from argparse import ArgumentParser
from collections import defaultdict, deque
from pathlib import Path
from typing import NamedTuple


class Direction(NamedTuple):
    row: int
    column: int


UP = Direction(-1, 0)
RIGHT = Direction(0, 1)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


class GardenPatch(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "GardenPatch":
        return GardenPatch(self.row + direction.row, self.column + direction.column)

    def get_neighbours(self) -> list["GardenPatch"]:
        return [self.move_in(direction) for direction in DIRECTIONS]


class Region:
    def __init__(self, patches: set[GardenPatch]):
        self.patches: set[GardenPatch] = patches

    def area(self) -> int:
        return len(self.patches)

    def perimeter(self) -> int:
        total: int = 0
        for patch in self.patches:
            for neighbour in patch.get_neighbours():
                if neighbour in self:
                    continue
                total += 1
        return total

    def sides(self) -> int:
        total: int = 0
        for patch in self.patches:
            # The TOP of the current patch will be a new side if:
            # Patch above is not in the region
            # If Patch to the left is in the region Then patch above-left also in patch
            for i, direction in enumerate(DIRECTIONS):
                prev_direction: Direction = DIRECTIONS[(4 + i - 1) % 4]
                if patch.move_in(direction) in self:
                    continue
                previous_patch = patch.move_in(prev_direction)
                if previous_patch in self:
                    if previous_patch.move_in(direction) not in self:
                        continue
                total += 1
        return total

    def fence_cost(self) -> int:
        return self.area() * self.perimeter()

    def discount_fence_cost(self) -> int:
        return self.area() * self.sides()

    def __contains__(self, patch: GardenPatch) -> bool:
        return patch in self.patches

    def __eq__(self, other) -> bool:
        if not isinstance(other, Region):
            return NotImplemented
        return self.patches == other.patches


class Garden:
    def __init__(self, patches: list[list[str]]):
        self.patches: list[list[str]] = patches
        self.regions: dict[str, list[Region]] = defaultdict(list)
        self._explore_regions()

    def _explore_regions(self) -> None:
        visited: set[GardenPatch] = set()
        for row_index, row in enumerate(self.patches):
            for column_index, cell in enumerate(row):
                patch: GardenPatch = GardenPatch(row_index, column_index)
                if patch in visited:
                    continue
                region: Region = self._explore_region(cell, patch)
                self.regions[cell].append(region)
                for patch in region.patches:
                    visited.add(patch)

    def _explore_region(self, cell: str, patch: GardenPatch) -> Region:
        frontier: deque[GardenPatch] = deque()
        frontier.append(patch)
        visited: set[GardenPatch] = {patch}

        while len(frontier) > 0:
            current: GardenPatch = frontier.popleft()

            for neighbour in current.get_neighbours():
                if neighbour in visited:
                    continue
                if neighbour not in self:
                    continue
                if self[neighbour] != cell:
                    continue
                visited.add(neighbour)
                frontier.append(neighbour)
        return Region(visited)

    def total_fence_cost(self) -> int:
        total: int = 0
        for regions_by_type in self.regions.values():
            for region in regions_by_type:
                total += region.fence_cost()
        return total

    def total_discount_fence_cost(self) -> int:
        total: int = 0
        for regions_by_type in self.regions.values():
            for region in regions_by_type:
                total += region.discount_fence_cost()
        return total

    def __contains__(self, patch: GardenPatch) -> bool:
        if patch.row < 0 or patch.row >= len(self.patches):
            return False
        return 0 <= patch.column < len(self.patches[patch.row])

    def __getitem__(self, patch: GardenPatch) -> str:
        return self.patches[patch.row][patch.column]


def parse_file(file: Path) -> Garden:
    with file.open("r") as f:
        return parse(f.readlines())


def parse(lines: list[str]) -> Garden:
    patches: list[list[str]] = []
    for row in lines:
        patches.append([cell for cell in row.strip()])
    return Garden(patches)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    garden: Garden = parse_file(file)
    fence_cost: int = garden.total_fence_cost()
    print(f"The total fence cost is {fence_cost}")

    discount_fence_cost: int = garden.total_discount_fence_cost()
    print(f"The total discount fence cost is {discount_fence_cost}")
