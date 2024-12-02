from pathlib import Path
from argparse import ArgumentParser

Report = list[int]


def parse(filepath: Path) -> list[Report]:
    reports: list[Report] = []
    with filepath.open() as f:
        for report_line in f:
            report = parse_report(report_line)
            reports.append(report)
    return reports


def parse_report(report_line: str) -> Report:
    report = [int(x) for x in report_line.split(" ")]
    return report


def is_report_valid(report: Report, damp: bool = False) -> bool:
    report_length: int = len(report)
    if report_length < 2:
        return True

    increasing: bool = report[0] < report[1]
    for i in range(1, report_length):
        difference: int = report[i] - report[i - 1]
        if not increasing:
            difference = -difference
        if difference <= 0 or difference > 3:
            if damp:
                return _check_modified_reports(report, i)
            return False
    return True


def _check_modified_reports(report: Report, problem_index: int) -> bool:
    # The type of monotonicity may have been incorrectly identified
    # Otherwise, it is localised to indices being compared
    possible_error_locations = [0, problem_index - 1, problem_index]
    for possible_error_location in possible_error_locations:
        mod_report = report[:]
        mod_report.pop(possible_error_location)
        if is_report_valid(mod_report):
            return True
    return False


def count_valid_reports(report_list: list[Report], damp: bool = False) -> int:
    valid_counter = 0
    for report in report_list:
        if is_report_valid(report, damp):
            valid_counter += 1
    return valid_counter


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    reports: list[Report] = parse(file)
    number_valid_undamped: int = count_valid_reports(reports)
    print(f"Number of valid undamped reports {number_valid_undamped}")

    number_valid_damped: int = count_valid_reports(reports, True)
    print(f"Number of valid damped reports {number_valid_damped}")
