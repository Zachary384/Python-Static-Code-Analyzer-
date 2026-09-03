import ast
from pathlib import Path

from analyzer.complexity import calculate_complexity
from analyzer.unused_variables import find_unused_variables
from analyzer.duplicates import find_duplicate_blocks
from analyzer.naming import find_naming_violations
from analyzer.metrics import calculate_metrics


def analyze_source(source):
    if not isinstance(source, str):
        return {
            "input_error": "Source must be a string.",
            "syntax_error": None,
        }

    try:
        ast.parse(source)
    except (SyntaxError, IndentationError) as error:
        return {
            "syntax_error": str(error),
        }

    return {
        "syntax_error": None,
        "complexity": calculate_complexity(source),
        "unused_variables": find_unused_variables(source),
        "duplicates": find_duplicate_blocks(source),
        "naming": find_naming_violations(source),
        "metrics": calculate_metrics(source),
    }


def analyze_file(path):
    path = Path(path)

    if not path.exists():
        return {
            "file_error": f"File does not exist: {path}",
            "syntax_error": None,
        }

    if not path.is_file():
        return {
            "file_error": f"Path is not a file: {path}",
            "syntax_error": None,
        }

    if path.suffix.lower() != ".py":
        return {
            "file_error": f"Unsupported file type: {path.suffix}",
            "syntax_error": None,
        }

    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return {
            "file_error": f"Unable to read file: {error}",
            "syntax_error": None,
        }

    result = analyze_source(source)
    result["file_error"] = None

    return result