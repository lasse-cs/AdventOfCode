from resonant_collinearity import parse, Location, Map
from pathlib import Path
import pytest


@pytest.fixture
def simple_sample_input() -> Path:
    return Path(__file__).resolve().parent / "files" / "test_simpler_input.txt"


@pytest.fixture
def sample_input() -> Path:
    return Path(__file__).resolve().parent / "files" / "test_input.txt"


@pytest.fixture
def line_sample_input() -> Path:
    return Path(__file__).resolve().parent / "files" / "test_line_input.txt"


def test_parse(simple_sample_input: Path) -> None:
    parsed_map: Map = parse(simple_sample_input)
    expected_map: Map = Map(10, 10, {"a": [Location(3, 4), Location(5, 5)]})
    assert parsed_map == expected_map


def test_find_point_antinodes(simple_sample_input) -> None:
    map: Map = parse(simple_sample_input)
    antinodes: set[Location] = map.find_point_antinodes()
    assert antinodes == {Location(1, 3), Location(7, 6)}


def test_find_line_antinodes(line_sample_input) -> None:
    map: Map = parse(line_sample_input)
    antinodes: set[Location] = map.find_line_antinodes()
    expected_antinodes = {
        Location(0, 0),
        Location(0, 5),
        Location(1, 3),
        Location(2, 1),
        Location(2, 6),
        Location(3, 9),
        Location(4, 2),
        Location(6, 3),
        Location(8, 4),
    }
    assert antinodes == expected_antinodes


def test_count_antinodes(sample_input) -> None:
    map: Map = parse(sample_input)
    antinodes: set[Location] = map.find_point_antinodes()
    assert len(antinodes) == 14


def test_count_line_antinodes(sample_input) -> None:
    map: Map = parse(sample_input)
    antinodes: set[Location] = map.find_line_antinodes()
    assert len(antinodes) == 34
