import ast


def _count_decisions(node):
    count = 0

    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        if isinstance(
            child,
            (ast.If, ast.For, ast.While, ast.ExceptHandler)
        ):
            count += 1

        count += _count_decisions(child)

    return count


def calculate_complexity(source):
    tree = ast.parse(source)

    complexities = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = 1 + _count_decisions(node)
            complexities[node.name] = complexity

    return complexities