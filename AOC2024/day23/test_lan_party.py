from pathlib import Path
from pytest import FixtureRequest
import pytest
from lan_party import Network


@pytest.fixture
def network(request: FixtureRequest) -> Network:
    filename = request.param
    file: Path = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        return Network.parse(f)


@pytest.mark.parametrize("network", ("test_small_input.txt",), indirect=True)
def test_parse(network: Network) -> None:
    connections: dict[str, set[str]] = {
        "kh": {"tc", "qp"},
        "tc": {"qp", "kh", "dd"},
        "qp": {"kh", "tc"},
        "dd": {"tc"},
    }
    assert Network(connections) == network


@pytest.mark.parametrize("network", ("test_small_input.txt",), indirect=True)
def test_are_mutually_connected(network: Network):
    assert network.are_mutually_connected(["kh", "tc", "qp"])


@pytest.mark.parametrize("network", ("test_small_input.txt",), indirect=True)
def test_are_not_mutually_connected(network: Network):
    assert not network.are_mutually_connected(["kh", "tc", "dd"])


@pytest.mark.parametrize("network", ("test_input.txt",), indirect=True)
def test_find_mutual_connections(network: Network):
    mutuals: list[tuple[str, str, str]] = list(network.find_mutual_triples())
    assert len(mutuals) == 12


@pytest.mark.parametrize("network", ("test_input.txt",), indirect=True)
def test_find_mutual_triples_with_t(network: Network):
    mutuals: list[tuple[str, str, str]] = list(network.find_mutual_triples_with_t())
    assert len(mutuals) == 7


@pytest.mark.parametrize("network", ("test_input.txt",), indirect=True)
def test_find_maximal_mutual(network: Network):
    maximal_mutual: list[str] = network.find_maximal_mutual_component()
    formatted: str = network.format_maximal_mutual(maximal_mutual)
    assert formatted == "co,de,ka,ta"
