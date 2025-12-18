from reindeer_olympics import (
    Reindeer,
    get_race_winning_distance,
    get_race_winning_points,
)


def test_parse():
    line = "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."
    assert Reindeer.parse(line) == Reindeer("Dancer", 16, 11, 162)


def test_distance():
    deer = Reindeer("Comet", 14, 10, 127)
    assert deer.distance(10) == 140
    assert deer.distance(1000) == 1120
    deer = Reindeer("Dancer", 16, 11, 162)
    assert deer.distance(1000) == 1056


def test_get_race_winning_distance():
    reindeer = [Reindeer("Comet", 14, 10, 127), Reindeer("Dancer", 16, 11, 162)]
    assert get_race_winning_distance(reindeer, 1000) == 1120


def test_get_race_winning_points():
    reindeer = [Reindeer("Comet", 14, 10, 127), Reindeer("Dancer", 16, 11, 162)]
    assert get_race_winning_points(reindeer, 1000) == 689
