import pytest

from factory import bit_pattern_from_indicator, Button, ManualLine


@pytest.fixture()
def manual_lines():
    l1 = ManualLine.parse("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")
    l2 = ManualLine.parse(
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
    )
    l3 = ManualLine.parse(
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    )
    return [l1, l2, l3]


@pytest.fixture
def manual_line():
    text = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    return ManualLine.parse(text)


def test_bit_pattern_from_indicator():
    text = "[.##.]"
    assert bit_pattern_from_indicator(text) == 0b0110
    text = "[.###.#]"
    assert bit_pattern_from_indicator(text) == 0b101110


def test_parse_button():
    text = "(3)"
    assert Button.parse(text) == Button([3], 0b1000)
    text = "(2, 3)"
    assert Button.parse(text) == Button([2, 3], 0b1100)


def test_parse(manual_line):
    assert manual_line == ManualLine(
        0b0110,
        [
            Button([3], 0b1000),
            Button([1, 3], 0b1010),
            Button([2], 0b100),
            Button([2, 3], 0b1100),
            Button([0, 2], 0b101),
            Button([0, 1], 0b11),
        ],
        (3, 5, 4, 7),
    )


def test_minimum_to_configure(manual_lines):
    assert [ml.minimum_to_configure() for ml in manual_lines] == [2, 3, 2]


def test_minimum_to_get_joltage(manual_lines):
    assert [ml.minimum_to_get_joltage() for ml in manual_lines] == [10, 12, 11]
