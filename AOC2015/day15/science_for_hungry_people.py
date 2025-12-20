import argparse
from dataclasses import dataclass
from pathlib import Path
import re


INGREDIENT_REGEX = r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
MAX_INGREDIENTS = 100
CALORIES = 500


@dataclass(frozen=True)
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @staticmethod
    def parse(text: str) -> "Ingredient":
        ingredient_match = re.match(INGREDIENT_REGEX, text)
        if not ingredient_match:
            raise ValueError
        name = ingredient_match.group(1)
        capacity = int(ingredient_match.group(2))
        durability = int(ingredient_match.group(3))
        flavor = int(ingredient_match.group(4))
        texture = int(ingredient_match.group(5))
        calories = int(ingredient_match.group(6))
        return Ingredient(name, capacity, durability, flavor, texture, calories)


def get_score(amounts: list[int], ingredients: list[Ingredient]) -> int:
    num_ingredients = len(ingredients)
    capacity = max(
        0, sum(amounts[i] * ingredients[i].capacity for i in range(num_ingredients))
    )
    durability = max(
        0, sum(amounts[i] * ingredients[i].durability for i in range(num_ingredients))
    )
    flavor = max(
        0, sum(amounts[i] * ingredients[i].flavor for i in range(num_ingredients))
    )
    texture = max(
        0, sum(amounts[i] * ingredients[i].texture for i in range(num_ingredients))
    )
    return capacity * durability * flavor * texture


def get_calories(amounts: list[int], ingredients: list[Ingredient]) -> int:
    return sum(amounts[i] * ingredients[i].calories for i in range(len(ingredients)))


def get_maximal_score(ingredients: list[Ingredient]) -> int:
    maximal_score = 0
    for amounts in _get_amounts(len(ingredients), MAX_INGREDIENTS):
        score = get_score(amounts, ingredients)
        maximal_score = max(maximal_score, score)
    return maximal_score


def get_maximal_score_for_restricted_calories(ingredients: list[Ingredient]) -> int:
    maximal_score = 0
    for amounts in _get_amounts(len(ingredients), MAX_INGREDIENTS):
        calories = get_calories(amounts, ingredients)
        if calories != CALORIES:
            continue
        score = get_score(amounts, ingredients)
        maximal_score = max(maximal_score, score)
    return maximal_score


def _get_amounts(length: int, total_amount: int):
    if length == 0:
        yield []
    else:
        for a in range(1, total_amount + 1):
            for x in _get_amounts(length - 1, total_amount - a):
                yield [a] + x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    ingredients = [Ingredient.parse(line) for line in text.splitlines()]
    maximal_score = get_maximal_score(ingredients)
    print(maximal_score)
    maximal_score = get_maximal_score_for_restricted_calories(ingredients)
    print(maximal_score)


if __name__ == "__main__":
    main()
