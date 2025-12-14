from elves_look_elves_say import Block, evolve_list_of_blocks


def test_parse_into_blocks():
    number = "11"
    assert Block.parse_into_blocks(number) == [Block(1, 2)]

    number = "111221"
    assert Block.parse_into_blocks(number) == [Block(1, 3), Block(2, 2), Block(1, 1)]


def test_evolve_list_of_blocks():
    blocks = [Block(1, 1)]
    assert evolve_list_of_blocks(blocks) == [Block(1, 2)]
    blocks = [Block(1, 2)]
    assert evolve_list_of_blocks(blocks) == [Block(2, 1), Block(1, 1)]
    blocks = [Block(1, 1), Block(2, 1), Block(1, 2)]
    assert evolve_list_of_blocks(blocks) == [Block(1, 3), Block(2, 2), Block(1, 1)]
