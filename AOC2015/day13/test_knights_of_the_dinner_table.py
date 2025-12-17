from knights_of_the_dinner_table import parse_connections, calculate_maximum_happiness


def test_parse_connections():
    line = "Alice would gain 54 happiness units by sitting next to Bob."
    assert parse_connections(line) == {"Alice": {"Bob": 54}}


def test_maximum_happiness():
    text = """Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol."""
    connections = parse_connections(text)
    assert calculate_maximum_happiness(connections) == 330
