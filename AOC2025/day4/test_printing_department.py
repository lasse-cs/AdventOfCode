import pytest

from printing_department import Grid, Location


@pytest.fixture
def grid() -> Grid:
    return Grid.parse(
        """..@@.@@@@.
        @@@.@.@.@@
        @@@@@.@.@@
        @.@@@@..@.
        @@.@@@@.@@
        .@@@@@@@.@
        .@.@.@.@@@
        @.@@@.@@@@
        .@@@@@@@@.
        @.@.@@@.@."""
    )


def test_parse_grid():
    text = "@..\n@.@"
    assert Grid.parse(text).grid == [
        [Location.ROLL, Location.FREE, Location.FREE],
        [Location.ROLL, Location.FREE, Location.ROLL],
    ]


def test_roll_count_neighbours(grid: Grid):
    assert grid.count_roll_neighbours(0, 0) == 2
    assert grid.count_roll_neighbours(1, 1) == 6


def test_is_accessible(grid: Grid):
    assert grid.is_accessible(0, 2)
    assert not grid.is_accessible(1, 1)


def test_accessible_count(grid: Grid):
    assert grid.count_accessible_rolls() == 13


def test_all_accessible_count(grid: Grid):
    assert grid.count_all_accessible_rolls() == 43
