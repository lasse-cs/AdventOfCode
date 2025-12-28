from cube_conundrum import Draw, Game


def test_parse_draw():
    assert Draw.parse("3 blue, 4 red") == Draw(blue=3, red=4)


def test_parse_game():
    text = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    assert Game.parse(text) == Game(
        number=1,
        draws=[
            Draw(blue=3, red=4),
            Draw(red=1, green=2, blue=6),
            Draw(green=2),
        ],
    )


def test_game_possible():
    text = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    assert Game.parse(text).is_possible()
    text = "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    assert not Game.parse(text).is_possible()


def test_power():
    text = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    assert Game.parse(text).power() == 48
