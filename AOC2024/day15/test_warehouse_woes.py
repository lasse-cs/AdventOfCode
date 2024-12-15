from pathlib import Path
import pytest
from pytest import FixtureRequest

from warehouse_woes import (
    Direction,
    Warehouse,
    WarehouseLocation,
    WarehouseObject,
    parse,
)


@pytest.fixture
def warehouse(request: FixtureRequest) -> Warehouse:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        warehouse, _ = parse(f)
        return warehouse


@pytest.fixture
def warehouse_directions(request: FixtureRequest) -> tuple[Warehouse, list[Direction]]:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        return parse(f)


@pytest.fixture
def wide_warehouse_directions(
    request: FixtureRequest,
) -> tuple[Warehouse, list[Direction]]:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        return parse(f, True)


@pytest.fixture
def wide_warehouse(
    request: FixtureRequest,
) -> Warehouse:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        warehouse, _ = parse(f, True)
    return warehouse


@pytest.mark.parametrize("warehouse", ("test_small_input.txt",), indirect=True)
def test_parse(warehouse: Warehouse) -> None:
    expected_map: list[list[WarehouseObject]] = [
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.BOX,
            WarehouseObject.FREE,
            WarehouseObject.BOX,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.ROBOT,
            WarehouseObject.FREE,
            WarehouseObject.BOX,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.BOX,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.BOX,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.BOX,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
    ]
    expected_robot_location: WarehouseLocation = WarehouseLocation(2, 2)
    expected_box_locations = {
        WarehouseLocation(1, 3),
        WarehouseLocation(1, 5),
        WarehouseLocation(2, 4),
        WarehouseLocation(3, 4),
        WarehouseLocation(4, 4),
        WarehouseLocation(5, 4),
    }
    assert warehouse.map == expected_map
    assert warehouse.robot_location == expected_robot_location
    assert warehouse.box_locations == expected_box_locations


@pytest.mark.parametrize("warehouse", ("test_small_input.txt",), indirect=True)
def test_execute_move_into_wall(warehouse: Warehouse):
    warehouse.execute_move(Direction(0, -1))
    assert warehouse.robot_location == WarehouseLocation(2, 2)


@pytest.mark.parametrize("warehouse", ("test_small_input.txt",), indirect=True)
def test_execute_move_into_free(warehouse: Warehouse):
    warehouse.execute_move(Direction(-1, 0))
    assert warehouse.robot_location == WarehouseLocation(1, 2)


@pytest.mark.parametrize("warehouse", ("test_small_input.txt",), indirect=True)
def test_execute_move_push_one(warehouse: Warehouse):
    warehouse.execute_move(Direction(-1, 0))
    warehouse.execute_move(Direction(0, 1))
    assert warehouse.robot_location == WarehouseLocation(1, 3)

    expected_box_locations = {
        WarehouseLocation(1, 4),
        WarehouseLocation(1, 5),
        WarehouseLocation(2, 4),
        WarehouseLocation(3, 4),
        WarehouseLocation(4, 4),
        WarehouseLocation(5, 4),
    }
    assert warehouse.box_locations == expected_box_locations


@pytest.mark.parametrize("warehouse", ("test_small_input.txt",), indirect=True)
def test_execute_move_push_multiple(warehouse: Warehouse):
    warehouse.execute_move(Direction(-1, 0))
    warehouse.execute_move(Direction(0, 1))
    warehouse.execute_move(Direction(0, 1))
    assert warehouse.robot_location == WarehouseLocation(1, 4)

    expected_box_locations = {
        WarehouseLocation(1, 5),
        WarehouseLocation(1, 6),
        WarehouseLocation(2, 4),
        WarehouseLocation(3, 4),
        WarehouseLocation(4, 4),
        WarehouseLocation(5, 4),
    }
    assert warehouse.box_locations == expected_box_locations


@pytest.mark.parametrize(
    argnames=["warehouse_directions", "total"],
    argvalues=[
        ("test_small_input.txt", 2028),
        ("test_large_input.txt", 10092),
    ],
    indirect=["warehouse_directions"],
)
def test_gps_coordinate_total(
    warehouse_directions: tuple[Warehouse, list[Direction]], total: int
):
    warehouse, directions = warehouse_directions
    for direction in directions:
        warehouse.execute_move(direction)
    assert warehouse.gps_coordinate_total() == total


@pytest.mark.parametrize(
    argnames=["wide_warehouse_directions", "total"],
    argvalues=[
        ("test_large_input.txt", 9021),
    ],
    indirect=["wide_warehouse_directions"],
)
def test_wide_gps_coordinate_total(
    wide_warehouse_directions: tuple[Warehouse, list[Direction]], total: int
):
    warehouse, directions = wide_warehouse_directions
    for direction in directions:
        warehouse.execute_move(direction)
    assert warehouse.gps_coordinate_total() == total


@pytest.mark.parametrize(
    "wide_warehouse", ("test_wide_small_input.txt",), indirect=True
)
def test_parse_wide(wide_warehouse: Warehouse) -> None:
    expected_map: list[list[WarehouseObject]] = [
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.BOX_START,
            WarehouseObject.BOX_END,
            WarehouseObject.BOX_START,
            WarehouseObject.BOX_END,
            WarehouseObject.ROBOT,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.BOX_START,
            WarehouseObject.BOX_END,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.FREE,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
        [
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
            WarehouseObject.WALL,
        ],
    ]
    expected_robot_location: WarehouseLocation = WarehouseLocation(3, 10)
    expected_box_locations = {
        WarehouseLocation(3, 6),
        WarehouseLocation(3, 8),
        WarehouseLocation(4, 6),
    }
    assert wide_warehouse.map == expected_map
    assert wide_warehouse.robot_location == expected_robot_location
    assert wide_warehouse.box_locations == expected_box_locations
