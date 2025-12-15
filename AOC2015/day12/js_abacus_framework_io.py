import argparse
import json
from pathlib import Path
import re


NUMBER_REGEX = r"-?\d+"


def sum_all_numbers(text: str) -> int:
    matches = re.findall(NUMBER_REGEX, text)
    return sum(int(m) for m in matches)


def sum_all_json(obj: dict | list | int | str) -> int:
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, str):
        return 0
    elif isinstance(obj, list):
        return sum(sum_all_json(o) for o in obj)
    else:
        if "red" in obj.values():
            return 0
        return sum(sum_all_json(k) + sum_all_json(v) for k, v in obj.items())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    number_sum = sum_all_numbers(text)
    print(number_sum)

    json_obj = json.loads(text)
    json_sum_no_red = sum_all_json(json_obj)
    print(json_sum_no_red)


if __name__ == "__main__":
    main()
