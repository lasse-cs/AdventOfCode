import pytest
from mull_it_over import tally_mults


@pytest.mark.parametrize(
    argnames=["first_number", "second_number"],
    argvalues=[
        (44, 46),
        (123, 4),
        (123, 123),
    ],
)
def test_valid_matches(first_number: int, second_number: int):
    extracted = tally_mults(f"mul({first_number},{second_number})")
    assert extracted == first_number * second_number


@pytest.mark.parametrize(
    argnames=["input"],
    argvalues=[
        ("mul(4*",),
        ("mul(6,9!",),
        ("?(12,34)",),
        ("mul ( 2 , 4 )",),
    ],
)
def test_invalid_matches(input: str):
    extracted = tally_mults(input)
    assert extracted == 0


def test_match_memory_string():
    extracted = tally_mults(
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    assert extracted == 161


def test_match_memory_string_with_logic():
    extracted = tally_mults(
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
        logic=True,
    )
    assert extracted == 48
