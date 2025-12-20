from no_such_thing_as_too_much import Box, combinations


def test_combinations():
    boxes = [
        Box(1, 20),
        Box(2, 15),
        Box(3, 10),
        Box(4, 5),
        Box(5, 5),
    ]
    assert combinations(boxes, 25) == {2: 3, 3: 1}
