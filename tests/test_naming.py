from analyzer.naming import find_naming_violations


def test_valid_snake_case_function_has_no_violation():
    source = """
def calculate_total():
    return 10
"""

    result = find_naming_violations(source)

    assert result == []


def test_invalid_function_name_is_reported():
    source = """
def CalculateTotal():
    return 10
"""

    result = find_naming_violations(source)

    assert result == [
        {
            "name": "CalculateTotal",
            "type": "function",
            "rule": "snake_case",
        }
    ]


def test_valid_pascal_case_class_has_no_violation():
    source = """
class StudentRecord:
    pass
"""

    result = find_naming_violations(source)

    assert result == []


def test_invalid_class_name_is_reported():
    source = """
class student_record:
    pass
"""

    result = find_naming_violations(source)

    assert result == [
        {
            "name": "student_record",
            "type": "class",
            "rule": "PascalCase",
        }
    ]
    
    
def test_valid_snake_case_variable_has_no_violation():
    source = """
def calculate():
    student_count = 10
    return student_count
"""

    result = find_naming_violations(source)

    assert result == []


def test_invalid_variable_name_is_reported():
    source = """
def calculate():
    studentCount = 10
    return studentCount
"""

    result = find_naming_violations(source)

    assert result == [
        {
            "name": "studentCount",
            "type": "variable",
            "rule": "snake_case",
        }
    ]


def test_single_letter_variable_is_processed_without_violation():
    source = """
def calculate():
    x = 10
    return x
"""

    result = find_naming_violations(source)

    assert result == []


def test_variable_name_containing_digit_is_processed_consistently():
    source = """
def calculate():
    value2 = 10
    return value2
"""

    result = find_naming_violations(source)

    assert result == []
    
    
def test_valid_upper_case_constant_has_no_violation():
    source = """
MAX_SIZE = 100
"""

    result = find_naming_violations(source)

    assert result == []


def test_multiple_identifier_types_use_correct_naming_rules():
    source = """
MAX_SIZE = 100

class student_record:
    pass

def CalculateTotal():
    studentCount = 10
    return studentCount
"""

    result = find_naming_violations(source)

    assert {
        "name": "student_record",
        "type": "class",
        "rule": "PascalCase",
    } in result

    assert {
        "name": "CalculateTotal",
        "type": "function",
        "rule": "snake_case",
    } in result

    assert {
        "name": "studentCount",
        "type": "variable",
        "rule": "snake_case",
    } in result

    assert not any(
        violation["name"] == "MAX_SIZE"
        for violation in result
    )
    
    
def test_invalid_module_level_constant_name_is_reported():
    source = """
maxSize = 100
"""

    result = find_naming_violations(source)

    assert {
        "name": "maxSize",
        "type": "constant",
        "rule": "UPPER_CASE",
    } in result
    
    
def test_long_valid_identifier_is_processed_without_violation():
    source = """
def calculate_total_for_all_registered_students_in_current_semester():
    return 10
"""

    result = find_naming_violations(source)

    assert result == []