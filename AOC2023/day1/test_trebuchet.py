from trebuchet import calibration_value, word_calibration_value


def test_calibration_value():
    assert calibration_value("1abc2") == 12
    assert calibration_value("pqr3stu8vwx") == 38
    assert calibration_value("treb7uchet") == 77


def test_word_calibration_value():
    assert word_calibration_value("two1nine") == 29
