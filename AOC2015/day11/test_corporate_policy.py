from corporate_policy import (
    check_password,
    next_password,
    next_candidate_password,
    password_to_numbers,
    numbers_to_password,
)


def test_next_candidate():
    assert next_candidate_password([0, 0, 0, 0, 0, 0, 0, 0]) == [0, 0, 0, 0, 0, 0, 0, 1]


def test_conversion():
    password = "abcdefghijklmnop"
    assert numbers_to_password(password_to_numbers(password)) == password


def test_check_password():
    assert check_password(password_to_numbers("abcdffaa"))
    assert check_password(password_to_numbers("ghjaabcc"))
    assert not check_password(password_to_numbers("hijklmmn"))
    assert not check_password(password_to_numbers("abbceffg"))
    assert not check_password(password_to_numbers("abbcegjk"))


def test_next_password():
    assert next_password("abcdefgh") == "abcdffaa"
    assert next_password("ghijklmn") == "ghjaabcc"
