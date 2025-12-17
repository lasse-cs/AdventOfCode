import argparse
from itertools import permutations, pairwise
from pathlib import Path
import re


CONNECTION_REGEX = (
    r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)"
)


def parse_connections(text: str) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for line in text.splitlines():
        connection_match = re.match(CONNECTION_REGEX, line.strip())
        if not connection_match:
            raise ValueError
        first_person = connection_match.group(1)
        gain = connection_match.group(2) == "gain"
        amount = int(connection_match.group(3))
        second_person = connection_match.group(4)
        if first_person not in result:
            result[first_person] = {}
        result[first_person][second_person] = amount if gain else -amount
    return result


def calculate_total_happiness(
    arrangement: tuple, connections: dict[str, dict[str, int]]
) -> int:
    total = 0
    for p1, p2 in pairwise(arrangement):
        total += connections[p1][p2] + connections[p2][p1]
    total += (
        connections[arrangement[0]][arrangement[-1]]
        + connections[arrangement[-1]][arrangement[0]]
    )
    return total


def calculate_maximum_happiness(connections: dict[str, dict[str, int]]):
    maximum = None
    for arrangement in permutations(connections):
        happiness = calculate_total_happiness(arrangement, connections)
        if maximum is None or maximum < happiness:
            maximum = happiness
    return maximum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()

    connections = parse_connections(text)
    maximum_happiness = calculate_maximum_happiness(connections)
    print(maximum_happiness)

    people = list(connections)
    connections["me"] = {}
    for person in people:
        connections[person]["me"] = 0
        connections["me"][person] = 0
    maximum_happiness = calculate_maximum_happiness(connections)
    print(maximum_happiness)


if __name__ == "__main__":
    main()
