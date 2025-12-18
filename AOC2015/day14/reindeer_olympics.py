import argparse
from dataclasses import dataclass
import re
from pathlib import Path


REINDEER_REGEX = (
    r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
)


@dataclass(frozen=True)
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int

    def distance(self, time: int) -> int:
        total = 0
        period = self.duration + self.rest
        num_periods = time // period
        total += num_periods * self.speed * self.duration
        total += self.speed * min(time % period, self.duration)
        return total

    @staticmethod
    def parse(text: str) -> "Reindeer":
        reindeer_match = re.match(REINDEER_REGEX, text)
        if not reindeer_match:
            raise ValueError
        name = reindeer_match.group(1)
        speed = int(reindeer_match.group(2))
        duration = int(reindeer_match.group(3))
        rest = int(reindeer_match.group(4))
        return Reindeer(name, speed, duration, rest)


def get_race_winning_distance(reindeer: list[Reindeer], time: int) -> int:
    distance = 0
    for r in reindeer:
        d = r.distance(time)
        distance = max(d, distance)
    return distance


def get_race_winners(reindeer: list[Reindeer], time: int) -> list[Reindeer]:
    winners = []
    distance = 0
    for r in reindeer:
        d = r.distance(time)
        if d > distance:
            distance = d
            winners = [r]
        elif d == distance:
            winners.append(r)
    return winners


def get_race_winning_points(reindeer: list[Reindeer], time: int) -> int:
    points = {}
    for t in range(1, time + 1):
        winners = get_race_winners(reindeer, t)
        for winner in winners:
            if winner not in points:
                points[winner] = 0
            points[winner] += 1
    return max(points.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    reindeers = [Reindeer.parse(line) for line in text.splitlines()]
    race_winning_distance = get_race_winning_distance(reindeers, 2503)
    print(race_winning_distance)

    race_winning_points = get_race_winning_points(reindeers, 2503)
    print(race_winning_points)


if __name__ == "__main__":
    main()
