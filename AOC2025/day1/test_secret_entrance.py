import pytest
from secret_entrance import Instruction, Dial


instructions_to_parse = [
    ("L51", Instruction(direction="L", distance=51)),
    ("R1", Instruction(direction="R", distance=1)),
]


@pytest.mark.parametrize("instruction,expected", instructions_to_parse)
def test_parse_instruction(instruction, expected):
    assert Instruction.parse(instruction) == expected


instructions_to_turn = [
    (Instruction("L", 49), 1, 0),
    (Instruction("L", 99), 51, 1),
    (Instruction("L", 149), 1, 1),
    (Instruction("R", 49), 99, 0),
    (Instruction("R", 99), 49, 1),
    (Instruction("R", 149), 99, 1),
    (Instruction("R", 1000), 50, 10),
    (Instruction("R", 50), 0, 1),
    (Instruction("L", 50), 0, 1),
]


@pytest.mark.parametrize(
    "instruction,expected_position,expected_turns", instructions_to_turn
)
def test_turn(instruction, expected_position, expected_turns):
    dial = Dial()
    turns = dial.turn(instruction)
    assert dial.position == expected_position
    assert turns == expected_turns


def test_password():
    instructions = [
        Instruction("L", 68),
        Instruction("L", 30),
        Instruction("R", 48),
        Instruction("L", 5),
        Instruction("R", 60),
        Instruction("L", 55),
        Instruction("L", 1),
        Instruction("L", 99),
        Instruction("R", 14),
        Instruction("L", 82),
    ]
    dial = Dial()
    assert dial.password(instructions) == (3, 6)
