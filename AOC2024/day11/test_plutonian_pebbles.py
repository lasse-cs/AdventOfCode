from plutonian_pebbles import parse, Pebbles, blink, length_after_multiple_blinks


def test_parse() -> None:
    input: str = "0 1 10 99 999"
    parsed: Pebbles = parse(input)
    assert parsed == {0: 1, 1: 1, 10: 1, 99: 1, 999: 1}


def test_one_blink() -> None:
    initial: Pebbles = {0: 1, 1: 1, 10: 1, 99: 1, 999: 1}
    expected: Pebbles = {0: 1, 1: 2, 9: 2, 2024: 1, 2021976: 1}
    assert blink(initial) == expected


def test_length_after_multiple_blinks() -> None:
    initial: Pebbles = {125: 1, 17: 1}
    final_length: int = length_after_multiple_blinks(initial, 25)
    assert final_length == 55312
