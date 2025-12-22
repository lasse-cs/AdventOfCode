import argparse
from pathlib import Path


DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

WORD_DIGITS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def calibration_value(text: str) -> int:
    left, right = 0, len(text) - 1
    left_stop = False
    right_stop = False
    while not right_stop or not left_stop:
        if text[left] in DIGITS:
            left_stop = True
        else:
            left += 1
        if text[right] in DIGITS:
            right_stop = True
        else:
            right -= 1

    return int(text[left] + text[right])


def word_calibration_value(text: str) -> int:
    left_idx, right_idx = 0, len(text) - 1
    left_stop, right_stop = False, False
    left, right = "", ""
    while not right_stop or not left_stop:
        if text[left_idx] in DIGITS:
            left_stop = True
            left = text[left_idx]
        if text[right_idx] in DIGITS:
            right_stop = True
            right = text[right_idx]
        for digit in WORD_DIGITS:
            len_digit = len(digit)
            if text[left_idx : left_idx + len_digit] == digit:
                left = str(WORD_DIGITS.index(digit))
                left_stop = True
            if text[right_idx : right_idx + len_digit] == digit:
                right = str(WORD_DIGITS.index(digit))
                right_stop = True
        if not left_stop:
            left_idx += 1
        if not right_stop:
            right_idx -= 1
    return int(left + right)


def sum_calibrations(text: str) -> int:
    return sum(calibration_value(x) for x in text.splitlines())


def sum_word_calibration(text: str) -> int:
    return sum(word_calibration_value(x) for x in text.splitlines())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()

    calibration_sum = sum_calibrations(text)
    print(calibration_sum)

    word_calibration_sum = sum_word_calibration(text)
    print(word_calibration_sum)


if __name__ == "__main__":
    main()
