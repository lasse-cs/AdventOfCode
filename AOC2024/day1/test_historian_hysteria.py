from pathlib import Path
from historian_hysteria import (
    parse,
    sort_list,
    calculate_total_distance,
    calculate_list_counts,
    calculate_similarity_score,
)


def test_parse():
    test_file = Path(".") / "files" / "test_input.txt"
    first_parsed_list, second_parsed_list = parse(test_file)
    assert first_parsed_list == [3, 4, 2, 1, 3, 3]
    assert second_parsed_list == [4, 3, 5, 3, 9, 3]


def test_sort_list():
    the_list = [3, 4, 2, 1, 3, 3]
    sort_list(the_list)
    assert the_list == sorted(the_list)


def test_calculate_total_distance():
    first_list = [1, 2, 3, 3, 3, 4]
    second_list = [3, 3, 3, 4, 5, 9]
    total = calculate_total_distance(first_list, second_list)
    assert total == 11


def test_calculate_list_counts():
    input_list = [4, 3, 5, 3, 9, 3]
    counts = {3: 3, 4: 1, 5: 1, 9: 1}
    calculated_counts = dict(calculate_list_counts(input_list))
    assert calculated_counts == counts


def test_calculate_similarity_score():
    input_list = [3, 4, 2, 1, 3, 3]
    counts = calculate_list_counts([4, 3, 5, 3, 9, 3])
    similarity_score = calculate_similarity_score(input_list, counts)
    assert similarity_score == 31
