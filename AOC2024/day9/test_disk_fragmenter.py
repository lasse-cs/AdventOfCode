from pathlib import Path
import pytest

from disk_fragmenter import (
    parse,
    parse_file,
    Disk,
    GapLengths,
    fragment,
    calculate_checksum,
    read_gaps,
    defragment,
)


@pytest.fixture
def simple_disk() -> Disk:
    return parse("12345")


@pytest.fixture
def test_disk() -> Disk:
    file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    return parse_file(file)


def test_parse(simple_disk: Disk):
    expected = [0, None, None, 1, 1, 1, None, None, None, None, 2, 2, 2, 2, 2]
    assert simple_disk == expected


def test_fragment(simple_disk: Disk):
    fragment(simple_disk)
    expected: Disk = [0, 2, 2, 1, 1, 1, 2, 2, 2, None, None, None, None, None, None]
    assert simple_disk == expected


def test_simple_calculate_checksum(simple_disk: Disk):
    fragment(simple_disk)
    checksum: int = calculate_checksum(simple_disk)
    assert checksum == 60


def test_calculate_checksum(test_disk: Disk):
    fragment(test_disk)
    checksum: int = calculate_checksum(test_disk)
    assert checksum == 1928


def test_read_gaps(simple_disk: Disk):
    gaps: GapLengths = read_gaps(simple_disk)
    expected: GapLengths = [
        [],
        [],
        [1],
        [],
        [6],
        [],
        [],
        [],
        [],
        [],
    ]
    assert gaps == expected


def test_defragment(test_disk: Disk):
    defragment(test_disk)
    checksum: int = calculate_checksum(test_disk)
    assert checksum == 2858
