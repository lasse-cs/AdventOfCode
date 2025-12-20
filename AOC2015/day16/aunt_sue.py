import argparse
from dataclasses import dataclass, fields
from pathlib import Path
import re


@dataclass(frozen=True)
class Aunt:
    number: int
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None

    def matches_spec(self, spec: "Aunt") -> bool:
        for field in fields(self):
            if field.name == "number":
                continue
            field_value = getattr(self, field.name)
            if field_value is None:
                continue
            spec_value = getattr(spec, field.name)
            if field_value != spec_value:
                return False
        return True

    def actually_matches_spec(self, spec: "Aunt") -> bool:
        if self.children is not None and self.children != spec.children:
            return False
        if self.cats is not None and self.cats <= spec.cats:
            return False
        if self.samoyeds is not None and self.samoyeds != spec.samoyeds:
            return False
        if self.pomeranians is not None and self.pomeranians >= spec.pomeranians:
            return False
        if self.akitas is not None and self.akitas != spec.akitas:
            return False
        if self.vizslas is not None and self.vizslas != spec.vizslas:
            return False
        if self.goldfish is not None and self.goldfish >= spec.goldfish:
            return False
        if self.trees is not None and self.trees <= spec.trees:
            return False
        if self.cars is not None and self.cars != spec.cars:
            return False
        if self.perfumes is not None and self.perfumes != spec.perfumes:
            return False
        return True

    @staticmethod
    def parse(text: str) -> "Aunt":
        split = re.split("Sue |: |, ", text)
        number = int(split[1])
        attributes = {split[i]: int(split[i + 1]) for i in range(2, len(split), 2)}
        return Aunt(number, **attributes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    aunts = [Aunt.parse(line) for line in text.splitlines()]
    spec_aunt = Aunt(
        0,
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )
    for aunt in aunts:
        if aunt.matches_spec(spec_aunt):
            print(aunt.number)
    for aunt in aunts:
        if aunt.actually_matches_spec(spec_aunt):
            print(aunt.number)


if __name__ == "__main__":
    main()
