import argparse
from pathlib import Path


def string_data_length(text: str) -> int:
    count = 0
    position = 1
    while position < len(text) - 1:
        count += 1
        if text[position] == "\\":
            if text[position + 1] == "x":
                position += 4
            else:
                position += 2
        else:
            position += 1
    return count


def encoded_string_length(text: str) -> int:
    result = 2
    for c in text:
        if c == '"':
            result += 2
        elif c == "\\":
            result += 2
        else:
            result += 1
    return result


def total_difference_code_data(text: str) -> int:
    total = 0
    for line in text.splitlines():
        line = line.strip()
        total += len(line) - string_data_length(line)
    return total


def total_difference_encoded_code(text: str) -> int:
    total = 0
    for line in text.splitlines():
        line = line.strip()
        total += encoded_string_length(line) - len(line)
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    total_difference = total_difference_code_data(text)
    print(total_difference)

    total_difference_encoded = total_difference_encoded_code(text)
    print(total_difference_encoded)


if __name__ == "__main__":
    main()
