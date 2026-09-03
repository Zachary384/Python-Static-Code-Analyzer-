import time
from analyzer.core import analyze_source, analyze_file


def test_valid_source_has_no_syntax_error():
    source = """
def hello():
    return "Hello"
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None


def test_invalid_assignment_reports_syntax_error():
    source = "x ="

    result = analyze_source(source)

    assert result["syntax_error"] is not None


def test_incomplete_function_reports_syntax_error():
    source = "def calculate("

    result = analyze_source(source)

    assert result["syntax_error"] is not None


def test_invalid_indentation_reports_syntax_error():
    source = """
def hello():
return "Hello"
"""

    result = analyze_source(source)

    assert result["syntax_error"] is not None
    
    
def test_valid_source_returns_all_analysis_results():
    source = """
def CalculateTotal():
    unusedValue = 10

    if True:
        print("hello")

    return 5
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None

    assert "complexity" in result
    assert "unused_variables" in result
    assert "duplicates" in result
    assert "naming" in result
    assert "metrics" in result
    
    
def test_invalid_source_does_not_run_further_analysis():
    source = "x ="

    result = analyze_source(source)

    assert result["syntax_error"] is not None

    assert "complexity" not in result
    assert "unused_variables" not in result
    assert "duplicates" not in result
    assert "naming" not in result
    assert "metrics" not in result
    
    
def test_empty_source_returns_valid_empty_analysis():
    source = ""

    result = analyze_source(source)

    assert result["syntax_error"] is None
    assert result["complexity"] == {}
    assert result["unused_variables"] == []
    assert result["duplicates"] == []
    assert result["naming"] == []

    assert result["metrics"]["physical_lines"] == 0
    assert result["metrics"]["blank_lines"] == 0
    assert result["metrics"]["comment_lines"] == 0
    assert result["metrics"]["code_lines"] == 0
    assert result["metrics"]["functions"] == 0
    assert result["metrics"]["classes"] == 0


def test_blank_only_source_returns_no_findings():
    source = "\n\n"

    result = analyze_source(source)

    assert result["syntax_error"] is None
    assert result["complexity"] == {}
    assert result["unused_variables"] == []
    assert result["duplicates"] == []
    assert result["naming"] == []

    assert result["metrics"]["physical_lines"] == 2
    assert result["metrics"]["blank_lines"] == 2
    assert result["metrics"]["code_lines"] == 0


def test_comment_only_source_returns_no_findings():
    source = "# first comment\n# second comment"

    result = analyze_source(source)

    assert result["syntax_error"] is None
    assert result["complexity"] == {}
    assert result["unused_variables"] == []
    assert result["duplicates"] == []
    assert result["naming"] == []

    assert result["metrics"]["physical_lines"] == 2
    assert result["metrics"]["comment_lines"] == 2
    assert result["metrics"]["code_lines"] == 0
    
    
def test_analyzed_source_is_not_executed(tmp_path):
    marker_file = tmp_path / "executed.txt"

    source = f"""
with open({str(marker_file)!r}, "w") as file:
    file.write("This source was executed")
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None
    assert not marker_file.exists()
    
    
def test_python_file_can_be_analyzed(tmp_path):
    source_file = tmp_path / "sample.py"

    source_file.write_text(
        "def hello():\n"
        "    return 'Hello'\n",
        encoding="utf-8",
    )

    result = analyze_file(source_file)

    assert result["syntax_error"] is None
    assert result["metrics"]["functions"] == 1
    assert result["metrics"]["classes"] == 0
    
    
def test_missing_file_reports_file_error(tmp_path):
    missing_file = tmp_path / "missing.py"

    result = analyze_file(missing_file)

    assert result["file_error"] is not None
    assert result["syntax_error"] is None
    
    
def test_non_python_file_reports_unsupported_file_type(tmp_path):
    source_file = tmp_path / "sample.txt"
    source_file.write_text("x = 10\n", encoding="utf-8")

    result = analyze_file(source_file)

    assert result["file_error"] is not None
    assert "unsupported" in result["file_error"].lower()


def test_directory_path_reports_file_error(tmp_path):
    directory = tmp_path / "source_folder"
    directory.mkdir()

    result = analyze_file(directory)

    assert result["file_error"] is not None
    
    
def test_invalid_utf8_file_reports_file_error(tmp_path):
    source_file = tmp_path / "invalid_encoding.py"

    source_file.write_bytes(b"\xff\xfe\xfa")

    result = analyze_file(source_file)

    assert result["file_error"] is not None
    assert result["syntax_error"] is None
    
    
def test_unsupported_source_type_reports_input_error():
    result = analyze_source(None)

    assert result["input_error"] is not None
    assert result["syntax_error"] is None
    
    
def test_multiple_issues_are_reported_together():
    source = """
def CalculateTotal():
    unused_value = 10

    if True:
        return 5

    return 0
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None

    assert result["complexity"]["CalculateTotal"] == 2

    assert "unused_value" in result["unused_variables"]

    assert {
        "name": "CalculateTotal",
        "type": "function",
        "rule": "snake_case",
    } in result["naming"]


def test_clean_program_has_no_quality_findings():
    source = """
class StudentRecord:
    pass

def calculate_total():
    value = 10
    return value
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None

    assert result["unused_variables"] == []
    assert result["duplicates"] == []
    assert result["naming"] == []

    assert result["complexity"]["calculate_total"] == 1
    assert result["metrics"]["functions"] == 1
    assert result["metrics"]["classes"] == 1
    
    
def test_malformed_nested_structure_reports_syntax_error():
    source = """
def outer():
    if True:
        for i in range(3)
            print(i)
"""

    result = analyze_source(source)

    assert result["syntax_error"] is not None

    assert "complexity" not in result
    assert "unused_variables" not in result
    assert "duplicates" not in result
    assert "naming" not in result
    assert "metrics" not in result


def test_empty_class_is_counted_and_has_no_naming_violation():
    source = """
class Example:
    pass
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None
    assert result["metrics"]["classes"] == 1
    assert result["naming"] == []
    
    
def test_multiple_findings_for_same_identifier_are_preserved():
    source = """
def calculate():
    studentCount = 10
    return 5
"""

    result = analyze_source(source)

    assert result["syntax_error"] is None

    assert "studentCount" in result["unused_variables"]

    assert {
        "name": "studentCount",
        "type": "variable",
        "rule": "snake_case",
    } in result["naming"]
    
    
def test_large_python_file_is_processed_within_performance_target(tmp_path):
    source_file = tmp_path / "large_source.py"

    source = "\n".join(
        f"VALUE_{i} = {i}"
        for i in range(1000)
    )

    source_file.write_text(source, encoding="utf-8")

    start = time.perf_counter()

    result = analyze_file(source_file)

    elapsed = time.perf_counter() - start

    assert result["file_error"] is None
    assert result["syntax_error"] is None

    assert result["metrics"]["physical_lines"] == 1000
    assert result["metrics"]["code_lines"] == 1000
    assert result["metrics"]["functions"] == 0
    assert result["metrics"]["classes"] == 0

    assert elapsed < 2.0