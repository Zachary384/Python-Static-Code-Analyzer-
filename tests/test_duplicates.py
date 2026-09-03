from analyzer.duplicates import find_duplicate_blocks


def test_three_line_duplicate_is_detected():
    source = """
x = 10
y = 20
print(x + y)

a = 1

x = 10
y = 20
print(x + y)
"""

    result = find_duplicate_blocks(source)

    assert len(result) == 1

    assert result[0]["lines"] == [
        "x = 10",
        "y = 20",
        "print(x + y)",
    ]

    assert result[0]["locations"] == [2, 8]


def test_source_without_duplicate_returns_empty_list():
    source = """
x = 10
y = 20
print(x + y)

a = 1
b = 2
print(a * b)
"""

    result = find_duplicate_blocks(source)

    assert result == []
    
    
def test_two_line_duplicate_is_not_reported():
    source = """
x = 10
y = 20

x = 10
y = 20
"""

    result = find_duplicate_blocks(source)

    assert result == []


def test_leading_and_trailing_whitespace_is_ignored():
    source = """
x = 10
y = 20
print(x + y)

    x = 10
    y = 20
    print(x + y)
"""

    result = find_duplicate_blocks(source)

    assert len(result) == 1

    assert result[0]["lines"] == [
        "x = 10",
        "y = 20",
        "print(x + y)",
    ]


def test_blank_and_comment_lines_are_ignored():
    source = """
x = 10
# first comment
y = 20

print(x + y)

x = 10

# second comment
y = 20
print(x + y)
"""

    result = find_duplicate_blocks(source)

    assert len(result) == 1

    assert result[0]["lines"] == [
        "x = 10",
        "y = 20",
        "print(x + y)",
    ]


def test_three_occurrences_report_all_locations():
    source = """
x = 10
y = 20
print(x + y)

x = 10
y = 20
print(x + y)

x = 10
y = 20
print(x + y)
"""

    result = find_duplicate_blocks(source)

    assert len(result) == 1
    assert result[0]["locations"] == [2, 6, 10]
    
    
def test_repeated_four_line_block_is_detected():
    source = """
x = 10
y = 20
total = x + y
print(total)

x = 10
y = 20
total = x + y
print(total)
"""

    result = find_duplicate_blocks(source)

    assert result != []

    assert any(
        block["locations"][0] == 2
        and len(block["locations"]) >= 2
        for block in result
    )