from argparse import ArgumentParser
from pathlib import Path
from heapq import heappop, heappush

Disk = list[int | None]


def fragment(disk: Disk):
    left: int = 0
    right: int = len(disk) - 1
    while left <= right:
        if disk[left] is not None:
            left += 1
        elif disk[right] is None:
            right -= 1
        else:
            disk[left], disk[right] = disk[right], disk[left]


def defragment(disk: Disk):
    gap_lengths: list[list[int]] = read_gaps(disk)

    right: int = len(disk) - 1
    file_length: int = 0

    seen_files: set[int] = set()

    while right > 0:
        id = disk[right]
        if id is None or id in seen_files:
            right -= 1
            continue

        file_length += 1
        if right == 0 or disk[right - 1] != id:
            _fill_gap(disk, gap_lengths, file_length, right)
            file_length = 0
            seen_files.add(id)
        right -= 1


def _fill_gap(
    disk: Disk, gap_lengths: list[list[int]], file_length: int, file_start: int
):
    gap_length = _find_gap(gap_lengths, file_length, file_start)

    if gap_length == 0:
        return

    gap_start = heappop(gap_lengths[gap_length])

    for index in range(file_length):
        disk[gap_start + index], disk[file_start + index] = (
            disk[file_start + index],
            disk[gap_start + index],
        )

    if gap_length > file_length:
        new_gap_start = gap_start + file_length
        new_gap_length = gap_length - file_length
        heappush(gap_lengths[new_gap_length], new_gap_start)


def _find_gap(gap_lengths: list[list[int]], file_length: int, file_start: int) -> int:
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


def read_gaps(disk: Disk) -> list[list[int]]:
    gap_lengths: list[list[int]] = [[] for _ in range(10)]
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


def calculate_checksum(disk: Disk):
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
