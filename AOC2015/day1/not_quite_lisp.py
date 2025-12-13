import argparse
from pathlib import Path


def get_final_floor(instructions: str) -> int:
    floor = 0
    for c in instructions:
        floor += 1 if c == "(" else -1
    return floor


def get_first_basement(instructions: str) -> int | None:
    floor = 0
    for idx, c in enumerate(instructions):
        floor += 1 if c == "(" else -1
        if floor == -1:
            return idx + 1
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    final_floor = get_final_floor(text.strip())
    print(final_floor)

    first_basement = get_first_basement(text.strip())
    print(first_basement)


if __name__ == "__main__":
    main()
