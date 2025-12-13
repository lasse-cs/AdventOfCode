import argparse
from hashlib import md5


def minimum_with_leading_zeroes(prefix: str, zeroes: int) -> int:
    x = 1
    while True:
        if check_attempt(prefix, x, zeroes):
            return x
        x += 1


def check_attempt(prefix: str, attempt_num: int, zeroes: int) -> bool:
    attempt = prefix + str(attempt_num)
    h = md5(attempt.encode()).hexdigest()
    for x in h[:zeroes]:
        if x != "0":
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    minimum_with_5 = minimum_with_leading_zeroes(args.input, 5)
    print(minimum_with_5)
    minimum_with_6 = minimum_with_leading_zeroes(args.input, 6)
    print(minimum_with_6)


if __name__ == "__main__":
    main()
