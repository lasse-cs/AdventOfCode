from pathlib import Path
import pytest
from pytest import FixtureRequest
from ram_run import Memory, MemoryCell, parse, MemoryLocation, get_first_blocker


@pytest.fixture
def test_instructions(request: FixtureRequest) -> list[MemoryLocation]:
    file_name: str = request.param
    file: Path = Path(__file__).resolve().parent / "files" / file_name
    with file.open("r") as f:
        lines: list[str] = f.readlines()
    return parse(lines)


def test_parse() -> None:
    input: list[str] = ["5,4", "4,2", "4,5"]
    parsed: list[MemoryLocation] = parse(input)
    expected: list[MemoryLocation] = [
        MemoryLocation(4, 5),
        MemoryLocation(2, 4),
        MemoryLocation(5, 4),
    ]
    assert expected == parsed


@pytest.mark.parametrize("test_instructions", ("test_input.txt",), indirect=True)
def test_corrupt_twelve_memory(test_instructions: list[MemoryLocation]):
    memory: Memory = Memory(7, 7)
    for i in range(12):
        memory.corrupt_cell(test_instructions[i])
    expected_cells: list[list[MemoryCell]] = [
        [
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
        ],
        [
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
        ],
        [
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
        ],
        [
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
        ],
        [
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
        ],
        [
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
        ],
        [
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.CORRUPTED,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
            MemoryCell.SAFE,
        ],
    ]
    assert memory.cells == expected_cells


@pytest.mark.parametrize("test_instructions", ("test_input.txt",), indirect=True)
def test_steps_after_twelve(test_instructions: list[MemoryLocation]):
    memory: Memory = Memory(7, 7)
    for i in range(12):
        memory.corrupt_cell(test_instructions[i])
    path_length: int = memory.get_steps_required()
    assert path_length == 22


@pytest.mark.parametrize("test_instructions", ("test_input.txt",), indirect=True)
def test_first_blocker(test_instructions: list[MemoryLocation]):
    memory: Memory = Memory(7, 7)
    blocker: MemoryLocation | None = get_first_blocker(memory, test_instructions)
    assert blocker == MemoryLocation(1, 6)
