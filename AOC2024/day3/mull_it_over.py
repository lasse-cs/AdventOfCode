from re import Pattern, compile
from pathlib import Path
from argparse import ArgumentParser


def tally_mults(input: str, logic: bool = False) -> int:
    mult_pattern: Pattern = compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    logic_pattern: Pattern = compile(r"do(n't)?")
    index: int = 0
    enabled: bool = True
    total = 0
    while index < len(input):
        current_char = input[index]
        match = None
        if current_char == "m":
            match = mult_pattern.match(input, index, index + 12)
            if enabled and match is not None:
                total += int(match.group(1)) * int(match.group(2))
        elif logic and current_char == "d":
            match = logic_pattern.match(input, index, index + 5)
            if match is not None:
                enabled = match.group() == "do"

        if match is None:
            index += 1
        else:
            index = match.end()
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
