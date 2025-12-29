from scratchcards import Scratchcard, get_won_card_counts


def test_parse():
    text = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    assert Scratchcard.parse(text) == Scratchcard(
        number=1, winners={41, 48, 83, 86, 17}, actuals={83, 86, 6, 31, 17, 9, 48, 53}
    )


def test_score():
    card = Scratchcard(
        number=1, winners={41, 48, 83, 86, 17}, actuals={83, 86, 6, 31, 17, 9, 48, 53}
    )
    assert card.score() == 8
    card = Scratchcard(
        number=5, winners={87, 83, 26, 28, 32}, actuals={88, 30, 70, 12, 93, 22, 82, 36}
    )
    assert card.score() == 0


def test_won_cards():
    card = Scratchcard(
        number=1, winners={41, 48, 83, 86, 17}, actuals={83, 86, 6, 31, 17, 9, 48, 53}
    )
    assert card.won_cards() == [2, 3, 4, 5]


def test_won_card_count():
    text = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    cards = [Scratchcard.parse(line.strip()) for line in text.splitlines()]
    assert get_won_card_counts(cards) == 30
