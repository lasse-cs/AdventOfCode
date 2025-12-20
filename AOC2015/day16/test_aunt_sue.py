from aunt_sue import Aunt


def test_parse():
    text = "Sue 2: akitas: 10, perfumes: 10, children: 5"
    assert Aunt.parse(text) == Aunt(2, akitas=10, perfumes=10, children=5)
