import pytest
from movie_theater import Tile, get_maximum_area


@pytest.fixture
def tiles() -> list[Tile]:
    text = """7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3
    """
    return [Tile.parse(x.strip()) for x in text.splitlines() if x.strip()]


def test_parse():
    text = "7,3"
    assert Tile.parse(text) == Tile(row=3, column=7)


def test_maximum_area(tiles: list[Tile]):
    assert get_maximum_area(tiles) == 50
