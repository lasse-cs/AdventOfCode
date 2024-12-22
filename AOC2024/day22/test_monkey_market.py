import pytest
from monkey_market import (
    mix,
    prune,
    generate_next_secret,
    generate_nth_secret,
    sum_nth_secrets,
    PriceSequence,
    calculate_banana_sequences_for_secret,
    calculate_best_banana_total,
)


def test_mix() -> None:
    secret: int = 42
    value: int = 15
    assert mix(secret, value) == 37


def test_prune() -> None:
    secret: int = 100_000_000
    assert prune(secret) == 16_113_920


def test_generate_next_secret() -> None:
    secret: int = 123
    results: list[int] = []
    for _ in range(10):
        secret = generate_next_secret(secret)
        results.append(secret)
    expected = [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]
    assert results == expected


@pytest.mark.parametrize(
    ["initial_secret", "expected"],
    [
        (1, 8_685_429),
        (10, 4_700_978),
        (100, 15_273_692),
        (2024, 8_667_524),
    ],
)
def test_generate_n_secret(initial_secret: int, expected: int) -> None:
    secret: int = generate_nth_secret(initial_secret, 2000)
    assert secret == expected


def test_sum_nth_secrets() -> None:
    secrets: list[int] = [1, 10, 100, 2024]
    sum: int = sum_nth_secrets(secrets, 2000)
    assert sum == 37_327_623


def test_calculate_banana_sequences_for_secret() -> None:
    secret: int = 123
    sequence_bananas: dict[PriceSequence, int] = calculate_banana_sequences_for_secret(
        secret, 10
    )
    assert sequence_bananas[(-1, -1, 0, 2)] == 6
    assert max(sequence_bananas.values()) == 6


def test_calculate_best_banana_total() -> None:
    secrets: list[int] = [1, 2, 3, 2024]
    best_total: int = calculate_best_banana_total(secrets, 2000)
    assert best_total == 23
