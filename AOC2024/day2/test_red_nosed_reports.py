import pytest
from red_nosed_reports import parse_report, is_report_valid, count_valid_reports, Report


def test_parse_report():
    report_line = "7 6 4 2 1"
    report = parse_report(report_line)
    assert report == [7, 6, 4, 2, 1]


@pytest.mark.parametrize(
    argnames=["report", "validity"],
    argvalues=[
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], False),
        ([8, 6, 4, 4, 1], False),
        ([1, 3, 6, 7, 9], True),
    ],
    ids=[
        "Safe Decreasing",
        "Unsafe increasing large gap",
        "Unsafe decreasing large gap",
        "Unsafe not monotonic",
        "Unsafe equal values",
        "Safe increasing",
    ],
)
def test_is_undamped_report_valid(report: Report, validity: bool):
    assert is_report_valid(report) == validity


@pytest.mark.parametrize(
    argnames=["report", "validity"],
    argvalues=[
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], True),
        ([8, 6, 4, 4, 1], True),
        ([1, 3, 6, 7, 9], True),
        ([14, 11, 14, 17, 18, 19], True),
    ],
    ids=[
        "Decreasing",
        "Increasing large gap",
        "Decreasing large gap",
        "Monotonic after remove one value",
        "Valid after remove equal values",
        "Safe increasing",
        "Valid after remove first",
    ],
)
def test_is_damped_report_valid(report: Report, validity: bool):
    assert is_report_valid(report, True) == validity


@pytest.fixture
def report_list():
    return [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9],
    ]


def test_count_valid_undamped_reports(report_list):
    assert count_valid_reports(report_list) == 2


def test_count_valid_damped_reports(report_list):
    assert count_valid_reports(report_list, True) == 4
