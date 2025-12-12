import argparse
from pathlib import Path


class Shape:
    def __init__(self, shape, index):
        self.index = index
        self.variants = []
        for rotate in [0, 1, 2]:
            for flip_row in [0, 1]:
                for flip_col in [0, 1]:
                    variant = self._get_variant(shape, rotate, flip_row, flip_col)
                    if variant not in self.variants:
                        self.variants.append(variant)
        self.size = self._get_size(shape)

    def _get_size(self, shape):
        count = 0
        for row in shape:
            for c in row:
                count += c
        return count

    def _flip_rows(self, shape):
        return [shape[-1][:], shape[1][:], shape[0][:]]

    def _flip_columns(self, shape):
        return [[row[-1], row[1], row[0]] for row in shape]

    def _rotate_clockwise(self, shape):
        return [
            [shape[2][0], shape[1][0], shape[0][0]],
            [shape[2][1], shape[1][1], shape[0][1]],
            [shape[2][2], shape[1][2], shape[0][2]],
        ]

    def _get_variant(self, shape, rotate, flip_row, flip_col):
        for _ in range(rotate):
            shape = self._rotate_clockwise(shape)
        if flip_row:
            shape = self._flip_rows(shape)
        if flip_col:
            shape = self._flip_columns(shape)
        return shape

    def __str__(self):
        return str(self.variants[0])

    def __repr__(self):
        return repr(self.variants[0])


class Region:
    def __init__(self, width, height, shapes, target):
        self.grid = [[False] * width for _ in range(height)]
        self.rows = height
        self.columns = width
        self.shapes = shapes
        self.target = target

    def size(self):
        return self.rows * self.columns

    def target_size(self):
        count = 0
        for shape in self.shapes:
            count += shape.size * self.target[shape.index]
        return count

    def can_fit(self, row, column, shape):
        if row + 2 >= self.rows or column + 2 >= self.columns:
            return False
        for r_idx, shape_row in enumerate(shape):
            for c_idx, p in enumerate(shape_row):
                if p and self.grid[row + r_idx][column + c_idx]:
                    return False
        return True

    def fill(self, row, column, shape):
        for r_idx, shape_row in enumerate(shape):
            for c_idx, p in enumerate(shape_row):
                if p:
                    self.grid[row + r_idx][column + c_idx] = p

    def unfill(self, row, column, shape):
        for r_idx, shape_row in enumerate(shape):
            for c_idx, p in enumerate(shape_row):
                if p:
                    self.grid[row + r_idx][column + c_idx] = not p

    def can_fit_all(self) -> bool:
        if self.size() < self.target_size():
            return False
        if self.size() // 9 > sum(self.target):
            return True

        if not any(self.target):
            return True

        for row in range(self.rows):
            for column in range(self.columns):
                for shape in self.shapes:
                    if not self.target[shape.index]:
                        continue
                    for variant in shape.variants:
                        if not self.can_fit(row, column, variant):
                            continue
                        self.fill(row, column, variant)
                        self.target[shape.index] -= 1
                        if self.can_fit_all():
                            return True
                        self.target[shape.index] += 1
                        self.unfill(row, column, variant)
        return False

    def __str__(self):
        x = ""
        for row in range(self.rows):
            for column in range(self.columns):
                x += "#" if self.grid[row][column] else "."
            x += "\n"
        return x


def parse(text):
    segments = text.split("\n\n")
    shapes = []
    for idx, shape_segment in enumerate(segments[:-1]):
        lines = shape_segment.splitlines()
        shape = [[x == "#" for x in line] for line in lines[1:]]
        shapes.append(Shape(shape, idx))
    regions = []
    for line in segments[-1].splitlines():
        size, targets = line.split(": ")
        width, height = (int(x) for x in size.split("x"))
        target = [int(x) for x in targets.split(" ")]
        regions.append(Region(width, height, shapes, target))
    return regions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    regions = parse(text)
    count = 0
    for region in regions:
        count += region.can_fit_all()
    print(count)


if __name__ == "__main__":
    main()
