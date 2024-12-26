import pytest
from keypad_conundrum import NumericKeypad, DirectionalKeypad, KeypadCollection


@pytest.mark.parametrize(
    ["start", "end", "expected"],
    [
        ("A", "9", {"^^^"}),
        ("A", "7", {"^^^<<"}),
        ("3", "7", {"^^<<", "<<^^"}),
    ],
)
def test_shortest_paths_numeric(start: str, end: str, expected: set[str]) -> None:
    numeric: NumericKeypad = NumericKeypad()
    shortest: set[str] = numeric.get_shortest_paths_between(start, end)
    assert shortest == expected


@pytest.mark.parametrize(
    ["start", "end", "expected"],
    [
        ("A", "<", {"v<<"}),
        ("<", "A", {">>^"}),
        ("A", "v", {"<v", "v<"}),
    ],
)
def test_shortest_paths_directional(start: str, end: str, expected: set[str]) -> None:
    directional: DirectionalKeypad = DirectionalKeypad()
    shortest: set[str] = directional.get_shortest_paths_between(start, end)
    assert shortest == expected


@pytest.mark.parametrize(
    ["sequence", "expected"],
    [
        ("029A", 68),
        ("980A", 60),
        ("179A", 68),
        ("456A", 64),
        ("379A", 64),
    ],
)
def test_get_minimum_keys_for_sequence(sequence: str, expected: int) -> None:
    collection: KeypadCollection = KeypadCollection(2)
    assert collection.get_minimum_keys_for_sequence(sequence) == expected


def test_get_total_complexity_for_sequences() -> None:
    collection: KeypadCollection = KeypadCollection(2)
    sequences: list[str] = ["029A", "980A", "179A", "456A", "379A"]
    total: int = collection.get_total_complexity_for_sequences(sequences)
    assert total == 126384
