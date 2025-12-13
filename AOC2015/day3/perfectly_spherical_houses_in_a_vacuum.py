import argparse
from pathlib import Path


def _move(position: list[int], instruction: str):
    if instruction == ">":
        position[1] += 1
    elif instruction == "<":
        position[1] -= 1
    elif instruction == "v":
        position[0] += 1
    elif instruction == "^":
        position[0] -= 1


def get_houses_santa(instructions) -> int:
    position = [0, 0]
    visited = {(0, 0)}
    for instruction in instructions:
        _move(position, instruction)
        visited.add((position[0], position[1]))
    return len(visited)


def get_houses_santa_and_robo_santa(instructions):
    santa_position = [0, 0]
    robo_santa_position = [0, 0]
    santa_turn = True
    visited = {(0, 0)}
    for instruction in instructions:
        p = santa_position if santa_turn else robo_santa_position
        _move(p, instruction)
        visited.add((p[0], p[1]))
        santa_turn = not santa_turn
    return len(visited)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    santa_houses = get_houses_santa(text.strip())
    print(santa_houses)

    santa_and_robo_houses = get_houses_santa_and_robo_santa(text.strip())
    print(santa_and_robo_houses)


if __name__ == "__main__":
    main()
