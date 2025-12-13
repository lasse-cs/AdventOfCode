import pytest
from perfectly_spherical_houses_in_a_vacuum import (
    get_houses_santa,
    get_houses_santa_and_robo_santa,
)


instructions_with_expected = [
    (">", 2, 2),
    ("^>v<", 4, 3),
    ("^v^v^v^v^v", 2, 11),
]


@pytest.mark.parametrize("instructions,expected,robo", instructions_with_expected)
def test_get_houses(instructions, expected, robo):
    assert get_houses_santa(instructions) == expected
    assert get_houses_santa_and_robo_santa(instructions) == robo
