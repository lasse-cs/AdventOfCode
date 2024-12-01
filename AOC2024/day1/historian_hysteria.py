from pathlib import Path
from typing import Tuple
from argparse import ArgumentParser
from collections import defaultdict


def parse(input_file_path: Path) -> Tuple[list[int], list[int]]:
    first_list: list[int] = []
    second_list: list[int] = []
    with input_file_path.open() as f:
        for line in f:
            _parse_line(line, first_list, second_list)
    return first_list, second_list


def _parse_line(line: str, first_list: list[int], second_list: list[int]) -> None:
    split_line: list[str] = line.split(3 * " ")
    first_integer = int(split_line[0])
    first_list.append(first_integer)

    second_integer = int(split_line[1])
    second_list.append(second_integer)


def sort_list(input: list[int]):
    _sort_list(input, 0, len(input) - 1)


def _sort_list(input: list[int], left: int, right: int):
    if left >= right:
        return
    pivot: int = _partition(input, left, right)
    _sort_list(input, left, pivot - 1)
    _sort_list(input, pivot + 1, right)


def _partition(input: list[int], left: int, right: int) -> int:
    pivot_index: int = left
    pivot_element: int = input[right]
    for index in range(left, right):
        if input[index] <= pivot_element:
            input[index], input[pivot_index] = input[pivot_index], input[index]
            pivot_index += 1

    input[pivot_index], input[right] = input[right], input[pivot_index]

    return pivot_index


def calculate_total_distance(
    sorted_list_one: list[int], sorted_list_two: list[int]
) -> int:
    total: int = 0
    for i in range(len(sorted_list_one)):
        total += abs(sorted_list_one[i] - sorted_list_two[i])
    return total


def calculate_list_counts(input: list[int]) -> defaultdict[int, int]:
    counts: defaultdict[int, int] = defaultdict(int)
    for item in input:
        counts[item] += 1
    return counts


def calculate_similarity_score(
    input_list: list[int], counts: defaultdict[int, int]
) -> int:
    total = 0
    for item in input_list:
        total += item * counts[item]
    return total


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    list_one, list_two = parse(file)
    sort_list(list_one)
    sort_list(list_two)
    total = calculate_total_distance(list_one, list_two)
    print(f"The distance is {total}")

    counts = calculate_list_counts(list_two)
    similarity_score = calculate_similarity_score(list_one, counts)
    print(f"The similarity score is {similarity_score}")
