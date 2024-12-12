from pathlib import Path
import pytest
from pytest import FixtureRequest
from garden_groups import Garden, parse_file, Region, GardenPatch


@pytest.fixture
def test_garden(request: FixtureRequest) -> Garden:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    return parse_file(file)


@pytest.mark.parametrize("test_garden", ("test_small_input.txt",), indirect=True)
def test_parse(test_garden: Garden):
    expected_patches: list[list[str]] = [
        ["A", "A", "A", "A"],
        ["B", "B", "C", "D"],
        ["B", "B", "C", "C"],
        ["E", "E", "E", "C"],
    ]
    expected_regions: dict[str, list[Region]] = {
        "A": [
            Region(
                {
                    GardenPatch(0, 0),
                    GardenPatch(0, 1),
                    GardenPatch(0, 2),
                    GardenPatch(0, 3),
                }
            )
        ],
        "B": [
            Region(
                {
                    GardenPatch(1, 0),
                    GardenPatch(1, 1),
                    GardenPatch(2, 0),
                    GardenPatch(2, 1),
                }
            )
        ],
        "C": [
            Region(
                {
                    GardenPatch(1, 2),
                    GardenPatch(2, 2),
                    GardenPatch(2, 3),
                    GardenPatch(3, 3),
                }
            )
        ],
        "D": [Region({GardenPatch(1, 3)})],
        "E": [
            Region(
                {
                    GardenPatch(3, 0),
                    GardenPatch(3, 1),
                    GardenPatch(3, 2),
                }
            )
        ],
    }
    assert test_garden.patches == expected_patches
    assert test_garden.regions == expected_regions


@pytest.fixture
def region() -> Region:
    return Region(
        {
            GardenPatch(1, 2),
            GardenPatch(2, 2),
            GardenPatch(2, 3),
            GardenPatch(3, 3),
        }
    )


def test_region_area(region: Region):
    assert region.area() == 4


def test_region_perimeter(region: Region):
    assert region.perimeter() == 10


def test_region_price(region: Region):
    assert region.fence_cost() == 40


def test_region_sides(region: Region):
    assert region.sides() == 8


@pytest.mark.parametrize(
    argnames=["test_garden", "price"],
    argvalues=[
        ("test_small_input.txt", 140),
        ("test_holes_input.txt", 772),
        ("test_larger_input.txt", 1930),
    ],
    indirect=["test_garden"],
)
def test_total_fence_cost(test_garden: Garden, price: int):
    assert test_garden.total_fence_cost() == price


@pytest.mark.parametrize(
    argnames=["test_garden", "price"],
    argvalues=[
        ("test_small_input.txt", 80),
        ("test_holes_input.txt", 436),
        ("test_larger_input.txt", 1206),
        ("test_e_input.txt", 236),
        ("test_ab_input.txt", 368),
    ],
    indirect=["test_garden"],
)
def test_total_discount_fence_cost(test_garden: Garden, price: int):
    assert test_garden.total_discount_fence_cost() == price
