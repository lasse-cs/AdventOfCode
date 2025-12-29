import argparse
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class Scratchcard:
    number: int
    winners: set[int]
    actuals: set[int]

    def _overlap_count(self) -> int:
        return len(self.winners & self.actuals)

    def score(self) -> int:
        overlap_count = self._overlap_count()
        if not overlap_count:
            return 0
        return 2 ** (overlap_count - 1)

    def won_cards(self) -> list[int]:
        overlap_count = self._overlap_count()
        return [self.number + x + 1 for x in range(overlap_count)]

    @staticmethod
    def parse(text: str) -> "Scratchcard":
        card, rest = text.split(": ")
        number = int(card[5:])
        winner_string, actual_string = rest.split(" | ")
        winners = {int(x) for x in re.split(r"\s+", winner_string.strip())}
        actuals = {int(x) for x in re.split(r"\s+", actual_string.strip())}
        return Scratchcard(number, winners, actuals)


def get_won_card_counts(scratchcards: list[Scratchcard]) -> dict[int, int]:
    counts = {card.number: 1 for card in scratchcards}
    for card in scratchcards:
        won_cards = card.won_cards()
        for won_card in won_cards:
            counts[won_card] += counts[card.number]
    return sum(counts.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    scratchcards = [Scratchcard.parse(line) for line in text.splitlines()]
    score = sum(scratchcard.score() for scratchcard in scratchcards)
    print(score)
    won_cards = get_won_card_counts(scratchcards)
    print(won_cards)


if __name__ == "__main__":
    main()
