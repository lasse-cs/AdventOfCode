import argparse
from pathlib import Path

VOWELS = "aeiou"
DISALLOWED = [("a", "b"), ("c", "d"), ("p", "q"), ("x", "y")]


def is_nice(text: str) -> bool:
    vowel_count = 1 if text[-1] in VOWELS else 0
    has_double = False
    for i in range(len(text) - 1):
        letter, next_letter = text[i], text[i + 1]
        vowel_count += letter in VOWELS
        has_double = has_double or letter == next_letter
        if (letter, next_letter) in DISALLOWED:
            return False
    return vowel_count >= 3 and has_double


def is_actually_nice(text: str) -> bool:
    has_gapped_repeat = False
    pairs_to_index = {(text[0], text[1]): 1}
    has_double_pair = False
    for i in range(2, len(text)):
        has_gapped_repeat = has_gapped_repeat or text[i] == text[i - 2]
        pair = (text[i - 1], text[i])
        if pair in pairs_to_index:
            has_double_pair = has_double_pair or pairs_to_index[pair] + 1 != i
        else:
            pairs_to_index[pair] = i
    return has_gapped_repeat and has_double_pair


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    total_nice = sum(is_nice(x) for x in text.splitlines())
    print(total_nice)

    total_actually_nice = sum(is_actually_nice(x) for x in text.splitlines())
    print(total_actually_nice)


if __name__ == "__main__":
    main()
