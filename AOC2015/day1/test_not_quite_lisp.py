import pytest
from not_quite_lisp import get_final_floor, get_first_basement


instructions_with_floors = [
    ("(())", 0),
    ("()()", 0),
    ("(((", 3),
    ("(()(()(", 3),
    ("))(((((", 3),
    ("())", -1),
    ("))(", -1),
    (")))", -3),
    (")())())", -3),
]


@pytest.mark.parametrize("instructions,expected", instructions_with_floors)
def test_get_final_floor(instructions, expected):
    assert get_final_floor(instructions) == expected


def test_get_first_basement():
    assert get_first_basement(")") == 1
    assert get_first_basement("()())") == 5
