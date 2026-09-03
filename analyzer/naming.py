import ast
import re


def _is_snake_case(name):
    return re.fullmatch(
        r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*",
        name
    ) is not None


def _is_pascal_case(name):
    return re.fullmatch(
        r"[A-Z][A-Za-z0-9]*",
        name
    ) is not None


def _is_upper_case(name):
    return re.fullmatch(
        r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*",
        name
    ) is not None


def _get_assigned_names(target):
    names = []

    if isinstance(target, ast.Name):
        names.append(target.id)

    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            names.extend(_get_assigned_names(element))

    return names


def find_naming_violations(source):
    tree = ast.parse(source)

    violations = []

    # Module-level assignments are treated as constants for this project.
    for statement in tree.body:
        targets = []

        if isinstance(statement, ast.Assign):
            targets = statement.targets

        elif isinstance(statement, ast.AnnAssign):
            targets = [statement.target]

        for target in targets:
            for name in _get_assigned_names(target):
                if not _is_upper_case(name):
                    violations.append(
                        {
                            "name": name,
                            "type": "constant",
                            "rule": "UPPER_CASE",
                        }
                    )

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not _is_snake_case(node.name):
                violations.append(
                    {
                        "name": node.name,
                        "type": "function",
                        "rule": "snake_case",
                    }
                )

            for child in ast.walk(node):
                if isinstance(child, ast.Name):
                    if isinstance(child.ctx, ast.Store):
                        if not _is_snake_case(child.id):
                            violations.append(
                                {
                                    "name": child.id,
                                    "type": "variable",
                                    "rule": "snake_case",
                                }
                            )

        elif isinstance(node, ast.ClassDef):
            if not _is_pascal_case(node.name):
                violations.append(
                    {
                        "name": node.name,
                        "type": "class",
                        "rule": "PascalCase",
                    }
                )

    return violations