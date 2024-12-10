from pathlib import Path
import pytest
from hoof_it import parse, TopographicMap, CellLocation


@pytest.fixture
def test_map() -> TopographicMap:
    file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    return parse(file)


@pytest.fixture
def test_score_two_trailhead_map() -> TopographicMap:
    file: Path = (
        Path(__file__).resolve().parent / "files" / "test_score_two_trailhead_input.txt"
    )
    return parse(file)


@pytest.fixture
def test_larger_map() -> TopographicMap:
    file: Path = Path(__file__).resolve().parent / "files" / "test_larger_input.txt"
    return parse(file)


@pytest.fixture
def test_score_four_trailhead_map() -> TopographicMap:
    file: Path = (
        Path(__file__).resolve().parent
        / "files"
        / "test_score_four_trailhead_input.txt"
    )
    return parse(file)


@pytest.fixture
def test_two_trailheads_map() -> TopographicMap:
    file: Path = (
        Path(__file__).resolve().parent / "files" / "test_two_trailheads_input.txt"
    )
    return parse(file)


def test_two_trailheads_score_map(test_two_trailheads_map: TopographicMap):
    assert test_two_trailheads_map.score_map() == 3


def test_score_map(test_larger_map: TopographicMap):
    assert test_larger_map.score_map() == 36


def test_score_two_trailhead(test_score_two_trailhead_map: TopographicMap):
    assert test_score_two_trailhead_map.score_trailhead(CellLocation(0, 3))


def test_score_four_trailhead(test_score_four_trailhead_map: TopographicMap):
    assert test_score_four_trailhead_map.score_trailhead(CellLocation(0, 3))


def test_parse(test_map: TopographicMap):
    expected_cells = [
        [0, 1, 2, 3],
        [1, 2, 3, 4],
        [8, 7, 6, 5],
        [9, 8, 7, 6],
    ]
    assert test_map._cells == expected_cells
