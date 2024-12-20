from pathlib import Path
import pytest
from pytest import FixtureRequest
from race_condition import Cell, Location, RaceTrack, RacePath


@pytest.fixture
def race_track(request: FixtureRequest):
    file_name = request.param
    file: Path = Path(__file__).resolve().parent / "files" / file_name
    with file.open("r") as f:
        return RaceTrack.parse(f)


@pytest.mark.parametrize("race_track", ("test_small_input.txt",), indirect=True)
def test_parse(race_track: RaceTrack):
    expected_cells: list[list[Cell]] = [
        [
            Cell.WALL,
            Cell.WALL,
            Cell.WALL,
            Cell.WALL,
        ],
        [
            Cell.WALL,
            Cell.TRACK,
            Cell.END,
            Cell.WALL,
        ],
        [
            Cell.WALL,
            Cell.START,
            Cell.WALL,
            Cell.WALL,
        ],
        [
            Cell.WALL,
            Cell.WALL,
            Cell.WALL,
            Cell.WALL,
        ],
    ]
    assert race_track.cells == expected_cells
    assert race_track.start == Location(2, 1)
    assert race_track.end == Location(1, 2)


@pytest.mark.parametrize("race_track", ("test_small_input.txt",), indirect=True)
def test_get_path(race_track: RaceTrack):
    path: RacePath = race_track.get_path()
    expected_path: RacePath = {Location(1, 2): 0, Location(1, 1): 1, Location(2, 1): 2}
    assert path == expected_path


@pytest.mark.parametrize("race_track", ("test_input.txt",), indirect=True)
def test_cheat_counts(race_track: RaceTrack):
    path: RacePath = race_track.get_path()
    cheat_counts: dict[int, int] = race_track.get_cheat_counts(path, 1)
    expected_counts: dict[int, int] = {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
    assert cheat_counts == expected_counts


@pytest.mark.parametrize("race_track", ("test_input.txt",), indirect=True)
def test_extra_cheat_counts(race_track: RaceTrack):
    path: RacePath = race_track.get_path()
    cheat_counts: dict[int, int] = race_track.get_cheat_counts(path, 50, True)
    expected_counts: dict[int, int] = {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }
    assert cheat_counts == expected_counts
