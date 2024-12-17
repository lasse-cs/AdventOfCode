from pathlib import Path
from chronospatial_computer import (
    Registers,
    adv,
    bdv,
    bxc,
    bxl,
    bst,
    cdv,
    execute_program,
    find_first_repeat,
    jnz,
    out,
    parse,
)


def test_adv_small_operand() -> None:
    registers: Registers = Registers(10, 5, 0)
    adv(registers, 2, 0)
    assert registers == Registers(2, 5, 0)


def test_adv_larger_operand() -> None:
    registers: Registers = Registers(10, 2, 0)
    p, _ = adv(registers, 5, 0)
    assert p == 2
    assert registers == Registers(2, 2, 0)


def test_bxl() -> None:
    registers: Registers = Registers(0, 0b1010, 0)
    p, _ = bxl(registers, 0b111, 0)
    assert p == 2
    assert registers == Registers(0, 0b1101, 0)


def test_bst() -> None:
    registers: Registers = Registers(0, 0, 12)
    p, _ = bst(registers, 6, 0)
    assert p == 2
    assert registers == Registers(0, 4, 12)


def test_jnz_no_jump() -> None:
    registers: Registers = Registers(0, 0, 0)
    p, _ = jnz(registers, 6, 8)
    assert p == 10


def test_jnz_jump() -> None:
    registers: Registers = Registers(1, 0, 0)
    p, _ = jnz(registers, 6, 10)
    assert p == 6


def test_bxc() -> None:
    registers: Registers = Registers(0, 0b111, 0b1101)
    p, _ = bxc(registers, 2, 0)
    assert p == 2
    assert registers == Registers(0, 0b1010, 0b1101)


def test_out() -> None:
    registers: Registers = Registers(0, 0, 10)
    p, output = out(registers, 6, 2)
    assert p == 4
    assert output == 2


def test_bdv() -> None:
    registers: Registers = Registers(10, 5, 0)
    p, _ = bdv(registers, 2, 0)
    assert p == 2
    assert registers == Registers(10, 2, 0)


def test_cdv() -> None:
    registers: Registers = Registers(10, 5, 0)
    p, _ = cdv(registers, 2, 0)
    assert p == 2
    assert registers == Registers(10, 5, 2)


def test_bst_program() -> None:
    registers: Registers = Registers(0, 0, 9)
    program: list[int] = [2, 6]
    execute_program(registers, program)
    assert registers == Registers(0, 1, 9)


def test_program_two() -> None:
    registers: Registers = Registers(10, 0, 0)
    program: list[int] = [5, 0, 5, 1, 5, 4]
    output: list[int] = execute_program(registers, program)
    assert output == [0, 1, 2]


def test_program_three() -> None:
    registers: Registers = Registers(2024, 0, 0)
    program: list[int] = [0, 1, 5, 4, 3, 0]
    output: list[int] = execute_program(registers, program)
    assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert registers.a == 0


def test_program_four() -> None:
    registers: Registers = Registers(0, 29, 0)
    program: list[int] = [1, 7]
    execute_program(registers, program)
    assert registers.b == 26


def test_program_five() -> None:
    registers: Registers = Registers(0, 2024, 43690)
    program: list[int] = [4, 0]
    execute_program(registers, program)
    assert registers.b == 44354


def test_parse() -> None:
    file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    with file.open("r") as f:
        lines = f.readlines()
    registers, program = parse(lines)
    assert registers == Registers(729, 0, 0)
    assert program == [0, 1, 5, 4, 3, 0]


def test_execute_program() -> None:
    file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    with file.open("r") as f:
        lines = f.readlines()
    registers, program = parse(lines)
    output = execute_program(registers, program)
    assert output == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]


def test_copy_self() -> None:
    file: Path = Path(__file__).resolve().parent / "files" / "test_repeat_input.txt"
    with file.open("r") as f:
        lines = f.readlines()
    initial_registers, program = parse(lines)
    a: int = find_first_repeat(initial_registers, program)
    assert a == 117440
