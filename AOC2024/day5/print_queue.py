from collections import defaultdict
from pathlib import Path
from argparse import ArgumentParser

Rules = defaultdict[int, set[int]]
Update = list[int]


def parse_rule(input: str, rules: Rules):
    split_input: list[int] = [int(x) for x in input.split("|")]
    rules[split_input[0]].add(split_input[1])


def parse_update(input: str) -> Update:
    return [int(x) for x in input.split(",")]


def parse(file: Path) -> tuple[Rules, list[Update]]:
    rules: Rules = defaultdict(set)
    updates = []
    with open(file, "r") as f:
        is_rule: bool = True
        for line in f:
            stripped_line: str = line.strip()
            if stripped_line == "":
                is_rule = False
                continue

            if is_rule:
                parse_rule(stripped_line, rules)
            else:
                updates.append(parse_update(stripped_line))
    return rules, updates


def check_update(update: Update, rules: Rules) -> bool:
    for index in range(1, len(update)):
        prev_number = update[index - 1]
        number = update[index]
        if not _page_before_other_page(prev_number, number, rules):
            return False
    return True


def _page_before_other_page(page: int, other_page: int, rules: Rules) -> bool:
    return other_page in rules[page]


def _get_middle_number(update: Update) -> int:
    mid_index: int = len(update) // 2
    return update[mid_index]


def quick_select_middle(update: Update, rules: Rules) -> int:
    return _quick_select(update, rules, 0, len(update) - 1)


def _quick_select(update: Update, rules: Rules, left: int, right: int) -> int:
    if right == left:
        return update[left]
    pivot_index: int = _partition(update, rules, left, right)
    if pivot_index == len(update) // 2:
        return update[pivot_index]
    elif pivot_index < len(update) // 2:
        return _quick_select(update, rules, pivot_index + 1, right)
    else:
        return _quick_select(update, rules, left, pivot_index - 1)


def _partition(update: Update, rules: Rules, left: int, right: int) -> int:
    pivot_index = left
    pivot_page = update[right]
    for i in range(left, right):
        if update[i] == pivot_page or _page_before_other_page(
            update[i], pivot_page, rules
        ):
            update[i], update[pivot_index] = update[pivot_index], update[i]
            pivot_index += 1
    update[pivot_index], update[right] = update[right], update[pivot_index]
    return pivot_index


def split_updates_by_correctness(
    updates: list[Update], rules: Rules
) -> tuple[list[Update], list[Update]]:
    correct_updates = []
    incorrect_updates = []
    for update in updates:
        if check_update(update, rules):
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)
    return correct_updates, incorrect_updates


def correctly_ordered_middle_page_total(correct_updates: list[Update]) -> int:
    total: int = 0
    for update in correct_updates:
        total += _get_middle_number(update)
    return total


def incorrectly_ordered_middle_page_total(
    incorrect_updates: list[Update], rules
) -> int:
    total: int = 0
    for update in incorrect_updates:
        total += quick_select_middle(update, rules)
    return total


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    rules, updates = parse(file)
    correct_updates, incorrect_updates = split_updates_by_correctness(updates, rules)
    correct_total = correctly_ordered_middle_page_total(correct_updates)
    print(f"The total for the correctly ordered middle pages is {correct_total}")

    incorrect_total = incorrectly_ordered_middle_page_total(incorrect_updates, rules)
    print(f"The total for the incorrectly ordered middle pages is {incorrect_total}")
