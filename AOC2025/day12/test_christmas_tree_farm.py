from christmas_tree_farm import Shape


def test_variants():
    shape = [[True, True, True], [True, True, False], [True, True, False]]
    s = Shape(shape, 0)
    assert not len(s.variants)
