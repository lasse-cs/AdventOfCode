import pytest
from movie_theater import (
    Edge,
    Tile,
    get_maximum_area,
    get_maximum_interior_area,
    get_edges,
    is_interior_edge,
    is_interior_point,
    is_interior_rectangle,
)


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


def test_get_maximum_interior_area(tiles: list[Tile]):
    assert get_maximum_interior_area(tiles) == 24


def test_is_interior_edge(tiles: list[Tile]):
    edges = get_edges(tiles)
    tstart = Tile(row=5, column=2)
    tend = Tile(row=3, column=2)
    edge = Edge(tstart, tend)
    assert is_interior_edge(edge, edges)


def test_edge_contains():
    edge = Edge(start=Tile(column=2, row=5), end=Tile(column=2, row=3))
    t = Tile(column=2, row=4)
    assert edge.contains(t)


def test_is_interior_point(tiles: list[Tile]):
    edges = get_edges(tiles)
    tile = Tile(row=4, column=2)
    assert is_interior_point(tile, edges)


def test_is_interior_rectangle(tiles: list[Tile]):
    edges = get_edges(tiles)
    t1 = Tile(row=3, column=2)
    t2 = Tile(row=5, column=9)
    assert is_interior_rectangle(t1, t2, edges)


def test_is_not_interior_rectangle(tiles: list[Tile]):
    edges = get_edges(tiles)
    t1 = Tile(column=11, row=7)
    t2 = Tile(column=2, row=3)
    assert not is_interior_rectangle(t1, t2, edges)


def test_is_not_interior_edge(tiles: list[Tile]):
    edges = get_edges(tiles)
    t1 = Tile(column=11, row=7)
    t2 = Tile(column=2, row=7)
    edge = Edge(t1, t2)
    assert not is_interior_edge(edge, edges)


def test_is_not_interior_point(tiles: list[Tile]):
    edges = get_edges(tiles)
    t = Tile(column=5, row=7)
    assert not is_interior_point(t, edges)
