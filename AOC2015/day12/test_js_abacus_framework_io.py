from js_abacus_framework_io import sum_all_numbers, sum_all_json


def test_sum_all_numbers():
    assert sum_all_numbers("[1, 2, 3]") == 6
    assert sum_all_numbers('{"a":2,"b":4}') == 6
    assert sum_all_numbers("[[[3]]]") == 3
    assert sum_all_numbers('{"a":{"b":4},"c":-1}') == 3
    assert sum_all_numbers('{"a":[-1,1]}') == 0
    assert sum_all_numbers('[-1,{"a":1}]') == 0
    assert sum_all_numbers("[]") == 0
    assert sum_all_numbers("{}") == 0


def test_sum_all_json():
    assert sum_all_json([1, 2, 3]) == 6
    assert sum_all_json([1, {"c": "red", "b": 2}, 3]) == 4
    assert sum_all_json({"d": "red", "e": [1, 2, 3, 4], "f": 5}) == 0
    assert sum_all_json([1, "red", 5]) == 6
