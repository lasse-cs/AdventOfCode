import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    @staticmethod
    def parse(text: str) -> "Draw":
        parts = text.split(", ")
        arguments = {}
        for part in parts:
            num, color = part.split(" ")
            arguments[color] = int(num)
        return Draw(**arguments)

    def is_possible(self) -> bool:
        return self.red <= 12 and self.green <= 13 and self.blue <= 14


@dataclass(frozen=True)
class Game:
    number: int
    draws: list[Draw]

    @staticmethod
    def parse(text: str) -> "Game":
        game, draw_string = text.strip().split(": ")
        number = int(game[5:])
        draws = [Draw.parse(d) for d in draw_string.split("; ")]
        return Game(number, draws)

    def is_possible(self) -> bool:
        return all(draw.is_possible() for draw in self.draws)

    def power(self) -> int:
        min_green = max(draw.green for draw in self.draws)
        min_red = max(draw.red for draw in self.draws)
        min_blue = max(draw.blue for draw in self.draws)
        return min_green * min_red * min_blue


def sum_possible_game_numbers(games: list[Game]) -> int:
    return sum(game.number for game in games if game.is_possible())


def sum_game_powers(games: list[Game]) -> int:
    return sum(game.power() for game in games)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    games = [Game.parse(t) for t in text.splitlines()]
    possible_game_sum = sum_possible_game_numbers(games)
    print(possible_game_sum)

    total_power = sum_game_powers(games)
    print(total_power)


if __name__ == "__main__":
    main()
