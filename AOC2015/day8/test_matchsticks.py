from matchsticks import (
    string_data_length,
    total_difference_code_data,
    total_difference_encoded_code,
)


def test_string_data_length():
    assert string_data_length('""') == 0
    assert string_data_length('"abc"') == 3
    assert string_data_length('"aaa\\"aaa"') == 7
    assert string_data_length('"\\x27"') == 1


def test_total_difference_code_data():
    text = '''""
    "abc"
    "aaa\\"aaa"
    "\\x27"'''
    assert total_difference_code_data(text) == 12


def test_total_difference_encoded_code():
    text = '''""
    "abc"
    "aaa\\"aaa"
    "\\x27"'''
    assert total_difference_encoded_code(text) == 19
