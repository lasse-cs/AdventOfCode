import argparse
from pathlib import Path


def parse(text: str) -> dict[str, list[str]]:
    connections = {}
    for line in text.splitlines():
        line = line.strip()
        source, outputs = line.split(": ")
        connections[source] = outputs.split(" ")
    return connections


def count_paths(
    connections: dict[str, list[str]],
    start: str = "you",
    target: str = "out",
    not_through: str = "",
) -> int:
    return _count_paths(
        connections,
        [],
        {},
        start,
        target,
        not_through,
    )


def _count_paths(
    connections: dict[str, list[str]],
    path: list[str],
    cache: dict[str, int],
    current: str,
    target: str,
    not_through: str,
) -> int:
    if current == target:
        return 1
    if current == not_through:
        return 0
    if current not in cache:
        path.append(current)
        cache[current] = 0
        for conn in connections.get(current, []):
            cache[current] += _count_paths(
                connections, path, cache, conn, target, not_through
            )
        path.pop()
    return cache[current]


def count_svr_dac_fft_out_paths(connections: dict[str, list[str]]) -> int:
    svr_to_dac_paths = count_paths(connections, "svr", "dac", "fft")
    svr_to_fft_paths = count_paths(connections, "svr", "fft", "dac")
    dac_to_fft_paths = count_paths(connections, "dac", "fft")
    fft_to_dac_paths = count_paths(connections, "fft", "dac")
    dac_to_out_paths = count_paths(connections, "dac", "out", "fft")
    fft_to_out_paths = count_paths(connections, "fft", "out", "dac")

    count = svr_to_dac_paths * dac_to_fft_paths * fft_to_out_paths
    count += svr_to_fft_paths * fft_to_dac_paths * dac_to_out_paths
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    connections = parse(text)
    if "you" in connections:
        path_count = count_paths(connections)
        print(path_count)
    if "svr" in connections:
        svr_dac_fft_out_paths = count_svr_dac_fft_out_paths(connections)
        print(svr_dac_fft_out_paths)


if __name__ == "__main__":
    main()
