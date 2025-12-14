import argparse
from dataclasses import dataclass
from pathlib import Path
import re


ROUTE_REGEX = r"(\w+) to (\w+) = (\d+)"


@dataclass(frozen=True)
class Route:
    first: str
    second: str
    distance: int

    @staticmethod
    def parse(text: str) -> "Route":
        route_match = re.match(ROUTE_REGEX, text.strip())
        if not route_match:
            raise ValueError
        first = route_match.group(1)
        second = route_match.group(2)
        distance = int(route_match.group(3))
        return Route(first, second, distance)


def find_extreme_routes(routes: list[Route]) -> tuple[int, int]:
    routes_by_destination: dict[str, list[Route]] = {}
    for route in routes:
        if route.first not in routes_by_destination:
            routes_by_destination[route.first] = []
        if route.second not in routes_by_destination:
            routes_by_destination[route.second] = []
        routes_by_destination[route.first].append(route)
        routes_by_destination[route.second].append(route)

    mini: list[int | None] = [None]
    maxi: list[int | None] = [None]
    for start in routes_by_destination:
        _find_extremum(start, routes_by_destination, {start}, 0, mini)
        _find_extremum(start, routes_by_destination, {start}, 0, maxi, False)
    if not mini[0] or not maxi[0]:
        raise ValueError
    return mini[0], maxi[0]


def _find_extremum(
    start: str,
    routes_by_destination: dict[str, list[Route]],
    path: set[str],
    distance: int,
    extremum: list[int | None],
    find_minimum: bool = True,
):
    if extremum[0]:
        if find_minimum and distance > extremum[0]:
            return
    if len(path) == len(routes_by_destination):
        if not extremum[0]:
            extremum[0] = distance
        elif find_minimum:
            extremum[0] = min(extremum[0], distance)
        else:
            extremum[0] = max(extremum[0], distance)
        return
    for route in routes_by_destination[start]:
        if route.first in path and route.second in path:
            continue
        if route.first == start:
            next_stop = route.second
        else:
            next_stop = route.first
        next_distance = distance + route.distance
        path.add(next_stop)
        _find_extremum(
            next_stop,
            routes_by_destination,
            path,
            next_distance,
            extremum,
            find_minimum,
        )
        path.remove(next_stop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    routes = [Route.parse(line) for line in text.splitlines()]
    minimum, maximum = find_extreme_routes(routes)
    print(minimum)
    print(maximum)


if __name__ == "__main__":
    main()
