from pathlib import Path
from ceres_search import WordSearch, Cell


def test_parse():
    test_file = Path(".") / "files" / "test_smaller_input.txt"
    word_search = WordSearch.parse(test_file)
    assert word_search.cells == [
        [Cell.X, Cell.M, Cell.A, Cell.S],
        [Cell.X, Cell.M, Cell.A, Cell.S],
    ]


def test_count_words():
    test_file = Path(".") / "files" / "test_input.txt"
    word_search = WordSearch.parse(test_file)
    assert word_search.count_words() == 18


def test_count_crosses():
    test_file = Path(".") / "files" / "test_input.txt"
    word_search = WordSearch.parse(test_file)
    assert word_search.count_crosses() == 9
