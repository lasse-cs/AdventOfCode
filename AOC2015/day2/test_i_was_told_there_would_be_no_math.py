from i_was_told_there_would_be_no_math import Present


def test_parse():
    text = "2x3x4"
    assert Present.parse(text) == Present(2, 3, 4)


def test_wrapping_paper_area():
    assert Present(2, 3, 4).wrapping_paper_area() == 58
    assert Present(1, 1, 10).wrapping_paper_area() == 43


def test_ribbon_length():
    assert Present(2, 3, 4).ribbon_length() == 34
    assert Present(1, 1, 10).ribbon_length() == 14
