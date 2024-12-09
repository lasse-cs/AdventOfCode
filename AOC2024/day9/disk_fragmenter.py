from argparse import ArgumentParser
from pathlib import Path
from heapq import heappop, heappush

Disk = list[int | None]

# Basically a dictionary of gap length to a heap of start indices
# Max gap length will care about is 9, so use a list over dict
GapLengths = list[list[int]]


def fragment(disk: Disk):
    gap_pointer: int = 0
    file_pointer: int = len(disk) - 1
    while gap_pointer < file_pointer:
        if disk[gap_pointer] is not None:
            gap_pointer += 1
        elif disk[file_pointer] is None:
            file_pointer -= 1
        else:
            disk[gap_pointer], disk[file_pointer] = (
                disk[file_pointer],
                disk[gap_pointer],
            )


def defragment(disk: Disk):
    gap_lengths: GapLengths = read_gaps(disk)

    seen_files: set[int] = set()

    file_start: int = len(disk) - 1
    file_length: int = 0
    while file_start > 0:
        id: int | None = disk[file_start]
        if id is None or id in seen_files:
            file_start -= 1
            continue

        file_length += 1
        if file_start == 0 or disk[file_start - 1] != id:
            _move_file(disk, gap_lengths, file_length, file_start)
            file_length = 0
            seen_files.add(id)
        file_start -= 1


def _move_file(
    disk: Disk, gap_lengths: GapLengths, file_length: int, file_start: int
) -> None:
    gap_length = _find_gap(gap_lengths, file_length, file_start)
    if gap_length == 0:
        return
    gap_start = heappop(gap_lengths[gap_length])
    _fill_gap(disk, gap_start, file_length, file_start)
    _update_gaps(gap_lengths, gap_length, gap_start, file_length)


def _find_gap(gap_lengths: GapLengths, file_length: int, file_start: int) -> int:
    earlist_gap: int = file_start
    earliest_gap_length: int = 0
    for gap_length in range(file_length, 10):
        if len(gap_lengths[gap_length]) == 0:
            continue
        possible = gap_lengths[gap_length][0]
        if possible < earlist_gap:
            earliest_gap_length = gap_length
            earlist_gap = possible

    return earliest_gap_length


def _fill_gap(
    disk: Disk,
    gap_start: int,
    file_length: int,
    file_start: int,
) -> None:
    for index in range(file_length):
        disk[gap_start + index], disk[file_start + index] = (
            disk[file_start + index],
            disk[gap_start + index],
        )


def _update_gaps(
    gap_lengths: GapLengths, gap_length: int, gap_start: int, file_length: int
) -> None:
    if gap_length <= file_length:
        return

    new_gap_start: int = gap_start + file_length
    new_gap_length: int = gap_length - file_length
    heappush(gap_lengths[new_gap_length], new_gap_start)


def read_gaps(disk: Disk) -> GapLengths:
    gap_lengths: GapLengths = [[] for _ in range(10)]
    gap_length: int = 0
    gap_start: int = 0
    for index, id in enumerate(disk):
        if id is not None:
            continue

        if gap_length == 0:
            gap_start = index
        gap_length += 1

        if index == len(disk) or disk[index + 1] is not None:
            heappush(gap_lengths[gap_length], gap_start)
            gap_length = 0

    return gap_lengths


def calculate_checksum(disk: Disk) -> int:
    return sum(index * digit for index, digit in enumerate(disk) if digit is not None)


def parse_file(input_file: Path) -> Disk:
    input: str = input_file.read_text().strip()
    return parse(input)


def parse(input: str) -> Disk:
    disk: Disk = []
    is_file: bool = True
    id_counter: int = 0
    for digit in input:
        if is_file:
            disk.extend(int(digit) * [id_counter])
            id_counter += 1
        else:
            disk.extend(int(digit) * [None])
        is_file = not is_file
    return disk


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    disk: Disk = parse_file(file)
    fragment(disk)
    checksum: int = calculate_checksum(disk)

    print(f"The checksum of the fragmented disk is {checksum}")

    disk = parse_file(file)
    defragment(disk)
    checksum = calculate_checksum(disk)
    print(f"The checksum of the defragmented disk is {checksum}")
