import pytest

from lobby import Bank


batteries_with_joltage = [
    ([9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1], 98, 987654321111),
    ([8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9], 89, 811111111119),
    ([2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8], 78, 434234234278),
    ([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1], 92, 888911112111),
]


@pytest.mark.parametrize(
    "batteries,expected_two,expected_twelve", batteries_with_joltage
)
def test_joltage(batteries, expected_two, expected_twelve):
    assert Bank(batteries=batteries).joltage(2) == expected_two
    assert Bank(batteries=batteries).joltage(12) == expected_twelve
