from argparse import ArgumentParser
from collections import defaultdict, deque
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple, Optional


class Direction(NamedTuple):
    row: int
    column: int


DIRECTIONS: dict[Direction, str] = {
    Direction(-1, 0): "^",
    Direction(0, 1): ">",
    Direction(1, 0): "v",
    Direction(0, -1): "<",
}


class Position(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "Position":
        return Position(self.row + direction.row, self.column + direction.column)


class State(NamedTuple):
    position: Position
    direction_key: str | None = None
    previous: Optional["State"] = None

    def to_direction_sequence(self) -> str:
        current: State | None = self
        directions: list[str] = []
        while current is not None:
            if current.direction_key is not None:
                directions.append(current.direction_key)
            current = current.previous
        directions.reverse()
        return "".join(directions)


class Keypad:
    def __init__(self, keys: list[list[str]]) -> None:
        self.keys: list[list[str]] = keys
        self.keys_to_position: dict[str, Position] = {}
        for row_index, row in enumerate(self.keys):
            for column_index, k in enumerate(row):
                if k == ".":
                    continue
                self.keys_to_position[k] = Position(row_index, column_index)

    def get_shortest_paths_between(
        self, start_key: str, destination_key: str
    ) -> set[str]:
        start: Position = self.keys_to_position[start_key]
        destination: Position = self.keys_to_position[destination_key]

        frontier: deque[State] = deque()
        frontier.append(State(start))
        results: set[str] = set()
        while len(frontier) > 0:
            frontier_length: int = len(frontier)

            for _ in range(frontier_length):
                current: State = frontier.popleft()
                current_position: Position = current.position
                if current_position == destination:
                    path: str = current.to_direction_sequence()
                    if _swap_score(path) > 1:
                        continue
                    results.add(path)

                for direction in DIRECTIONS:
                    next_position: Position = current_position.move_in(direction)

                    if not self._is_on_board(next_position):
                        continue

                    next_state: State = State(
                        next_position, DIRECTIONS[direction], current
                    )
                    frontier.append(next_state)

            if len(results) > 0:
                break

        return results

    def _is_on_board(self, position: Position) -> bool:
        if position.row < 0 or position.row >= len(self.keys):
            return False
        if position.column < 0 or position.column >= len(self.keys[position.row]):
            return False
        return self.keys[position.row][position.column] != "."


def _swap_score(input: str) -> int:
    score: int = 0
    for a, b in pairwise(input):
        if a != b:
            score += 1
    return score


class NumericKeypad(Keypad):
    def __init__(self) -> None:
        keys: list[list[str]] = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [".", "0", "A"],
        ]
        super().__init__(keys)


class DirectionalKeypad(Keypad):
    def __init__(self) -> None:
        keys: list[list[str]] = [
            [".", "^", "A"],
            ["<", "v", ">"],
        ]
        super().__init__(keys)


class KeypadCollection:
    def __init__(self, num_robots_directionals: int) -> None:
        keypads: list[Keypad] = [NumericKeypad()]
        keypads.extend(num_robots_directionals * [DirectionalKeypad()])
        self.keypads: list[Keypad] = keypads

    def get_minimum_keys_for_sequence(self, sequence: str) -> int:
        sequence = "A" + sequence
        counts: dict[tuple[str, str], int] = defaultdict(int)
        for pair in pairwise(sequence):
            counts[pair] += 1

        for keypad in self.keypads:
            next_counts: dict[tuple[str, str], int] = defaultdict(int)
            for pair, count in counts.items():
                shortest_set: set[str] = keypad.get_shortest_paths_between(*pair)
                shortest: str = self._select_best_key(shortest_set)
                for p in pairwise("A" + shortest + "A"):
                    next_counts[p] += count
            counts = next_counts
        return sum(counts.values())

    def _select_best_key(self, shortest_set: set[str]) -> str:
        if len(shortest_set) == 1:
            return shortest_set.pop()

        # If there are multiple, choose "<" first if possible for best sequences.
        # Else, choose ">" last I think
        assert len(shortest_set) == 2
        first: str = shortest_set.pop()
        second: str = shortest_set.pop()
        if "<" in first:
            return first if first[0] == "<" else second
        else:
            return second if first[0] == ">" else first

    def get_complexity_for_sequence(self, sequence: str) -> int:
        return int(sequence[:-1]) * self.get_minimum_keys_for_sequence(sequence)

    def get_total_complexity_for_sequences(self, sequences: list[str]) -> int:
        return sum(self.get_complexity_for_sequence(s) for s in sequences)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)
    sequences = file.read_text().split("\n")
    collection: KeypadCollection = KeypadCollection(2)
    total_complexity: int = collection.get_total_complexity_for_sequences(sequences)
    print(
        f"The total complexity of the sequences is {total_complexity} for 2 directional robots"
    )

    collection = KeypadCollection(25)
    total_complexity = collection.get_total_complexity_for_sequences(sequences)
    print(
        f"The total complexity of the sequences is {total_complexity} for 25 directional robots"
    )
