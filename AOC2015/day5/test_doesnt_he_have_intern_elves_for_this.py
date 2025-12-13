from doesnt_he_have_intern_elves_for_this import is_actually_nice, is_nice


def test_is_nice():
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")


def test_is_actually_nice():
    assert is_actually_nice("qjhvhtzxzqqjkmpb")
    assert is_actually_nice("xxyxx")
    assert not is_actually_nice("uurcxstgmygtbstg")
    assert not is_actually_nice("ieodomkazucvgmuy")
