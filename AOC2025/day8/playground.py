import argparse
from dataclasses import dataclass
from heapq import heapify, heappop
from itertools import combinations
from pathlib import Path
from typing import Generator


@dataclass(frozen=True)
class JunctionBox:
    x: int
    y: int
    z: int

    @staticmethod
    def parse(text: str) -> "JunctionBox":
        return JunctionBox(*(int(n) for n in text.split(",")))

    def distance_squared(self, other: "JunctionBox") -> int:
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


class JunctionBoxPair:
    def __init__(self, j1: JunctionBox, j2: JunctionBox):
        self.j1 = j1
        self.j2 = j2
        self.distance_squared = j2.distance_squared(j1)

    def __lt__(self, other):
        return self.distance_squared < other.distance_squared


def closest_pairs(boxes: list[JunctionBox]) -> Generator[JunctionBoxPair, None, None]:
    pairs = [JunctionBoxPair(l1, l2) for l1, l2 in combinations(boxes, 2)]
    heapify(pairs)
    while pairs:
        yield heappop(pairs)


class UnionFind:
    def __init__(self, boxes: list[JunctionBox]):
        self.count = len(boxes)
        self.sizes = {b: 1 for b in boxes}
        self.parents = {b: b for b in boxes}

    def _find_parent(self, box: JunctionBox) -> JunctionBox:
        while box != self.parents[box]:
            box = self.parents[box]
        return box

    def union(self, pair: JunctionBoxPair):
        p1 = self._find_parent(pair.j1)
        p2 = self._find_parent(pair.j2)
        if p1 == p2:
            return
        if self.sizes[p1] < self.sizes[p2]:
            self.parents[p1] = p2
            self.sizes[p2] += self.sizes[p1]
        else:
            self.parents[p2] = p1
            self.sizes[p1] += self.sizes[p2]
        self.count -= 1

    def get_three_largest_component_sizes(self) -> tuple[int, int, int]:
        roots = [p for p in self.parents if self.parents[p] == p]
        sizes = sorted([self.sizes[p] for p in roots])
        a, b, c = sizes[-3:]
        return a, b, c


def connect_until_single_circuit(boxes: list[JunctionBox]) -> JunctionBoxPair:
    pairs = closest_pairs(boxes)
    uf = UnionFind(boxes)
    while True:
        pair = next(pairs)
        uf.union(pair)
        if uf.count == 1:
            return pair


def get_largest_circuits(boxes: list[JunctionBox], n: int) -> tuple[int, int, int]:
    pairs = closest_pairs(boxes)
    uf = UnionFind(boxes)
    for _ in range(n):
        uf.union(next(pairs))
    a, b, c = uf.get_three_largest_component_sizes()
    return a, b, c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    parser.add_argument("iterates", type=int)
    args = parser.parse_args()

    boxes = [JunctionBox.parse(line) for line in args.filename.read_text().splitlines()]
    a, b, c = get_largest_circuits(boxes, args.iterates)
    print(a * b * c)

    pair = connect_until_single_circuit(boxes)
    print(pair.j1.x * pair.j2.x)


if __name__ == "__main__":
    main()
