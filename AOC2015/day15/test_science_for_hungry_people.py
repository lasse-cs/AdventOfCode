from science_for_hungry_people import (
    Ingredient,
    get_maximal_score,
    get_score,
    get_maximal_score_for_restricted_calories,
)


def test_parse():
    text = "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"
    assert Ingredient.parse(text) == Ingredient("Butterscotch", -1, -2, 6, 3, 8)


def test_score():
    ingredients = [
        Ingredient("Butterscotch", -1, -2, 6, 3, 8),
        Ingredient("Cinnamon", 2, 3, -2, -1, 3),
    ]
    assert get_score([44, 56], ingredients) == 62842880


def test_get_maximal_score():
    ingredients = [
        Ingredient("Butterscotch", -1, -2, 6, 3, 8),
        Ingredient("Cinnamon", 2, 3, -2, -1, 3),
    ]
    assert get_maximal_score(ingredients) == 62842880


def test_get_maximal_score_restricted_calories():
    ingredients = [
        Ingredient("Butterscotch", -1, -2, 6, 3, 8),
        Ingredient("Cinnamon", 2, 3, -2, -1, 3),
    ]
    assert get_maximal_score_for_restricted_calories(ingredients) == 57600000
