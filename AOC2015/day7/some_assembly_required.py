import argparse
from dataclasses import dataclass
from pathlib import Path
import re


SETTER_REGEX = r"(\w+) -> (\w+)"
NOT_REGEX = r"NOT (\w+) -> (\w+)"
BINARY_REGEX = r"(\w+) (\w+) (\w+) -> (\w+)"


@dataclass
class Instruction:
    target: str

    def apply(self, registry: dict[str, int]):
        pass

    def can_resolve(self, registry: dict[str, int]) -> bool:
        return False

    def _get_value(self, x: str | int, registry: dict[str, int]) -> int:
        return registry[x] if isinstance(x, str) else x

    def _is_value_resolved(self, x: str | int, registry: dict[str, int]) -> bool:
        return x in registry if isinstance(x, str) else True


@dataclass
class UnaryInstruction(Instruction):
    value: str | int

    def can_resolve(self, registry: dict[str, int]) -> bool:
        return self._is_value_resolved(self.value, registry)


@dataclass
class BinaryInstruction(Instruction):
    left: str | int
    right: str | int

    def can_resolve(self, registry: dict[str, int]) -> bool:
        return self._is_value_resolved(self.left, registry) and self._is_value_resolved(
            self.right, registry
        )


@dataclass
class SetInstruction(UnaryInstruction):
    def apply(self, registry: dict[str, int]):
        registry[self.target] = self._get_value(self.value, registry)


@dataclass
class NotInstruction(UnaryInstruction):
    def apply(self, registry: dict[str, int]):
        registry[self.target] = self._get_value(self.value, registry) ^ (2**16 - 1)


@dataclass
class AndInstruction(BinaryInstruction):
    def apply(self, registry: dict[str, int]):
        left_value = self._get_value(self.left, registry)
        right_value = self._get_value(self.right, registry)
        registry[self.target] = (left_value & right_value) & (2**16 - 1)


@dataclass
class OrInstruction(BinaryInstruction):
    def apply(self, registry: dict[str, int]):
        left_value = self._get_value(self.left, registry)
        right_value = self._get_value(self.right, registry)
        registry[self.target] = (left_value | right_value) & (2**16 - 1)


@dataclass
class LShiftInstruction(BinaryInstruction):
    def apply(self, registry: dict[str, int]):
        left_value = self._get_value(self.left, registry)
        right_value = self._get_value(self.right, registry)
        registry[self.target] = (left_value << right_value) & (2**16 - 1)


@dataclass
class RShiftInstruction(BinaryInstruction):
    def apply(self, registry: dict[str, int]):
        left_value = self._get_value(self.left, registry)
        right_value = self._get_value(self.right, registry)
        registry[self.target] = (left_value >> right_value) & (2**16 - 1)


def _int_or_value(x: str) -> int | str:
    try:
        return int(x)
    except ValueError:
        return x


def read_instructions(
    text: str,
) -> list[Instruction]:
    instructions = []
    for line in text.splitlines():
        line = line.strip()
        instruction: Instruction | None = None
        if setter_match := re.match(SETTER_REGEX, line):
            value = _int_or_value(setter_match.group(1))
            target = setter_match.group(2)
            instruction = SetInstruction(value=value, target=target)
        elif not_match := re.match(NOT_REGEX, line):
            value = _int_or_value(not_match.group(1))
            target = not_match.group(2)
            instruction = NotInstruction(value=value, target=target)
        elif binary_match := re.match(BINARY_REGEX, line):
            left = _int_or_value(binary_match.group(1))
            operator = binary_match.group(2)
            right = _int_or_value(binary_match.group(3))
            target = binary_match.group(4)
            if operator == "AND":
                instruction = AndInstruction(target=target, left=left, right=right)
            elif operator == "OR":
                instruction = OrInstruction(target=target, left=left, right=right)
            elif operator == "LSHIFT":
                instruction = LShiftInstruction(target=target, left=left, right=right)
            else:
                instruction = RShiftInstruction(target=target, left=left, right=right)
        if instruction:
            instructions.append(instruction)
    return instructions


def resolve(instructions: list[Instruction]) -> dict[str, int]:
    registry: dict[str, int] = {}
    resolved: set[int] = set()
    done = False
    while not done:
        done = True
        for i, instruction in enumerate(instructions):
            if i in resolved:
                continue
            if not instruction.can_resolve(registry):
                continue
            instruction.apply(registry)
            resolved.add(i)
            done = False
    return registry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    instructions = read_instructions(text)
    registry = resolve(instructions)
    print(registry["a"])

    new_instruction = SetInstruction(target="b", value=registry["a"])
    for i, instruction in enumerate(instructions):
        if instruction.target == "b":
            break
    instructions.pop(i)
    instructions.append(new_instruction)
    new_registry = resolve(instructions)
    print(new_registry["a"])


if __name__ == "__main__":
    main()
