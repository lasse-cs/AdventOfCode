import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Present:
    length: int
    width: int
    height: int

    @staticmethod
    def parse(text: str) -> "Present":
        return Present(*(int(x) for x in text.split("x")))

    def _surface_areas(self) -> tuple[int, int, int]:
        return (
            self.length * self.width,
            self.width * self.height,
            self.height * self.length,
        )

    def wrapping_paper_area(self) -> int:
        surface_areas = self._surface_areas()
        return 2 * sum(surface_areas) + min(surface_areas)

    def _perimeters(self) -> tuple[int, int, int]:
        return (
            2 * (self.length + self.width),
            2 * (self.length + self.height),
            2 * (self.height + self.width),
        )

    def _volume(self) -> int:
        return self.length * self.width * self.height

    def ribbon_length(self) -> int:
        return self._volume() + min(self._perimeters())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    presents = [Present.parse(line) for line in text.splitlines()]
    total_wrapping_paper_area = sum(
        present.wrapping_paper_area() for present in presents
    )
    print(total_wrapping_paper_area)

    total_ribbon_length = sum(present.ribbon_length() for present in presents)
    print(total_ribbon_length)


if __name__ == "__main__":
    main()
