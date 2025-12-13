from probably_a_fire_hazard import parse_instruction, TurnOnInstruction


def test_parse():
    text = "turn on 0,0 through 999,999"
    parsed = parse_instruction(text)
    assert isinstance(parsed, TurnOnInstruction)
    assert parsed.start == (0, 0)
    assert parsed.end == (999, 999)
