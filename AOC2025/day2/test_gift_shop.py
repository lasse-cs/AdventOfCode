import pytest

from gift_shop import Range, parse_ranges, sum_doubles, sum_repeats


def test_parse():
    input_str = "95-115"
    assert Range.parse(input_str) == Range(start=95, end=115)


input_ranges_to_doubles = [
    (Range(11, 22), [11, 22]),
    (Range(95, 115), [99]),
    (Range(998, 1012), [1010]),
    (Range(1188511880, 1188511890), [1188511885]),
    (Range(222220, 222224), [222222]),
    (Range(1698522, 1698528), []),
    (Range(1, 99), [11, 22, 33, 44, 55, 66, 77, 88, 99]),
]


@pytest.mark.parametrize("input_range,expected", input_ranges_to_doubles)
def test_doubles(input_range, expected):
    assert input_range.doubles() == expected


def test_parse_ranges():
    input_txt = "11-22,95-115"
    ranges = parse_ranges(input_txt)
    assert ranges == [Range(11, 22), Range(95, 115)]


def test_sum_doubles():
    result = sum_doubles([Range(11, 22), Range(95, 115), Range(1698522, 1698528)])
    assert result == 11 + 22 + 99


def test_sum_repeats():
    result = sum_repeats([Range(11, 22), Range(95, 115), Range(998, 1012)])
    assert result == 11 + 22 + 99 + 111 + 999 + 1010


def test_triples():
    r = Range(565653, 565659)
    threepeats = r.repeats(3)
    assert threepeats == [565656]


def test_fivepeats():
    r = Range(6868676926, 6868700146)
    fivepeats = r.repeats(5)
    assert fivepeats == [6868686868]
