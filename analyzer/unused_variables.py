import ast


def find_unused_variables(source):
    tree = ast.parse(source)

    unused = []

    for function in ast.walk(tree):
        if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assigned = set()
            used = set()

            for node in ast.walk(function):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        assigned.add(node.id)
                    elif isinstance(node.ctx, ast.Load):
                        used.add(node.id)

            for name in assigned:
                if name not in used and not name.startswith("_"):
                    unused.append(name)

    return sorted(unused)