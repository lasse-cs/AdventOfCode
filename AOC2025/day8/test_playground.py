import pytest

from playground import (
    closest_pairs,
    connect_until_single_circuit,
    get_largest_circuits,
    JunctionBox,
)


@pytest.fixture
def junction_boxes() -> list[JunctionBox]:
    text = """162,817,812
    57,618,57
    906,360,560
    592,479,940
    352,342,300
    466,668,158
    542,29,236
    431,825,988
    739,650,466
    52,470,668
    216,146,977
    819,987,18
    117,168,530
    805,96,715
    346,949,466
    970,615,88
    941,993,340
    862,61,35
    984,92,344
    425,690,689"""
    return [JunctionBox.parse(line) for line in text.splitlines()]


def test_parse_junction_box():
    assert JunctionBox.parse("1,2,3") == JunctionBox(x=1, y=2, z=3)


def test_distance():
    j1 = JunctionBox(1, 2, 3)
    j2 = JunctionBox(3, 0, 1)
    assert j1.distance_squared(j2) == 12
    assert j2.distance_squared(j1) == 12


def test_closes_pairs(junction_boxes: list[JunctionBox]):
    pairs = closest_pairs(junction_boxes)
    pair = next(pairs)
    assert {pair.j1, pair.j2} == {
        JunctionBox(162, 817, 812),
        JunctionBox(425, 690, 689),
    }
    pair = next(pairs)
    assert {pair.j1, pair.j2} == {
        JunctionBox(162, 817, 812),
        JunctionBox(431, 825, 988),
    }


def test_get_closest_after_connections(junction_boxes: list[JunctionBox]):
    assert get_largest_circuits(junction_boxes, 10) == (2, 4, 5)


def test_connect_until_single_circuit(junction_boxes: list[JunctionBox]):
    pair = connect_until_single_circuit(junction_boxes)
    assert {pair.j1, pair.j2} == {
        JunctionBox(216, 146, 977),
        JunctionBox(117, 168, 530),
    }
