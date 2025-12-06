from trash_compactor import Problem, parse, parse_column


def test_solve_problems():
    assert Problem("+", [1, 2, 3]).solve() == 6
    assert Problem("*", [1, 2, 3]).solve() == 6


def test_parse():
    text = """123 328  51 64 
     45 64  387 23 
      6 98  215 314
    *   +   *   +  """
    problems = parse(text)
    expected = [
        Problem("*", [123, 45, 6]),
        Problem("+", [328, 64, 98]),
        Problem("*", [51, 387, 215]),
        Problem("+", [64, 23, 314]),
    ]
    assert problems == expected
