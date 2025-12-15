import argparse
from string import ascii_lowercase


def password_to_numbers(text: str) -> list[int]:
    return [ascii_lowercase.index(c) for c in text]


def numbers_to_password(numbers: list[int]) -> str:
    return "".join(ascii_lowercase[i] for i in numbers)


def check_password(numbers: list[int]) -> bool:
    previous_previous = numbers[0]
    previous = numbers[1]
    pairs: dict[int, int] = {}
    if previous_previous == previous:
        pairs[previous] = 1
    has_two_doubles = False
    has_rise = False
    for index, number in enumerate(numbers[2:], start=2):
        if number in {8, 11, 14}:
            return False
        if number == previous:
            if not has_two_doubles:
                if number in pairs:
                    has_two_doubles = pairs[number] + 1 != index
                else:
                    pairs[number] = index
                    has_two_doubles = len(pairs) > 1
        has_rise = has_rise or number == previous + 1 == previous_previous + 2
        previous_previous = previous
        previous = number
    return has_two_doubles and has_rise


def next_candidate_password(numbers: list[int]) -> list[int]:
    for i, num in enumerate(numbers):
        if num in {8, 11, 14}:
            return numbers[:i] + [num + 1] + [0] * (7 - i)
    carry_over = 1
    result = []
    for num in reversed(numbers):
        if num + carry_over == len(ascii_lowercase):
            result.append(0)
            carry_over = 1
        else:
            result.append(num + carry_over)
            carry_over = 0
    return list(reversed(result))


def next_password(password: str) -> str | None:
    numbers = password_to_numbers(password)
    while numbers := next_candidate_password(numbers):
        if check_password(numbers):
            return numbers_to_password(numbers)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    password = args.input
    next_pw = next_password(password)
    print(next_pw)
    next_next_pw = next_password(next_pw)
    print(next_next_pw)


if __name__ == "__main__":
    main()
