from argparse import ArgumentParser
from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass
class Network:
    def __init__(self, connections: dict[str, set[str]]):
        self.connections: dict[str, set[str]] = connections

    def find_mutual_triples(self) -> Iterator[tuple[str, str, str]]:
        checked: set[str] = set()
        for person, connection_set in self.connections.items():
            for pair in combinations(connection_set.difference(checked), 2):
                triple: tuple[str, str, str] = (person, *pair)
                if self.are_mutually_connected(triple):
                    yield triple
            checked.add(person)

    def find_mutual_triples_with_t(self) -> Iterator[tuple[str, str, str]]:
        for triple in self.find_mutual_triples():
            if any(x[0] == "t" for x in triple):
                yield triple

    def find_maximal_mutual_component(self) -> list[str]:
        current_max: list[str] = []
        checked: set[str] = set()
        for person, connection_set in self.connections.items():
            difference: set[str] = connection_set.difference(checked)
            for current_num in range(len(current_max), len(difference) + 1):
                for group in combinations(difference, current_num):
                    complete_group: list[str] = [person, *group]
                    if self.are_mutually_connected(complete_group):
                        current_max = list(complete_group)
                        break
            checked.add(person)
        return current_max

    def format_maximal_mutual(self, group: list[str]) -> str:
        return ",".join(sorted(group))

    def are_mutually_connected(self, items: Iterable[str]) -> bool:
        for item_a, item_b in combinations(items, 2):
            if item_b not in self.connections[item_a]:
                return False
        return True

    @staticmethod
    def parse(lines: Iterator[str]) -> "Network":
        connections: dict[str, set[str]] = defaultdict(set)
        for line in lines:
            first, second = line.strip().split("-")
            connections[first].add(second)
            connections[second].add(first)
        return Network(dict(connections))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file: Path = Path(args.filename)

    with file.open("r") as f:
        network: Network = Network.parse(f)

    mutual_triples: int = len(list(network.find_mutual_triples_with_t()))
    print(f"The number of mutual triples with t is {mutual_triples}")
    maximal_mutual: list[str] = network.find_maximal_mutual_component()
    max: str = network.format_maximal_mutual(maximal_mutual)
    print(f"The maximal mutual component is {max}")
