def test_split_long_line():
    line = "Standard Children 7-12 years old"
    lines = util.split_long_line(line, 17)
    assert len(lines) == 2
    assert lines[0] == "Standard Children"
    assert lines[1] == "7-12 years old"

def test_split_short_line():
    line = "Standard Adults"
    lines = util.split_long_line(line, 17)
    assert isinstance(lines, list)
    assert len(lines) == 1
    assert lines[0] == "Standard Adults"
