from analyzer.metrics import calculate_metrics


def test_one_function_is_counted():
    source = """
def hello():
    return "Hello"
"""

    result = calculate_metrics(source)

    assert result["functions"] == 1
    assert result["classes"] == 0


def test_two_functions_are_counted():
    source = """
def first():
    pass

def second():
    pass
"""

    result = calculate_metrics(source)

    assert result["functions"] == 2
    assert result["classes"] == 0


def test_one_class_is_counted():
    source = """
class StudentRecord:
    pass
"""

    result = calculate_metrics(source)

    assert result["functions"] == 0
    assert result["classes"] == 1


def test_two_functions_and_one_class_are_counted():
    source = """
def first():
    pass

def second():
    pass

class StudentRecord:
    pass
"""

    result = calculate_metrics(source)

    assert result["functions"] == 2
    assert result["classes"] == 1
    
    
def test_empty_source_has_zero_line_counts():
    source = ""

    result = calculate_metrics(source)

    assert result["physical_lines"] == 0
    assert result["blank_lines"] == 0
    assert result["comment_lines"] == 0
    assert result["code_lines"] == 0


def test_blank_line_only_source_has_zero_code_lines():
    source = "\n\n"

    result = calculate_metrics(source)

    assert result["physical_lines"] == 2
    assert result["blank_lines"] == 2
    assert result["comment_lines"] == 0
    assert result["code_lines"] == 0


def test_comment_only_source_has_zero_code_lines():
    source = "# first comment\n# second comment"

    result = calculate_metrics(source)

    assert result["physical_lines"] == 2
    assert result["blank_lines"] == 0
    assert result["comment_lines"] == 2
    assert result["code_lines"] == 0


def test_one_line_program_has_correct_line_counts():
    source = "x = 10"

    result = calculate_metrics(source)

    assert result["physical_lines"] == 1
    assert result["blank_lines"] == 0
    assert result["comment_lines"] == 0
    assert result["code_lines"] == 1


def test_mixed_source_line_categories_are_counted_independently():
    source = "x = 10\n# comment\n\ny = 20"

    result = calculate_metrics(source)

    assert result["physical_lines"] == 4
    assert result["blank_lines"] == 1
    assert result["comment_lines"] == 1
    assert result["code_lines"] == 2