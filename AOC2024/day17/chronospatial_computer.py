from argparse import ArgumentParser
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from re import Match, Pattern, compile
from typing import TypeAlias


@dataclass
class Registers:
    a: int
    b: int
    c: int

    def get_combo_operand(self, operand: int) -> int:
        if operand in range(4):
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        raise ValueError("Unexpected Combo Operand")


# Register, Operand, Pointer -> Pointer, Output
Instruction: TypeAlias = Callable[[Registers, int, int], tuple[int, int | None]]


def adv(registers: Registers, operand: int, p: int) -> tuple[int, None]:
    numerator = registers.a
    denominator = 2 ** registers.get_combo_operand(operand)
    division = numerator // denominator
    registers.a = division
    return (p + 2, None)


def bxl(registers: Registers, operand: int, p: int) -> tuple[int, None]:
    registers.b = registers.b ^ operand
    return (p + 2, None)


def bst(registers: Registers, operand: int, p: int) -> tuple[int, None]:
    combo = registers.get_combo_operand(operand)
    registers.b = combo % 8
    return (p + 2, None)


def jnz(registers: Registers, operand: int, p: int) -> tuple[int, None]:
    if registers.a == 0:
        return (p + 2, None)
    return (operand, None)


def bxc(registers: Registers, _: int, p: int) -> tuple[int, None]:
    registers.b = registers.b ^ registers.c
    return (p + 2, None)


def out(registers: Registers, operand: int, p: int) -> tuple[int, int]:
    combo = registers.get_combo_operand(operand)
    return (p + 2, combo % 8)


def bdv(registers: Registers, operand: int, p: int) -> tuple[int, None]:
    numerator = registers.a
    denominator = 2 ** registers.get_combo_operand(operand)
    division = numerator // denominator
    registers.b = division
    return (p + 2, None)


def cdv(registers: Registers, operand: int, p: int) -> tuple[int, None]:
    numerator = registers.a
    denominator = 2 ** registers.get_combo_operand(operand)
    division = numerator // denominator
    registers.c = division
    return (p + 2, None)


INSTRUCTIONS: list[Instruction] = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def execute_program(registers: Registers, program: list[int]) -> list[int]:
    output: list[int] = []
    pointer: int = 0
    while pointer < len(program) - 1:
        opcode: int = program[pointer]
        operand: int = program[pointer + 1]
        instruction: Instruction = INSTRUCTIONS[opcode]
        pointer, out = instruction(registers, operand, pointer)
        if out is not None:
            output.append(out)
    return output


def find_first_repeat(registers: Registers, program: list[int]) -> int | None:
    output: list[int] = []
    digit_map: dict[int, list[str]] = defaultdict(list)
    # Looking through the input only 4 octal digits contribute to an output at a time
    for a in range(0o10000):
        a_registers = Registers(a, registers.b, registers.c)
        output = execute_program(a_registers, program)
        digit_map[output[0]].append(oct(a)[2:].rjust(4, "0"))

    possible: list[int] = []

    frontier: list[tuple[str, int]] = [("", 0)]
    seen: set[str] = set()
    while len(frontier) > 0:
        candidate, digit_count = frontier.pop()

        if digit_count == len(program):
            a = int(candidate, base=8)
            a_registers = Registers(a, registers.b, registers.c)
            output = execute_program(a_registers, program)
            assert output == program
            possible.append(a)
            continue

        next_digit = program[-(digit_count + 1)]
        for d in digit_map[next_digit]:
            if len(candidate) > 3:
                if candidate[-3:] != d[:3]:
                    continue
            next_candidate = candidate + d[-1]
            if next_candidate in seen:
                continue
            a_attempt = int(next_candidate, 8)
            regs = Registers(a_attempt, registers.b, registers.c)
            current_output = execute_program(regs, program)
            if current_output == program[-(digit_count + 1) :]:
                frontier.append((next_candidate, digit_count + 1))
                seen.add(next_candidate)

    return min(possible) if possible else 0


REGISTER_PATTERN: Pattern = compile(r"Register (A|B|C): (\d+)")
PROGRAM_PATTERN: Pattern = compile(r"Program: ((\d+,?)+)")


def parse(lines: list[str]) -> tuple[Registers, list[int]]:
    assert len(lines) >= 5
    registers: list[int] = []
    for i in range(3):
        m: Match[str] | None = REGISTER_PATTERN.match(lines[i])
        if m is None:
            raise ValueError("Unexpected register line")
        registers.append(int(m.group(2)))
    program_match: Match[str] | None = PROGRAM_PATTERN.match(lines[4])
    if program_match is None:
        raise ValueError("Unexpected Program line")
    program = [int(p) for p in program_match.group(1).split(",")]
    return Registers(*registers), program


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)
    with file.open("r") as f:
        lines: list[str] = f.readlines()
    registers, program = parse(lines)
    output: list[int] = execute_program(registers, program)
    print(f"The output of the program is {','.join([str(s) for s in output])}")

    with file.open("r") as f:
        lines = f.readlines()
    initial_registers, program = parse(lines)
    first_repeat: int | None = find_first_repeat(initial_registers, program)
    if first_repeat is None:
        raise ValueError("No solution found")
    print(f"The program first outputs a copy with register A = {first_repeat}")
