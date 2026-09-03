from analyzer.complexity import calculate_complexity


def test_function_without_decision_has_complexity_one():
    source = """
def hello():
    return "Hello"
"""

    result = calculate_complexity(source)

    assert result["hello"] == 1


def test_function_with_if_has_complexity_two():
    source = """
def check(x):
    if x > 0:
        return True
    return False
"""

    result = calculate_complexity(source)

    assert result["check"] == 2
    
    
def test_function_with_for_has_complexity_two():
    source = """
def repeat():
    for i in range(5):
        print(i)
"""

    result = calculate_complexity(source)

    assert result["repeat"] == 2


def test_function_with_while_has_complexity_two():
    source = """
def countdown(x):
    while x > 0:
        x -= 1
"""

    result = calculate_complexity(source)

    assert result["countdown"] == 2


def test_function_with_except_has_complexity_two():
    source = """
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
"""

    result = calculate_complexity(source)

    assert result["divide"] == 2


def test_function_with_if_and_elif_has_complexity_three():
    source = """
def classify(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    return "zero"
"""

    result = calculate_complexity(source)

    assert result["classify"] == 3


def test_nested_decisions_are_all_counted():
    source = """
def nested(x):
    if x > 0:
        if x > 10:
            return "large"
    return "other"
"""

    result = calculate_complexity(source)

    assert result["nested"] == 3
    
    
def test_empty_function_has_complexity_one():
    source = """
def empty():
    pass
"""

    result = calculate_complexity(source)

    assert result["empty"] == 1


def test_nested_loops_are_all_counted():
    source = """
def process(items):
    for item in items:
        while item > 0:
            item -= 1
"""

    result = calculate_complexity(source)

    assert result["process"] == 3


def test_multiple_functions_have_independent_complexity():
    source = """
def simple():
    return 1

def complex_function(x):
    if x > 0:
        return x
    return 0
"""

    result = calculate_complexity(source)

    assert result["simple"] == 1
    assert result["complex_function"] == 2
    
    
def test_nested_functions_have_independent_complexity():
    source = """
def outer():
    def inner():
        if True:
            return 1

    return 0
"""

    result = calculate_complexity(source)

    assert result["outer"] == 1
    assert result["inner"] == 2