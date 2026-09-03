from analyzer.unused_variables import find_unused_variables


def test_used_variable_is_not_reported():
    source = """
def calculate():
    value = 10
    return value
"""

    result = find_unused_variables(source)

    assert result == []


def test_unused_variable_is_reported():
    source = """
def calculate():
    value = 10
    return 5
"""

    result = find_unused_variables(source)

    assert result == ["value"]


def test_only_unused_variable_is_reported():
    source = """
def calculate():
    x = 10
    y = 20
    return x
"""

    result = find_unused_variables(source)

    assert result == ["y"]


def test_underscore_variable_is_ignored():
    source = """
def calculate():
    _temporary = 10
    return 5
"""

    result = find_unused_variables(source)

    assert result == []
    
    
def test_same_variable_name_in_different_functions_is_scoped_independently():
    source = """
def first():
    value = 10
    return value

def second():
    value = 20
    return 5
"""

    result = find_unused_variables(source)

    assert result == ["value"]


def test_function_parameter_is_not_treated_as_assigned_local_variable():
    source = """
def calculate(value):
    return 5
"""

    result = find_unused_variables(source)

    assert result == []
    
    
def test_augmented_assignment_variable_is_not_reported():
    source = """
def update():
    x = 1
    x += 1
    return x
"""

    result = find_unused_variables(source)

    assert result == []


def test_for_loop_variable_used_in_body_is_not_reported():
    source = """
def show(items):
    for item in items:
        print(item)
"""

    result = find_unused_variables(source)

    assert result == []


def test_unpacking_assignment_reports_only_unused_name():
    source = """
def unpack(values):
    a, b = values
    return a
"""

    result = find_unused_variables(source)

    assert result == ["b"]


def test_reassigned_variable_used_later_is_not_reported():
    source = """
def calculate():
    x = 1
    x = 2
    return x
"""

    result = find_unused_variables(source)

    assert result == []
    
    
def test_variable_used_inside_expression_is_not_reported():
    source = """
def calculate():
    value = 10
    return value + 5
"""

    result = find_unused_variables(source)

    assert result == []