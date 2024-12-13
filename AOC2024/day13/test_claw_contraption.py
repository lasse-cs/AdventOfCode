from pathlib import Path
import pytest
from claw_contraption import Game, Button, score_games, parse_file


@pytest.mark.parametrize(
    argnames=["game", "score"],
    argvalues=[
        (Game(Button(94, 34, 3), Button(22, 67, 1), 8400, 5400), 280),
        (Game(Button(26, 66, 3), Button(67, 21, 1), 12748, 12176), None),
        (Game(Button(17, 86, 3), Button(84, 37, 1), 7870, 6450), 200),
        (Game(Button(69, 23, 3), Button(27, 71, 1), 18641, 10279), None),
    ],
)
def test_solve(game: Game, score: int | None):
    solved_game: int | None = game.solve()
    if score is None:
        assert solved_game is None
    else:
        assert solved_game == score


def test_parse_button_a() -> None:
    line: str = "Button A: X+94, Y+34"
    button: Button = Button.parse(line)
    expected_button: Button = Button(94, 34, 3)
    assert button == expected_button


def test_parse_button_b() -> None:
    line: str = "Button B: X+94, Y+34"
    button: Button = Button.parse(line)
    expected_button: Button = Button(94, 34, 1)
    assert button == expected_button


def test_parse_game() -> None:
    first_button_line: str = "Button A: X+94, Y+34"
    second_button_line: str = "Button B: X+22, Y+67"
    prize_line: str = "Prize: X=8400, Y=5400"
    game: Game = Game.parse_game(first_button_line, second_button_line, prize_line)
    expected_game: Game = Game(Button(94, 34, 3), Button(22, 67, 1), 8400, 5400)
    assert game == expected_game


def test_solve_games() -> None:
    game_file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    games: list[Game] = parse_file(game_file)
    total_score: int = score_games(games)
    assert total_score == 480


def test_adjusted_games() -> None:
    game_file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    games: list[Game] = parse_file(game_file, True)
    possible: list[bool] = [game.solve() is not None for game in games]
    assert possible == [False, True, False, True]
