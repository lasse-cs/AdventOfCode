from cafeteria import Range, parse_input, get_fresh_ingredients, merge_ranges


def test_contained_id():
    r = Range(3, 5)
    assert 3 in r
    assert 4 in r
    assert 5 in r

    assert 2 not in r
    assert 6 not in r


def test_parse():
    input_text = """3-5
    10-14
    16-20
    12-18
    
    1
    5
    8
    11
    17
    32"""
    ranges, ingredients = parse_input(input_text)
    assert ranges == [Range(3, 5), Range(10, 14), Range(16, 20), Range(12, 18)]
    assert ingredients == [1, 5, 8, 11, 17, 32]


def test_get_fresh_ingredients():
    input_text = """3-5
    10-14
    16-20
    12-18
    
    1
    5
    8
    11
    17
    32"""
    ranges, ingredients = parse_input(input_text)
    assert get_fresh_ingredients(ranges, ingredients) == [5, 11, 17]


def test_merge_range():
    r1 = Range(12, 18)
    r2 = Range(16, 20)
    assert r1.can_merge(r2)
    assert r1.merge(r2) == Range(12, 20)


def test_merge_ranges():
    ranges = [Range(3, 5), Range(10, 14), Range(16, 20), Range(12, 18)]
    merged_ranges = merge_ranges(ranges)
    assert len(merged_ranges) == 2
    assert Range(3, 5) in merged_ranges
    assert Range(10, 20) in merged_ranges
