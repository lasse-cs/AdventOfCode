import pytest
from reactor import count_svr_dac_fft_out_paths, count_paths, parse


@pytest.fixture
def connections():
    text = """aaa: you hhh
    you: bbb ccc
    bbb: ddd eee
    ccc: ddd eee fff
    ddd: ggg
    eee: out
    fff: out
    ggg: out
    hhh: ccc fff iii
    iii: out"""
    return parse(text)


@pytest.fixture
def server_connections():
    text = """svr: aaa bbb
    aaa: fft
    fft: ccc
    bbb: tty
    tty: ccc
    ccc: ddd eee
    ddd: hub
    hub: fff
    eee: dac
    dac: fff
    fff: ggg hhh
    ggg: out
    hhh: out"""
    return parse(text)


def test_parse(connections):
    assert connections["aaa"] == ["you", "hhh"]
    assert connections["you"] == ["bbb", "ccc"]


def test_count_paths(connections):
    assert count_paths(connections) == 5


def test_count_svr_dac_fft_out_paths(server_connections):
    assert count_svr_dac_fft_out_paths(server_connections) == 2
