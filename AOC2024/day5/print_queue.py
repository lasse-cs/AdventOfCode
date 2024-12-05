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
        if number not in rules[prev_number]:
            return False
    return True


def _get_middle_number(update: Update) -> int:
    mid_index: int = len(update) // 2
    return update[mid_index]


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


def correctly_ordered_middle_page_total(
    correct_updates: list[Update], rules: Rules
) -> int:
    total: int = 0
    for update in correct_updates:
        total += _get_middle_number(update)
    return total


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    rules, updates = parse(file)
    correct_updates, incorrect_updates = split_updates_by_correctness(updates, rules)
    total = correctly_ordered_middle_page_total(correct_updates, rules)
    print(f"The total for the correctly ordered middle pages is {total}")
