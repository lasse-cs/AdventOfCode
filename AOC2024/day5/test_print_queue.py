from pathlib import Path
import pytest
from collections import defaultdict
from print_queue import (
    check_update,
    split_updates_by_correctness,
    correctly_ordered_middle_page_total,
    parse_rule,
    parse_update,
    parse,
)


@pytest.fixture
def rules():
    rule_dict = defaultdict(set)
    rule_dict[47] = {29, 13, 61, 53}
    rule_dict[97] = {75, 13, 47, 61, 53, 29}
    rule_dict[75] = {13, 47, 29, 53, 61}
    rule_dict[61] = {29, 53, 13}
    rule_dict[29] = {13}
    rule_dict[53] = {13, 29}
    return rule_dict


updates_list = [
    [75, 47, 61, 53, 29],
    [97, 61, 53, 29, 13],
    [75, 29, 13],
    [75, 97, 47, 61, 53],
    [61, 13, 29],
    [97, 13, 75, 29, 47],
]


@pytest.fixture
def updates():
    return updates_list


def test_parse_rule():
    rules = ["12|3", "12|4", "4|3"]
    rules_dict = defaultdict(set)
    for rule in rules:
        parse_rule(rule, rules_dict)
    assert {12: {3, 4}, 4: {3}} == dict(rules_dict)


def test_parse_update():
    update_input = "75,47,61,53,29"
    update = parse_update(update_input)
    assert update == [75, 47, 61, 53, 29]


def test_parse(rules, updates):
    input_file = Path(".") / "files" / "test_input.txt"
    parsed_rules, parsed_updates = parse(input_file)
    assert rules == parsed_rules
    assert updates == parsed_updates


@pytest.mark.parametrize(
    argnames=[
        "update",
        "expected_result",
    ],
    argvalues=zip(updates_list, [True, True, True, False, False, False]),
)
def test_check_good_update(rules, update, expected_result):
    result = check_update(update, rules)
    assert result == expected_result


def test_correctly_ordered_middle_page_total(updates, rules):
    correct_updates, _ = split_updates_by_correctness(updates, rules)
    total = correctly_ordered_middle_page_total(correct_updates, rules)
    assert total == 143
