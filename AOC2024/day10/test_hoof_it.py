from pathlib import Path
import pytest
from pytest import FixtureRequest
from hoof_it import parse, TopographicMap, CellLocation


@pytest.fixture
def test_map(request: FixtureRequest) -> TopographicMap:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    return parse(file)


@pytest.mark.parametrize(
    argnames=["test_map", "trailhead", "rating"],
    argvalues=[
        ("test_score_four_trailhead_input.txt", CellLocation(0, 3), 13),
        ("test_rating_three_trailhead_input.txt", CellLocation(0, 5), 3),
    ],
    indirect=["test_map"],
)
def test_rating_trailhead(
    test_map: TopographicMap, trailhead: CellLocation, rating: int
):
    assert test_map.rate_trailhead(trailhead) == rating


@pytest.mark.parametrize(
    argnames=["test_map", "rating"],
    argvalues=[
        ("test_rating_input.txt", 227),
        ("test_larger_input.txt", 81),
    ],
    indirect=["test_map"],
)
def test_rating(test_map: TopographicMap, rating: int):
    assert test_map.rate_map() == rating


@pytest.mark.parametrize(
    argnames=["test_map", "score"],
    argvalues=[
        ("test_two_trailheads_input.txt", 3),
        ("test_larger_input.txt", 36),
    ],
    indirect=["test_map"],
)
def test_score_map(test_map: TopographicMap, score: int):
    assert test_map.score_map() == score


@pytest.mark.parametrize(
    argnames=["test_map", "trailhead", "score"],
    argvalues=[
        ("test_score_two_trailhead_input.txt", CellLocation(0, 3), 2),
        ("test_score_four_trailhead_input.txt", CellLocation(0, 3), 4),
    ],
    indirect=["test_map"],
)
def test_score_trailhead(test_map: TopographicMap, trailhead: CellLocation, score: int):
    assert test_map.score_trailhead(trailhead) == score


@pytest.mark.parametrize("test_map", ["test_input.txt"], indirect=True)
def test_parse(test_map: TopographicMap):
    expected_cells = [
        [0, 1, 2, 3],
        [1, 2, 3, 4],
        [8, 7, 6, 5],
        [9, 8, 7, 6],
    ]
    assert test_map._cells == expected_cells
