from like_a_gif_for_your_yard import Grid


def test_parse():
    text = """#.
              .#"""
    assert Grid.parse(text).grid == [[True, False], [False, True]]


def test_evolve_grid():
    text = """.#.#.#
              ...##.
              #....#
              ..#...
              #.#..#
              ####.."""
    grid = Grid.parse(text)
    for _ in range(4):
        print(grid.count_on())
        grid.evolve()
    assert grid.count_on() == 4
