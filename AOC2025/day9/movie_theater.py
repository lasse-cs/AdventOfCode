import argparse
from dataclasses import dataclass
from itertools import combinations, pairwise
from pathlib import Path


@dataclass(frozen=True)
class Tile:
    column: int
    row: int

    @staticmethod
    def parse(text: str) -> "Tile":
        return Tile(*(int(x) for x in text.split(",")))

    def area(self, other: "Tile") -> int:
        return (abs(self.row - other.row) + 1) * (abs(self.column - other.column) + 1)


@dataclass(frozen=True)
class Edge:
    start: Tile
    end: Tile

    def is_vertical(self) -> bool:
        return self.start.column == self.end.column

    def is_horizontal(self) -> bool:
        return self.start.row == self.end.row

    def contains(self, tile: Tile) -> bool:
        if self.is_vertical():
            start_row = min(self.start.row, self.end.row)
            end_row = max(self.start.row, self.end.row)
            return tile.column == self.start.column and start_row <= tile.row <= end_row
        else:
            start_col = min(self.start.column, self.end.column)
            end_col = max(self.start.column, self.end.column)
            return tile.row == self.start.row and start_col <= tile.column <= end_col


def get_edges(tiles: list[Tile]) -> list[Edge]:
    edges = [Edge(t1, t2) for t1, t2 in pairwise(tiles)]
    edges.append(Edge(tiles[-1], tiles[0]))
    return edges


def is_interior_point(tile, edges):
    """
    A point is on the interior if between it and 0
    it has to go through an odd number of boundaries
    or if it lives on an edge
    """
    interior = False
    for edge in edges:
        if edge.contains(tile):
            return True

        if edge.start.column > tile.column:
            continue
        if edge.contains(Tile(row=tile.row, column=edge.start.column)):
            interior = not interior
    return interior


def is_interior_edge(edge, edges):
    """
    Find the X-edges that intersect the given edge.
    Take the midpoint of each segment.
    Check that all are interior.
    """
    if edge.is_vertical():
        edge_start_row = min(edge.start.row, edge.end.row)
        edge_end_row = max(edge.start.row, edge.end.row)
        x_rows = {edge_start_row, edge_end_row}
        edge_column = edge.start.column
        for e in edges:
            if e.is_vertical():
                continue
            if edge_start_row <= e.start.row <= edge_end_row:
                t = Tile(row=e.start.row, column=edge_column)
                if e.contains(t):
                    x_rows.add(e.start.row)
        x_rows = sorted(x_rows)
        mid_points = [(a + b) // 2 for a, b in pairwise(x_rows)]
        return all(
            is_interior_point(Tile(row=x_row, column=edge_column), edges)
            for x_row in mid_points
        )
    elif edge.is_horizontal():
        edge_start_col = min(edge.start.column, edge.end.column)
        edge_end_col = max(edge.start.column, edge.end.column)
        x_cols = {edge_start_col, edge_end_col}
        edge_row = edge.start.row
        for e in edges:
            if e.is_horizontal():
                continue
            if edge_start_col <= e.start.column <= edge_end_col:
                t = Tile(row=edge_row, column=e.start.column)
                if e.contains(t):
                    x_cols.add(e.start.column)
        x_cols = sorted(x_cols)
        mid_points = [(a + b) // 2 for a, b in pairwise(x_cols)]
        return all(
            is_interior_point(Tile(row=edge_row, column=x_col), edges)
            for x_col in mid_points
        )


def get_rectangle_edges(t1, t2) -> list[Edge]:
    t1_is_top = t1.row > t2.row
    t1_is_left = t1.column > t2.column
    if t1_is_top and t1_is_left:
        top_left = t1
        bottom_right = t2
    elif t1_is_top and not t1_is_left:
        top_left = Tile(row=t1.row, column=t2.column)
        bottom_right = Tile(row=t2.row, column=t1.column)
    elif not t1_is_top and t1_is_left:
        top_left = Tile(row=t2.row, column=t1.column)
        bottom_right = Tile(row=t1.row, column=t2.column)
    else:
        top_left = t2
        bottom_right = t1
    top_right = Tile(row=top_left.row, column=bottom_right.column)
    bottom_left = Tile(row=bottom_right.row, column=top_left.column)
    return [
        Edge(top_left, top_right),
        Edge(top_right, bottom_right),
        Edge(bottom_right, bottom_left),
        Edge(bottom_left, top_left),
    ]


def is_interior_rectangle(t1, t2, edges) -> bool:
    """
    The rectangle is interior if all edges are on the interior
    """
    rect_edges = get_rectangle_edges(t1, t2)
    for edge in rect_edges:
        if not is_interior_edge(edge, edges):
            return False
    return True


def get_maximum_area(tiles: list[Tile]) -> int:
    current_max = 0
    for t1, t2 in combinations(tiles, 2):
        area = t1.area(t2)
        if area > current_max:
            current_max = area
    return current_max


def get_maximum_interior_area(tiles: list[Tile]) -> int:
    current_max = 0
    edges = get_edges(tiles)
    for t1, t2 in combinations(tiles, 2):
        area = t1.area(t2)
        if area > current_max:
            if is_interior_rectangle(t1, t2, edges):
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

    max_interior_area = get_maximum_interior_area(tiles)
    print(max_interior_area)


if __name__ == "__main__":
    main()
