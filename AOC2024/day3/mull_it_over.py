from re import Pattern, compile
from pathlib import Path
from argparse import ArgumentParser


def tally_mults(input: str, logic: bool = False) -> int:
    mult_pattern_string: Pattern = compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    logic_pattern: Pattern = compile(r"do(n't)?")
    index: int = 0
    enabled: bool = True
    total = 0
    while index < len(input):
        current_char = input[index]
        if current_char == "m":
            match = mult_pattern_string.match(input, index, index + 12)
            if match is None:
                index += 1
                continue
            if enabled:
                total += int(match.group(1)) * int(match.group(2))
            index = match.end()
        elif logic and input[index] == "d":
            match = logic_pattern.match(input, index, index + 5)
            if match is None:
                index += 1
                continue
            enabled = match.group() == "do"
            index = match.end()
        else:
            index += 1
    return total


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    input: str = file.read_text()
    total: int = tally_mults(input)
    print(f"The total is {total}")

    total_with_logic = tally_mults(input, logic=True)
    print(f"The total with logic is {total_with_logic}")
