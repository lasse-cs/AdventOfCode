from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import TypeAlias


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret % 16777216


def multiply_mix_prune(secret: int, value: int) -> int:
    intermediate: int = secret * value
    intermediate = mix(secret, intermediate)
    return prune(intermediate)


def divide_mix_prune(secret: int, value: int) -> int:
    intermediate: int = secret // value
    intermediate = mix(secret, intermediate)
    return prune(intermediate)


def generate_next_secret(secret: int) -> int:
    secret = multiply_mix_prune(secret, 64)
    secret = divide_mix_prune(secret, 32)
    secret = multiply_mix_prune(secret, 2048)
    return secret


def generate_nth_secret(secret: int, n: int) -> int:
    for _ in range(n):
        secret = generate_next_secret(secret)
    return secret


def sum_nth_secrets(secrets: list[int], n: int) -> int:
    total: int = 0
    for secret in secrets:
        total += generate_nth_secret(secret, n)
    return total


PriceSequence: TypeAlias = tuple[int, int, int, int]


def calculate_banana_sequences_for_secret(
    secret: int, n: int
) -> dict[PriceSequence, int]:
    prices: list[int] = []
    for _ in range(n):
        prices.append(secret % 10)
        secret = generate_next_secret(secret)

    sequences: dict[PriceSequence, int] = {}

    for i in range(4, len(prices)):
        sequence: PriceSequence = (
            prices[i - 3] - prices[i - 4],
            prices[i - 2] - prices[i - 3],
            prices[i - 1] - prices[i - 2],
            prices[i] - prices[i - 1],
        )
        if sequence in sequences:
            continue
        sequences[sequence] = prices[i]
    return sequences


def calculate_best_banana_total(secrets: list[int], n: int) -> int:
    sequence_to_total: dict[PriceSequence, int] = defaultdict(int)

    for secret in secrets:
        secret_sequences: dict[PriceSequence, int] = (
            calculate_banana_sequences_for_secret(secret, n)
        )

        for sequence, bananas in secret_sequences.items():
            sequence_to_total[sequence] += bananas
    return max(sequence_to_total.values())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file: Path = Path(args.filename)

    initial_secrets: list[int] = [int(num) for num in file.read_text().split("\n")]
    sum_secrets: int = sum_nth_secrets(initial_secrets, 2000)
    print(f"The sum of the 2000th secrets is {sum_secrets}")

    best_bananas: int = calculate_best_banana_total(initial_secrets, 2000)
    print(f"The best banana total is {best_bananas}")
