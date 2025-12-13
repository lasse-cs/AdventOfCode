from the_ideal_stocking_stuffer import check_attempt, minimum_with_leading_zeroes


def test_check_attempt():
    prefix = "abcdef"
    assert check_attempt(prefix, 609043, 5)


def test_minimum_with_leading_zeros():
    prefix = "abcdef"
    assert minimum_with_leading_zeroes(prefix, 5) == 609043
    prefix = "pqrstuv"
    assert minimum_with_leading_zeroes(prefix, 5) == 1048970
