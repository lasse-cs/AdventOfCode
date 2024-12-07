from pathlib import Path
import pytest
from bridge_repair import (
    parse_callibration,
    Callibration,
    total_possible_callibrations,
    total_extended_possible_callibrations,
    parse,
    concat,
    EXTENDED_OPERATORS,
)


def test_parse_callibration() -> None:
    input: str = "190: 10 19"
    parsed: Callibration = parse_callibration(input)
    assert parsed == Callibration(190, [10, 19])


@pytest.mark.parametrize(
    argnames=["callibration", "possible"],
    argvalues=[
        (Callibration(190, [10, 19]), True),
        (Callibration(3267, [81, 40, 27]), True),
        (Callibration(83, [17, 5]), False),
        (Callibration(156, [15, 6]), False),
    ],
)
def test_is_callibration_possible(callibration: Callibration, possible: bool):
    actual: bool = callibration.is_possible()
    assert actual == possible


@pytest.mark.parametrize(
    argnames="callibration",
    argvalues=[
        Callibration(156, [15, 6]),
        Callibration(7290, [6, 8, 6, 15]),
        Callibration(192, [17, 8, 14]),
    ],
)
def test_is_extended_callibration_possible(callibration: Callibration):
    assert callibration.is_possible(EXTENDED_OPERATORS)


def test_total_possible_callibrations() -> None:
    file: Path = Path(".") / "files" / "test_input.txt"
    callibrations: list[Callibration] = parse(file)
    total: int = total_possible_callibrations(callibrations)
    assert total == 3749


def test_total_extended_possible_callibrations() -> None:
    file: Path = Path(".") / "files" / "test_input.txt"
    callibrations: list[Callibration] = parse(file)
    total: int = total_extended_possible_callibrations(callibrations)
    assert total == 11387


def test_concat():
    assert concat(12, 345) == 12345
