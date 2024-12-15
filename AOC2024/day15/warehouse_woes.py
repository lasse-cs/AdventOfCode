from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple
from enum import StrEnum
from collections.abc import Iterable
from collections import deque


class Direction(NamedTuple):
    row: int
    column: int

    def is_horizontal(self) -> bool:
        return self.row == 0


DIRECTIONS: dict[str, Direction] = {
    "^": Direction(-1, 0),
    ">": Direction(0, 1),
    "v": Direction(1, 0),
    "<": Direction(0, -1),
}


class WarehouseLocation(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "WarehouseLocation":
        return WarehouseLocation(
            self.row + direction.row, self.column + direction.column
        )

    def gps_coordinate(self):
        return 100 * self.row + self.column


class WarehouseObject(StrEnum):
    WALL = "#"
    ROBOT = "@"
    BOX = "O"
    FREE = "."
    BOX_START = "["
    BOX_END = "]"

    def translate_to_wide(
        o: "WarehouseObject",
    ) -> tuple["WarehouseObject", "WarehouseObject"]:
        if o is WarehouseObject.WALL or o is WarehouseObject.FREE:
            return (o, o)
        if o is WarehouseObject.ROBOT:
            return (WarehouseObject.ROBOT, WarehouseObject.FREE)
        return (WarehouseObject.BOX_START, WarehouseObject.BOX_END)


BOX_OBJECTS: list[WarehouseObject] = [
    WarehouseObject.BOX,
    WarehouseObject.BOX_START,
    WarehouseObject.BOX_END,
]


class Warehouse:
    def __init__(
        self,
        map: list[list[WarehouseObject]],
        robot_location: WarehouseLocation,
        box_locations: set[WarehouseLocation],
    ):
        self.map: list[list[WarehouseObject]] = map
        self.robot_location: WarehouseLocation = robot_location
        self.box_locations: set[WarehouseLocation] = box_locations

    def __str__(self) -> str:
        rows: list[list[str]] = [
            [self.map[r][c].value for c in range(len(row))]
            for r, row in enumerate(self.map)
        ]
        return "\n".join(["".join(row) for row in rows])

    def execute_move(self, direction: Direction):
        boxes: list[WarehouseLocation] = []
        frontier: deque[WarehouseLocation] | None
        frontier = deque()
        frontier.append(self.robot_location)

        while frontier:
            for location in frontier:
                current_object = self[location]
                if current_object in BOX_OBJECTS:
                    boxes.append(location)
            frontier = self._expand_frontier(frontier, direction)

        if frontier is None:
            return

        while boxes:
            old_box_location = boxes.pop()
            self._move_box(old_box_location, direction)

        self._move_robot(direction)

    def _expand_frontier(
        self, frontier: deque[WarehouseLocation], direction: Direction
    ) -> deque[WarehouseLocation] | None:
        new_frontier: deque[WarehouseLocation] = deque()
        for location in frontier:
            new_location = location.move_in(direction)
            w_object: WarehouseObject = self[new_location]
            if w_object is WarehouseObject.WALL:
                return None

            if w_object in BOX_OBJECTS:
                new_frontier.append(new_location)

            if direction.is_horizontal():
                continue

            if w_object is WarehouseObject.BOX_END:
                if WarehouseLocation(location.row, location.column - 1) not in frontier:
                    box_start = WarehouseLocation(
                        new_location.row, new_location.column - 1
                    )
                    new_frontier.appendleft(box_start)
            elif w_object is WarehouseObject.BOX_START:
                if WarehouseLocation(location.row, location.column + 1) not in frontier:
                    box_end = WarehouseLocation(
                        new_location.row, new_location.column + 1
                    )
                    new_frontier.append(box_end)
        return new_frontier

    def _move_box(self, box_location: WarehouseLocation, direction: Direction):
        new_box_location = box_location.move_in(direction)
        self[box_location], self[new_box_location] = (
            WarehouseObject.FREE,
            self[box_location],
        )

        if box_location in self.box_locations:
            self.box_locations.remove(box_location)
            self.box_locations.add(new_box_location)

    def _move_robot(self, direction: Direction):
        self[self.robot_location] = WarehouseObject.FREE
        self.robot_location = self.robot_location.move_in(direction)
        self[self.robot_location] = WarehouseObject.ROBOT

    def gps_coordinate_total(self) -> int:
        return sum(box.gps_coordinate() for box in self.box_locations)

    def __getitem__(self, location: WarehouseLocation) -> WarehouseObject:
        return self.map[location.row][location.column]

    def __setitem__(self, location: WarehouseLocation, item: WarehouseObject):
        self.map[location.row][location.column] = item

    @staticmethod
    def parse(lines: Iterable[str], wide: bool) -> "Warehouse":
        map: list[list[WarehouseObject]] = []
        robot_location: WarehouseLocation | None = None
        box_locations: set[WarehouseLocation] = set()

        def add_object(o: WarehouseObject, row_idx: int, col_idx: int):
            nonlocal robot_location
            map_row.append(o)
            if o is WarehouseObject.BOX or o is WarehouseObject.BOX_START:
                box_locations.add(WarehouseLocation(row_idx, col_idx))
            elif o is WarehouseObject.ROBOT:
                robot_location = WarehouseLocation(row_idx, col_idx)

        for row_index, row in enumerate(lines):
            map_row: list[WarehouseObject] = []
            for column_index, cell in enumerate(row.strip()):
                warehouse_object: WarehouseObject = WarehouseObject(cell)
                if wide:
                    objects = WarehouseObject.translate_to_wide(warehouse_object)
                    for i, wo in enumerate(objects):
                        add_object(wo, row_index, 2 * column_index + i)
                else:
                    add_object(warehouse_object, row_index, column_index)
            map.append(map_row)
        if robot_location is None:
            raise ValueError("Map with no robot!")
        return Warehouse(map, robot_location, box_locations)


def parse(
    lines: Iterable[str], wide: bool = False
) -> tuple[Warehouse, list[Direction]]:
    map_line: bool = True
    directions: list[Direction] = []
    map_lines: list[str] = []
    for line in lines:
        if not line.strip():
            map_line = not map_line
        elif map_line:
            map_lines.append(line)
        else:
            directions.extend(DIRECTIONS[x] for x in line.strip())
    return Warehouse.parse(map_lines, wide), directions


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    with file.open("r") as f:
        warehouse, directions = parse(f)
    for direction in directions:
        warehouse.execute_move(direction)
    gps_total: int = warehouse.gps_coordinate_total()
    print(f"The total of box GPS coordinates is {gps_total}")

    with file.open("r") as f:
        warehouse, directions = parse(f, True)
    for direction in directions:
        warehouse.execute_move(direction)
    wide_gps_total: int = warehouse.gps_coordinate_total()
    print(f"The total of wide box GPS coordinates is {wide_gps_total}")
