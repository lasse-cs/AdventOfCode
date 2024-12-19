from pathlib import Path
import pytest
from pytest import FixtureRequest
from linen_layout import (
    parse,
    count_possibilities,
    count_possibles,
)


@pytest.fixture
def towels() -> list[str]:
    return ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]


@pytest.fixture
def parsed_towels(request: FixtureRequest) -> tuple[list[str], list[str]]:
    filename: str = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        return parse(f)


@pytest.mark.parametrize("parsed_towels", ("test_input.txt",), indirect=True)
def test_parse(parsed_towels: tuple[list[str], list[str]], towels: list[str]):
    expected_patterns: list[str] = [
        "brwrr",
        "bggr",
        "gbbr",
        "rrbgbr",
        "ubwu",
        "bwurrg",
        "brgr",
        "bbrgwb",
    ]
    assert parsed_towels == (towels, expected_patterns)


@pytest.mark.parametrize("parsed_towels", ("test_input.txt",), indirect=True)
def test_count_possibles(parsed_towels: tuple[list[str], list[str]]):
    assert count_possibles(*parsed_towels) == 6


@pytest.mark.parametrize("parsed_towels", ("test_input.txt",), indirect=True)
def test_count_total_possibilities(parsed_towels: tuple[list[str], list[str]]):
    total_possibilities: int = count_possibilities(*parsed_towels)
    assert total_possibilities == 16
