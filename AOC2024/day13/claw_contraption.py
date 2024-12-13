from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple
from re import Pattern, compile, Match

BUTTON_PATTERN: Pattern = compile(r"Button (A|B): X\+(\d+), Y\+(\d+)")
PRIZE_PATTERN: Pattern = compile(r"Prize: X=(\d+), Y=(\d+)")


class Button(NamedTuple):
    x: int
    y: int
    cost: int

    @staticmethod
    def parse(line: str) -> "Button":
        match: Match | None = BUTTON_PATTERN.match(line)
        if match is None:
            raise Exception
        type: str = match.group(1)
        x: int = int(match.group(2))
        y: int = int(match.group(3))

        cost: int = 3 if type == "A" else 1
        return Button(x, y, cost)


class Game(NamedTuple):
    button_a: Button
    button_b: Button
    x: int
    y: int

    def determinant(self) -> int:
        return self.button_a.x * self.button_b.y - self.button_a.y * self.button_b.x

    def solve(self) -> int | None:
        det: int = self.determinant()
        if det != 0:
            a_count = (self.button_b.y * self.x - self.button_b.x * self.y) // det
            b_count = (-self.button_a.y * self.x + self.button_a.x * self.y) // det

            if not self.check(a_count, b_count):
                return None
            return self.score(a_count, b_count)
        else:
            # This feels stupid... I never encounter a value with zero determinant...
            raise Exception

    def score(self, a_count: int, b_count: int) -> int:
        return a_count * self.button_a.cost + b_count * self.button_b.cost

    def check(self, a_count: int, b_count: int) -> bool:
        if a_count * self.button_a.x + b_count * self.button_b.x != self.x:
            return False
        return a_count * self.button_a.y + b_count * self.button_b.y == self.y

    @staticmethod
    def parse_game(
        first_button_line: str,
        second_button_line: str,
        prize_line: str,
        adjust: bool = False,
    ):
        button_a: Button = Button.parse(first_button_line)
        button_b: Button = Button.parse(second_button_line)
        x, y = Game._parse_prize(prize_line)
        if adjust:
            x += 10_000_000_000_000
            y += 10_000_000_000_000
        return Game(button_a, button_b, x, y)

    @staticmethod
    def _parse_prize(line: str) -> tuple[int, int]:
        match: Match | None = PRIZE_PATTERN.match(line)
        if match is None:
            raise Exception
        x: int = int(match.group(1))
        y: int = int(match.group(2))
        return x, y


def score_games(games: list[Game]) -> int:
    total: int = 0
    for game in games:
        score: int | None = game.solve()
        if score is None:
            continue
        total += score
    return total


def parse_file(file: Path, adjust: bool = False) -> list[Game]:
    games: list[Game] = []
    with file.open("r") as f:
        lines: list[str] = f.readlines()
        for i in range(0, len(lines), 4):
            first_button_line = lines[i]
            second_button_line = lines[i + 1]
            prize_line = lines[i + 2]
            games.append(
                Game.parse_game(
                    first_button_line, second_button_line, prize_line, adjust
                )
            )
    return games


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    games: list[Game] = parse_file(file)
    score: int = score_games(games)
    print(f"The total score for the games is {score}")

    adjusted_games: list[Game] = parse_file(file, True)
    score = score_games(adjusted_games)
    print(f"The total score for the adjusted games is {score}")
