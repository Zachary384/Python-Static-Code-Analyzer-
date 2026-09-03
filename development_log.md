# AI-Assisted TDD Development Log

## Major Feature 1: Cyclomatic Complexity Analysis

### Iteration 1 – Base Complexity for a Simple Function

**Requirement/Test**

A function containing no decision statements should have a cyclomatic complexity of 1.

Test:

`test_function_without_decision_has_complexity_one`

---

**Test Status Before Implementation**

RED – pytest could not collect the test because the required
`analyzer.complexity` module had not yet been implemented.

Error:

`ModuleNotFoundError: No module named 'analyzer.complexity'`

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

My current pytest test imports:
from analyzer.complexity import calculate_complexity and expects calculate_complexity(source) to return a dictionary where a function containing no decision statements has a cyclomatic complexity of 1.

For this first iteration, implement only the minimum functionality necessary to satisfy this test.

Requirements:
- Use Python 3.
- Parse the source code statically.
- Do not execute the supplied source code.
- Return complexity results using function names as dictionary keys.
- A function with no decision statements has complexity 1.
- Do not implement if, elif, for, while, or except complexity yet.

---

**AI Response Summary**

The AI proposed a minimal implementation using Python's `ast` module.
The implementation parses the supplied source code using `ast.parse()`, traverses the syntax tree to identify function definitions, and assigns each detected function an initial cyclomatic complexity value of 1.

Decision structures were intentionally not implemented in this iteration.

---

**Decision**

Accepted.

---

**Justification**

The implementation was accepted because it satisfied the scope of the current TDD iteration.

It uses static AST parsing and does not execute the analysed source code.
It also avoids implementing functionality that has not yet been required by the current test.

---

**Changes Made**

Created:

`analyzer/complexity.py`

The initial implementation detects function definitions and returns a base complexity value of 1 for each function.

No manual modification to the AI-generated implementation was required during this iteration.

---

**Test Status After Implementation**

GREEN – the automated test passed successfully.

Result:

`1 passed in 0.03s`

---

**Evidence**

- `01_complexity_red_module_missing.png`
- `02_complexity_green_base_complexity.png`

---

**Notes / Problems Identified**

The current implementation only assigns a base complexity of 1.

It does not yet increase complexity for decision structures such as `if`, `elif`, `for`, `while`, or `except`.

These behaviours will be introduced and tested incrementally in subsequent TDD iterations.


### Iteration 2 – Complexity of an If Statement

**Requirement/Test**

Each `if` decision should increase the cyclomatic complexity of a function by 1.

A function containing one `if` statement should therefore have complexity 2.

Test:

`test_function_with_if_has_complexity_two`

---

**Test Status Before Implementation**

RED – the existing implementation passed the original base-complexity test but failed the newly introduced `if` statement test.

Expected complexity: 2

Actual complexity: 1

Test result:

`1 failed, 1 passed`

This demonstrated that the existing implementation correctly handled the base complexity of a function but did not yet count an `if` statement as a decision point.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The current implementation of calculate_complexity(source) successfully passes the test for a function with no decision statements, returning a base cyclomatic complexity of 1.

I have now added a new failing pytest test. The test uses:

def check(x):
    if x > 0:
        return True
    return False

The expected complexity is 2, but the current implementation returns 1.

Modify the existing implementation with the minimum change necessary to make an `if` statement increase the complexity of its containing function by 1.

Requirements:
- Preserve the existing behaviour where a function with no decisions
  has complexity 1.
- Use static AST analysis only.
- Do not execute the supplied source code.
- Count each `if` statement as one additional decision point.
- Do not add support for `for`, `while`, or `except` yet.
- Do not rewrite unrelated parts of the implementation.

---

**AI Response Summary**

The AI proposed modifying the existing AST-based implementation so that each function still starts with a base complexity of 1, while the AST of that function is traversed to identify `ast.If` nodes.

For each detected `if` statement, the function's complexity is incremented by 1.

The proposed change was limited to `if` statements and did not add support for loops or exception handlers.

---

**Decision**

Accepted.

---

**Justification**

The proposed change was accepted because it directly addressed the failing test while preserving the behaviour verified by the existing test.

The implementation continues to use static AST analysis and does not execute the supplied source code.

The change was also appropriately limited in scope because unsupported decision structures such as `for`, `while`, and `except` were not implemented prematurely.

---

**Changes Made**

Modified `analyzer/complexity.py`.

The function now traverses each function's AST and increments the complexity value for every detected `ast.If` node.

No manual modification to the AI-proposed implementation was made in this iteration.

---

**Test Status After Implementation**

GREEN – both automated complexity tests passed after the implementation was updated.

Test result:

`2 passed in 0.04s`

The original base-complexity behaviour remained correct, while the newly introduced `if` statement behaviour was successfully implemented.

---

**Evidence**

- `03_complexity_red_if_statement.png`
- `04_complexity_green_if_statement.png`

---

**Notes / Problems Identified**

The implementation currently supports the base complexity and `if` statements only.

Other decision structures defined in the specification, including `for`, `while`, and `except`, have not yet been implemented or verified by automated tests.

These behaviours will be introduced incrementally in later TDD iterations.


### Iteration 3 – Other Decision Structures

**Requirement/Test**

The complexity analyzer should count the remaining decision structures defined in the specification.

The following behaviours are tested:

- each `for` statement increases complexity by 1;
- each `while` statement increases complexity by 1;
- each `except` handler increases complexity by 1;
- an `if` followed by an `elif` should contribute two decision points;
- nested decision structures should all be counted.

Tests:

`test_function_with_for_has_complexity_two`

`test_function_with_while_has_complexity_two`

`test_function_with_except_has_complexity_two`

`test_function_with_if_and_elif_has_complexity_three`

`test_nested_decisions_are_all_counted`

---

**Test Status Before Implementation**

RED – the expanded complexity test suite revealed that the current implementation only partially supported the required decision structures.

Test result:

`3 failed, 4 passed`

The following new tests failed:

- `for`: expected complexity 2, actual complexity 1.
- `while`: expected complexity 2, actual complexity 1.
- `except`: expected complexity 2, actual complexity 1.

The tests for `if/elif` and nested `if` statements passed without any change to the production code.

---

**AI Output Evaluation**

Testing showed that the existing AI-generated implementation supported more behaviour than had been explicitly requested in Iteration 2.

The nested `if` test passed because the implementation uses `ast.walk()`, which traverses descendant nodes inside the function. Therefore, both the outer and inner `ast.If` nodes were counted.

The `if/elif` test also passed. In Python's AST representation, an `elif` branch is represented using another `ast.If` node, so the existing implementation counted both decision points.

However, the implementation failed the `for`, `while`, and `except` tests because it currently increments complexity only when an `ast.If` node is encountered.

The test results therefore identified three missing decision structures in the AI-generated implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The current calculate_complexity(source) implementation uses Python's AST and already counts ast.If nodes.

I expanded the automated test suite to evaluate additional decision structures.

Current pytest result:

3 failed, 4 passed

The failing behaviours are:
- A function containing one `for` loop returns complexity 1 instead of 2.
- A function containing one `while` loop returns complexity 1 instead of 2.
- A function containing one `except` handler returns complexity 1 instead of 2.

The existing tests for a simple function, `if`, `if/elif`, and nested `if` statements already pass.

Modify the existing implementation with the minimum change necessary to support the three failing behaviours.

Requirements:
- Preserve all currently passing behaviour.
- Each `for` statement increases complexity by 1.
- Each `while` statement increases complexity by 1.
- Each `except` handler increases complexity by 1.
- Continue using static AST analysis only.
- Do not execute the supplied source code.
- Do not rewrite unrelated parts of the implementation.

---

**AI Response Summary**

The AI proposed extending the existing `isinstance()` check rather than rewriting the complexity analyzer.

The decision-node tuple was expanded from only `ast.If` to include `ast.For`, `ast.While`, and `ast.ExceptHandler`.

Each matching AST node increments the function's complexity by 1.

The existing AST traversal and base-complexity logic were left unchanged.

---

**Decision**

Accepted.

---

**Justification**

The proposed modification was accepted because it directly addresses all three failing tests while preserving the existing design.

The change is small and focused, continues to use static AST analysis, and does not modify unrelated behaviour that is already passing its tests.

---

**Changes Made**

Modified `analyzer/complexity.py` by extending the decision-node check to include:

- `ast.For`
- `ast.While`
- `ast.ExceptHandler`

No manual modification to the AI-proposed solution was required before testing.

---

**Test Status After Implementation**

GREEN – all seven automated complexity tests passed after the implementation was extended.

Test result:

`7 passed in 0.05s`

The newly added support for `for`, `while`, and `except` satisfied all previously failing tests.

All previously passing tests also continued to pass, indicating that the modification did not introduce a regression in the behaviours already implemented.

---

**Evidence**

- `05a_complexity_red_other_decisions.png`
- `05b_complexity_red_other_decisions_summary.png`
- `06_complexity_green_other_decisions.png`

---

**Notes / Problems Identified**

The current implementation now supports all decision structures defined in the initial complexity specification: `if`, `elif`, `for`, `while`, and `except`.

Testing also confirmed that nested `if` statements and `if/elif` structures are handled by the AST-based traversal.

Further testing is still required for boundary and exceptional cases, particularly multiple functions and the independence of complexity results between functions.


### Iteration 4 – Boundary and Exceptional Complexity Cases

**Requirement/Test**

Additional tests were introduced to verify boundary and exceptional behaviour of the complexity analyzer.

The following behaviours are tested:

- an empty function containing only `pass` has complexity 1;
- nested loop decision points are all counted;
- multiple functions in the same source are analysed independently.

Tests:

`test_empty_function_has_complexity_one`

`test_nested_loops_are_all_counted`

`test_multiple_functions_have_independent_complexity`

---

**Test Status Before Further Implementation**

GREEN – all three newly introduced boundary and exceptional-case tests passed against the existing implementation.

The complete complexity test suite produced:

`10 passed in 0.04s`

No additional production-code modification was required.

---

**Evaluation**

The existing AST-based implementation successfully handled the additional boundary and exceptional cases.

An empty function correctly retained the base complexity of 1 because no decision nodes were present.

Nested `for` and `while` statements were both detected through `ast.walk()`, resulting in the expected complexity of 3.

Multiple functions in the same source were also analysed independently, with separate complexity values stored using their function names.

---

**Decision**

Accepted without modification.

---

**Changes Made**

No changes were made to `analyzer/complexity.py`.

Only three additional automated tests were added to `tests/test_complexity.py`.


---

**Evidence**

- `07_complexity_boundary_tests.png`

---

**Notes / Problems Identified**

No new defect was identified by these tests.

The complexity implementation passed all 10 current automated tests, including normal behaviour, nested decision structures, boundary cases, and multiple functions.



## Major Feature 2: Unused Variable Detection

### Iteration 1 – Basic Unused Variable Behaviour

**Requirement/Test**

The analyzer should identify local variables that are assigned but never referenced within the same function scope.

The following behaviours are tested:

- a used local variable is not reported;
- an unused local variable is reported;
- when multiple variables exist, only the unused variable is reported;
- variables beginning with `_` are treated as intentionally unused.

Tests:

`test_used_variable_is_not_reported`

`test_unused_variable_is_reported`

`test_only_unused_variable_is_reported`

`test_underscore_variable_is_ignored`

---

**Test Status Before Implementation**

RED – pytest could not collect the unused-variable tests because the required `analyzer.unused_variables` module had not yet been implemented.

Error:

`ModuleNotFoundError: No module named 'analyzer.unused_variables'`

The existing complexity tests remained present, but test collection was interrupted when pytest attempted to import the new unused-variable analysis module.

This confirms that the automated tests were created before the production implementation.
---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

I have written automated pytest tests for a new feature: unused variable detection.

The tests import:

from analyzer.unused_variables import find_unused_variables

The function find_unused_variables(source) should analyse Python source code statically and return a list of local variable names that are assigned but never referenced within the same function.

Current required behaviours:

1. A used local variable must not be reported.
2. An unused local variable must be reported.
3. When multiple variables exist, only the unused variable should be reported.
4. Variables beginning with "_" should be treated as intentionally unused and should not be reported.

Requirements:
- Use Python 3.
- Use static AST analysis.
- Do not execute the supplied source code.
- Analyse local variables inside functions.
- Return a list of unused variable names.
- Do not add advanced scope handling beyond what is required by the current tests.
- Implement only the minimum functionality necessary to satisfy the current tests.

---

**AI Response Summary**

The AI proposed a minimal AST-based implementation.

The implementation traverses the parsed Python syntax tree and records variable names appearing in `Store` context as assigned variables and names appearing in `Load` context as used variables.

A variable is reported as unused when it is assigned but never loaded, unless its name begins with `_`.

The returned list is sorted to provide deterministic test results.

---

**Decision**

Accepted.

---

**Justification**

The implementation was accepted because it directly addresses the four current automated tests using static AST analysis.

It does not execute the analysed source code and keeps the implementation small enough for the current TDD iteration.

Advanced scope handling has intentionally not been added yet so that future tests can evaluate whether the initial approach makes incorrect assumptions.

---

**Changes Made**

Created `analyzer/unused_variables.py`.

The initial implementation:

- parses the supplied Python source code using `ast.parse()`;
- traverses the AST using `ast.walk()`;
- records variable names in `ast.Store` context as assigned variables;
- records variable names in `ast.Load` context as used variables;
- identifies variables that are assigned but never used;
- ignores variable names beginning with `_`;
- sorts the returned unused-variable list to provide deterministic results.

No manual modification to the AI-proposed implementation was required before the initial test execution.

---

**Test Status After Implementation**

GREEN – all four basic unused-variable tests passed after the initial implementation was added.

The complete regression test suite produced:

`14 passed in 0.05s`

This consisted of 10 existing cyclomatic-complexity tests and 4 new unused-variable tests.

The previously implemented complexity functionality continued to pass, indicating that the new feature introduced no detected regression.

---

**Evidence**

- `08_unused_variables_red_module_missing.png`
- `09_unused_variables_green_basic.png`

---

**Notes / Problems Identified**

The initial implementation satisfies the current basic requirements.

However, it collects assigned and used variable names across the entire AST into global sets. It does not distinguish between individual function scopes.

This may cause incorrect results when the same variable name is used in different functions. Additional scope-specific tests are required to evaluate this limitation.


### Iteration 2 – Function Scope and Parameters

**Requirement/Test**

Additional tests were introduced to evaluate whether unused-variable analysis correctly handles function scope and function parameters.

The following behaviours are tested:

- variables with the same name in different functions must be analysed independently;
- function parameters must not automatically be treated as assigned local variables.

Tests:

`test_same_variable_name_in_different_functions_is_scoped_independently`

`test_function_parameter_is_not_treated_as_assigned_local_variable`

---

**Test Status Before Implementation**

RED – the additional scope test exposed a defect in the existing AI-generated implementation.

Test result:

`1 failed, 15 passed`

The failing test was:

`test_same_variable_name_in_different_functions_is_scoped_independently`

Expected result:

`["value"]`

Actual result:

`[]`

The function-parameter test passed without requiring any implementation change.

---

**AI Output Evaluation**

The initial AI-generated implementation collected assigned and used variable names into two sets across the entire parsed source file.

This approach passed the basic unused-variable tests but made an incorrect assumption that variables with the same name could be treated as the same variable regardless of function scope.

The new test demonstrated the defect. A variable named `value` was used inside `first()` but unused inside `second()`. Because the implementation combined both functions into the same `assigned` and `used` sets, the use of `value` in `first()` incorrectly prevented the unused `value` in `second()` from being reported.

The parameter test passed, confirming that function parameters were not incorrectly treated as local assignments by the current implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The current unused-variable implementation uses Python's AST and collects all assigned variables into one set and all used variables into another set across the entire source file.

The existing basic tests passed, but an additional scope test exposed a bug.

The failing source is:

def first():
    value = 10
    return value

def second():
    value = 20
    return 5

The expected result is:

["value"]

because `value` is used in first() but unused in second().

However, the current implementation returns:

[]

Current pytest result:

1 failed, 15 passed

Modify the implementation so that local variables are analysed independently for each function scope.

Requirements:
- Preserve all currently passing tests.
- Analyse assignments and uses separately for each function.
- A use of a variable in one function must not mark a variable with the same name as used in another function.
- Continue ignoring variable names beginning with `_`.
- Function parameters should not be reported as assigned local variables.
- Continue using static AST analysis only.
- Do not execute the supplied source code.
- Make the minimum change necessary to correct the scope defect.

---

**AI Response Summary**

The AI proposed changing the analysis from file-wide variable tracking to per-function variable tracking.

The revised implementation first identifies each function definition.
For every function, separate `assigned` and `used` sets are created and populated by traversing that function's AST.

Unused variables are then determined independently for each function before being added to the final result.

The existing underscore-name filtering and deterministic sorting were preserved.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed modification directly addresses the scope defect identified by the failing automated test.

Separating assigned and used variables by function prevents a reference in one function from incorrectly affecting analysis of another function.

The proposed solution also preserves the existing AST-based static analysis approach and does not intentionally alter unrelated behaviour.

---

**Changes Made**

Modified `analyzer/unused_variables.py`.

The previous file-wide `assigned` and `used` sets were replaced with separate sets created for each detected function.

Unused-variable detection is now performed independently for each function scope.

No additional manual modification to the AI-proposed fix was made before running the regression test suite.

---

**Test Status After Implementation**

GREEN – the complete automated test suite passed after the function-scope defect was corrected.

Test result:

`16 passed in 0.12s`

The previously failing function-scope test now passed, while all 15 previously passing tests continued to pass.

This confirmed that variables with the same name in different functions are now analysed independently and that the modification introduced no detected regression.

---

**Evidence**

- `10_unused_variables_red_scope_bug.png`
- `11_unused_variables_green_scope_fix.png`

---

**Notes / Problems Identified**

The file-wide scope defect identified in the initial AI-generated implementation was successfully corrected.

The current implementation now analyses ordinary functions independently.

However, the implementation still uses `ast.walk(function)` when analysing each function. Because this traversal also enters nested function definitions, nested lexical scopes may not be completely isolated.

This potential limitation has not yet been verified by an automated test.


### Iteration 3 – Boundary and Special Cases

**Requirement/Test**

Additional tests were introduced to evaluate unused-variable behaviour for common Python assignment patterns and boundary cases.

The following behaviours are tested:

- augmented assignment should not cause a used variable to be reported;
- a loop variable used inside the loop body should not be reported;
- tuple/unpacking assignment should identify only the unused target;
- a variable that is reassigned and later used should not be reported.

Tests:

`test_augmented_assignment_variable_is_not_reported`

`test_for_loop_variable_used_in_body_is_not_reported`

`test_unpacking_assignment_reports_only_unused_name`

`test_reassigned_variable_used_later_is_not_reported`

---

**Test Status Before Further Implementation**

GREEN – all four newly introduced boundary and special-case tests passed against the existing implementation.

The complete regression test suite produced:

`20 passed in 0.06s`

No additional production-code modification was required.

---

**Evaluation**

The existing AST-based implementation successfully handled all four additional assignment patterns.

Augmented assignment was handled correctly because the variable was subsequently loaded and therefore recognised as used.

Loop variables were correctly recognised through their `Store` context, while their references in the loop body were recognised through `Load` context.

Tuple/unpacking assignment was also handled correctly because each target name appeared independently in `Store` context. This allowed the unused target to be identified.

Repeated assignment did not cause a false positive when the variable was later referenced.

---

**Decision**

Accepted without modification.

---

**Changes Made**

No changes were made to `analyzer/unused_variables.py`.

Four additional automated tests were added to `tests/test_unused_variables.py` to verify boundary and special-case behaviour.

---

**Evidence**

- `12_unused_variables_boundary_tests.png`

---

**Notes / Problems Identified**

No new defect was identified by these tests.

The unused-variable implementation now passes 10 automated tests covering basic behaviour, function-scope separation, parameters, augmented assignment, loop variables, unpacking assignment, repeated assignment, and intentionally unused underscore-prefixed variables.

The potential behaviour of nested function scopes remains outside the current tested scope and was not pursued further in order to keep the implementation aligned with the defined project requirements.



## Major Feature 3: Duplicate Code Detection

### Iteration 1 – Basic Duplicate Behaviour

**Requirement/Test**

The analyzer should detect duplicated source-code blocks containing at least three consecutive non-empty, non-comment lines.

For the initial iteration, the following behaviours are tested:

- an identical three-line block appearing twice is reported as duplicate;
- source code containing no qualifying duplicate block returns an empty list;
- duplicate findings include the duplicated lines and their starting source-line locations.

Tests:

`test_three_line_duplicate_is_detected`

`test_source_without_duplicate_returns_empty_list`

---

**Test Status Before Implementation**

RED – pytest could not collect the duplicate-code tests because the required `analyzer.duplicates` module had not yet been implemented.

Error:

`ModuleNotFoundError: No module named 'analyzer.duplicates'`

The existing 20 automated tests from the complexity and unused-variable features remained present, but collection was interrupted when pytest attempted to import the new duplicate-code analysis module.

This confirms that the duplicate-code tests were created before the production implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

I have written automated pytest tests for a new duplicate-code detection feature.

The tests import:

from analyzer.duplicates import find_duplicate_blocks

The function find_duplicate_blocks(source) should detect duplicated blocks of Python source code.

Current required behaviour:

1. A duplicated block must contain at least three consecutive non-empty, non-comment source lines.
2. An identical three-line block appearing twice should be reported.
3. Source code with no qualifying duplicate block should return an empty list.
4. The result should include:
   - the duplicated normalized source lines;
   - the starting source-line numbers of each occurrence.
5. Leading and trailing whitespace should not affect comparison.

Use this result format:

[
    {
        "lines": ["line1", "line2", "line3"],
        "locations": [start_line_1, start_line_2]
    }
]

Requirements:
- Use Python 3.
- Analyse source text statically.
- Do not execute the supplied code.
- Ignore blank lines and comment-only lines when forming duplicate blocks.
- Use a minimum duplicate block size of three qualifying lines.
- Implement only the minimum functionality needed for the current tests.
- Do not add semantic clone detection or advanced duplicate analysis.

---

**AI Response Summary**

The AI proposed a line-based duplicate detector.

The implementation first splits the source code into physical lines, removes blank lines and comment-only lines, and normalizes each remaining line using `strip()`.

It then creates every consecutive three-line qualifying block and records the original starting source-line number of each block.

Blocks that occur at least twice are returned with their normalized lines and all detected starting locations.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation matches the current simplified duplicate-code definition and keeps the analysis limited to exact normalized line-based duplication.

It does not execute the supplied code and does not introduce unnecessary semantic clone analysis.

The implementation is intentionally minimal so that additional boundary tests can evaluate whitespace, comments, thresholds, and multiple occurrences later.

---

**Changes Made**

Created `analyzer/duplicates.py`.

The new implementation:
- removes blank lines and comment-only lines from duplicate comparison;
- normalizes qualifying lines using `strip()`;
- creates three-line duplicate candidates;
- records source-line locations;
- returns blocks appearing at least twice.

No manual modification to the AI-proposed implementation was made before the initial test execution.

---

**Test Status After Implementation**

GREEN – both initial duplicate-code tests passed after the new implementation was added.

The complete regression test suite produced:

`22 passed in 0.06s`

The duplicate detector successfully identified the tested three-line duplicate block and returned the expected source-line locations.

The existing 20 complexity and unused-variable tests also continued to pass, indicating that the new feature introduced no detected regression.


---

**Evidence**

- `13_duplicates_red_module_missing.png`
- `14_duplicates_green_basic.png`

---

**Notes / Problems Identified**

The initial implementation satisfies the current basic duplicate-code requirements.

However, only a simple three-line duplicate and a no-duplicate case have been verified so far.

Additional testing is required to evaluate the minimum three-line threshold, whitespace normalization, ignored blank/comment-only lines, and repeated occurrences.


### Iteration 2 – Threshold, Normalization and Repeated Occurrences

**Requirement/Test**

Additional tests were introduced to evaluate explicit boundary and normalization requirements of duplicate-code detection.

The following behaviours are tested:

- two repeated qualifying lines are below the minimum threshold and must not be reported;
- leading and trailing whitespace differences do not prevent duplicate detection;
- blank lines and comment-only lines are ignored during comparison;
- when the same duplicate block occurs three times, all three starting locations are reported.

Tests:

`test_two_line_duplicate_is_not_reported`

`test_leading_and_trailing_whitespace_is_ignored`

`test_blank_and_comment_lines_are_ignored`

`test_three_occurrences_report_all_locations`

---

**Test Status Before Further Implementation**

RED – the additional duplicate-code tests exposed a defect in the initial AI-generated implementation.

Test result:

`1 failed, 25 passed`

The failing test was:

`test_three_occurrences_report_all_locations`

Expected:

one duplicate block with locations `[2, 6, 10]`

Actual:

three duplicate blocks were returned.

The other newly introduced tests for the two-line threshold, whitespace normalization, and ignored blank/comment-only lines passed.

---

**Evaluation**

The initial implementation removed all blank and comment-only lines before creating three-line sliding windows.

This caused code lines that were originally separated by blank lines to become adjacent in the filtered representation.

As a result, when the same three-line block appeared three times, the detector correctly identified the intended block but also generated two additional overlapping blocks that crossed the original blank-line boundaries.

The failing test therefore exposed an incorrect assumption in the AI-generated implementation: ignoring blank and comment-only lines should not allow unrelated code regions to be joined into artificial consecutive duplicate blocks.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The current duplicate-code detector passed its initial tests but an additional test exposed a defect.

The detector currently removes all blank and comment-only lines and then creates sliding three-line windows from the remaining lines.

For this source:

x = 10
y = 20
print(x + y)

x = 10
y = 20
print(x + y)

x = 10
y = 20
print(x + y)

the expected result is one duplicate block:

["x = 10", "y = 20", "print(x + y)"]

with locations:

[2, 6, 10]

However, the implementation returns three duplicate blocks because it also creates sliding windows that cross the original blank-line boundaries.

Current pytest result:

1 failed, 25 passed

Modify the implementation with the minimum change necessary so that blank lines and comment-only lines do not become part of duplicate content but still prevent duplicate windows from joining separate code regions.

Requirements:
- Preserve all 25 currently passing tests.
- Minimum duplicate size remains three lines.
- Leading and trailing whitespace should still be ignored.
- Blank lines and comment-only lines should not be included in duplicate block content.
- Duplicate windows must not cross blank or comment-only line boundaries.
- All occurrences of the same qualifying block should still be reported.
- Do not execute the supplied source code.
- Do not add semantic clone detection.

---

**AI Response Summary**

The AI proposed preserving blank and comment-only lines as boundaries between code regions rather than removing them and joining all remaining code lines together.

The source is divided into contiguous regions of qualifying code.
Three-line duplicate windows are then generated independently within each region.

This prevents artificial duplicate blocks from crossing original blank or comment-only line boundaries while preserving normalized line comparison and source-line locations.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed change directly addresses the defect demonstrated by the failing test.

It preserves the existing three-line duplicate algorithm while changing only how qualifying code lines are grouped before sliding windows are generated.

This prevents artificial cross-boundary duplicates without introducing unnecessary semantic analysis.

---

**Changes Made**

Modified `analyzer/duplicates.py`.

Blank and comment-only lines are now treated as boundaries between contiguous code regions.

Duplicate windows are generated independently within each region instead of across one globally filtered list of source lines.

No additional manual modification to the AI-proposed fix was made before running the regression test suite.

---
**Regression Test Result**

RED – the first attempted fix introduced a regression.

Test result:

`1 failed, 25 passed`

The previously failing repeated-occurrence case was corrected, but the following existing test now failed:

`test_blank_and_comment_lines_are_ignored`

Expected:

one duplicate block

Actual:

no duplicate blocks were returned.

The attempted fix treated blank and comment-only lines as hard boundaries.
This prevented artificial cross-boundary windows, but it also prevented legitimate duplicate blocks containing ignored blank/comment-only lines from being matched.

---

**Evaluation of First Fix**

The first proposed correction was rejected after regression testing.

Although treating blank and comment-only lines as boundaries prevented artificial sliding windows between repeated blocks, this behaviour conflicted with the requirement that blank and comment-only lines should be ignored during duplicate comparison.

The failed regression test demonstrated that the correction was too restrictive.

A revised approach is required that preserves ignored lines while also preventing overlapping three-line windows from being reported as separate duplicate blocks.

---

**Decision After Regression Testing**

Rejected in its current form.

The proposed boundary-based fix was not retained because regression testing demonstrated that it violated an existing duplicate-detection requirement.

---

**AI Prompt First Fix**

The previous proposed fix treated blank and comment-only lines as hard boundaries between code regions.

Regression testing showed that this approach is incorrect.

Current pytest result:

1 failed, 25 passed

The failing test requires these two blocks to be considered duplicates despite different blank/comment-only lines appearing between their code lines:

Block 1:

x = 10
# first comment
y = 20

print(x + y)

Block 2:

x = 10

# second comment
y = 20
print(x + y)

Both should normalize to:

x = 10
y = 20
print(x + y)

However, another test with three repeated copies of the same three-line block must return only the intended duplicate block, not additional overlapping windows such as:

y = 20
print(x + y)
x = 10

Revise the duplicate-detection algorithm.

Requirements:
- Preserve all 25 currently passing tests.
- Blank and comment-only lines must be ignored during comparison.
- Leading and trailing whitespace must be ignored.
- A duplicate requires at least three qualifying code lines.
- Do not report artificial overlapping/cross-occurrence three-line windows as independent duplicate blocks.
- Report all starting locations of the same duplicate block.
- Prefer maximal meaningful duplicate blocks rather than every possible overlapping three-line window.
- Preserve original source-line locations.
- Use static source analysis only.
- Do not execute the supplied source code.

---

**AI Response Summary – Revised Fix**

The AI revised the duplicate-detection approach after the first fix caused a regression.

Instead of treating blank and comment-only lines as hard boundaries, the revised implementation again ignores these lines during duplicate comparison.

The implementation first generates all qualifying three-line duplicate candidates. It then performs a post-processing step to remove artificial overlapping candidates created by the sliding-window algorithm.

Candidates with more occurrences are considered first. A lower-frequency candidate is suppressed when it is a rotated version of an already accepted duplicate block and its source locations correspond to the same shift.

This allows legitimate duplicate blocks containing ignored blank or comment-only lines to remain detectable while preventing repeated three-line sequences from generating artificial rotated duplicate results.

---

**Decision – Revised Fix**

Accepted for testing.

---

**Justification – Revised Fix**

The revised proposal preserves the original requirement that blank and comment-only lines are ignored during comparison.

Unlike the previous boundary-based fix, it does not prevent legitimate duplicate blocks from spanning ignored lines.

The additional filtering is limited to artificial overlapping candidates created by repeated fixed-size sliding windows, directly addressing the failure observed in the repeated-occurrence test.

---

**Changes Made – Revised Fix**

Modified `analyzer/duplicates.py` again.

The hard-boundary region logic from the first attempted fix was removed.

The implementation now:
- ignores blank and comment-only lines during normalization;
- generates three-line duplicate candidates as before;
- sorts duplicate candidates by occurrence count;
- filters rotated overlapping candidates that are artifacts of repeated sliding windows;
- preserves the original source-line locations.

No additional manual modification to the revised AI proposal was made before regression testing.

---

**Test Status After Implementation**

GREEN – the revised duplicate-detection implementation passed the complete automated regression test suite.

Test result:

`26 passed in 0.12s`

The previously failing repeated-occurrence test now passed.

The regression introduced by the first attempted fix was also resolved: duplicate blocks containing ignored blank and comment-only lines were again detected correctly.

All previously passing complexity, unused-variable, and duplicate-code tests continued to pass.

---

**Final Decision**

Accepted.

---

**Final Justification**

Regression testing confirmed that the revised implementation satisfies both relevant behaviours:

- blank and comment-only lines are ignored during duplicate comparison;
- artificial overlapping windows generated across repeated occurrences are not reported as separate duplicate blocks.

The revised implementation therefore corrects the original defect without retaining the regression introduced by the first attempted fix.

---

**Evidence**

- `15_duplicates_red_cross_boundary_bug.png`
- `16_duplicates_red_comment_blank_regression.png`
- `17_duplicates_green_revised_fix.png`

---

**Notes / Problems Identified**

This iteration demonstrated that the initial fixed-size sliding-window approach could generate artificial overlapping duplicate candidates.

The first attempted correction solved that problem by treating ignored lines as boundaries, but regression testing showed that this conflicted with the requirement that blank and comment-only lines should be ignored during comparison.

The second correction retained ignored-line normalization and instead filtered artificial overlapping candidates.

The final regression suite passed all 26 tests.



## Major Feature 4: Naming Convention Analysis

### Iteration 1 – Basic Function and Class Naming

**Requirement/Test**

The naming analyzer should apply the simplified naming conventions defined in the Software Requirements Specification.

This iteration tests:

- a function named `calculate_total` is valid snake_case;
- a function named `CalculateTotal` is reported as a snake_case violation;
- a class named `StudentRecord` is valid PascalCase;
- a class named `student_record` is reported as a PascalCase violation.

Tests:

`test_valid_snake_case_function_has_no_violation`

`test_invalid_function_name_is_reported`

`test_valid_pascal_case_class_has_no_violation`

`test_invalid_class_name_is_reported`

---

**Test Status Before Implementation**

RED – pytest could not collect the naming-convention tests because the required `analyzer.naming` module had not yet been implemented.

Error:

`ModuleNotFoundError: No module named 'analyzer.naming'`

The existing 26 automated tests for complexity, unused variables, and duplicate-code detection remained present, but collection was interrupted when pytest attempted to import the new naming-analysis module.

This confirms that the naming tests were created before the production implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

I have written automated pytest tests for a new naming-convention analysis feature.

The tests import:

from analyzer.naming import find_naming_violations

Current required behaviour:

1. A function named calculate_total is valid snake_case and should produce no violation.
2. A function named CalculateTotal violates the function snake_case rule.
3. A class named StudentRecord is valid PascalCase and should produce no violation.
4. A class named student_record violates the class PascalCase rule.
5. Violations should be returned using this format:

[
    {
        "name": "identifier_name",
        "type": "function or class",
        "rule": "snake_case or PascalCase"
    }
]

Requirements:
- Use Python 3.
- Parse the supplied source code statically.
- Do not execute the supplied code.
- Use Python's ast module where appropriate.
- Implement only the minimum functionality needed for the current tests.
- Do not implement variable or constant naming yet.

---

**AI Response Summary**

The AI proposed an AST-based naming analyzer.

The implementation parses the supplied Python source using `ast.parse()` and traverses the syntax tree with `ast.walk()`.

Function definitions are checked against a simplified snake_case regular expression, while class definitions are checked against a simplified PascalCase regular expression.

When a violation is found, the implementation returns the identifier name, identifier type, and violated naming rule.

Variable and constant naming were intentionally not implemented in this iteration.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation matches the four current tests and the simplified naming requirements for functions and classes.

It uses static AST analysis and does not execute the supplied source code.

The implementation is intentionally limited to the current test scope so that variable and constant naming can be introduced in later TDD iterations.

---

**Changes Made**

Created `analyzer/naming.py`.

The implementation:
- parses source code using `ast.parse()`;
- identifies function and class definitions;
- validates function names using a simplified snake_case rule;
- validates class names using a simplified PascalCase rule;
- returns structured naming violations.

No manual modification to the AI-proposed implementation was made before the initial test execution.

---

**Test Status After Implementation**

GREEN – all four initial naming-convention tests passed after the new implementation was added.

The complete regression test suite produced:

`30 passed in 0.08s`

The naming analyzer correctly accepted valid snake_case function names and PascalCase class names, while reporting the tested invalid function and class names.

All 26 previously passing complexity, unused-variable, and duplicate-code tests continued to pass.

---

**Evidence**

- `18_naming_red_module_missing.png`
- `19_naming_green_function_class.png`

---

**Notes / Problems Identified**

No defect was identified by the initial function and class naming tests.

The current implementation only analyses function and class names. 
Local-variable and constant naming rules remain to be introduced in later iterations.


### Iteration 2 – Local Variables and Boundary Names

**Requirement/Test**

This iteration extends naming analysis to local variables and verifies the boundary identifier cases defined in the initial Test Design.

The following behaviours are tested:

- `student_count` is accepted as a valid snake_case local variable;
- `studentCount` is reported as a local-variable snake_case violation;
- the short valid identifier `x` is processed without a naming violation;
- the identifier `value2` is processed consistently as a valid simplified snake_case variable name.

Tests:

`test_valid_snake_case_variable_has_no_violation`

`test_invalid_variable_name_is_reported`

`test_single_letter_variable_is_processed_without_violation`

`test_variable_name_containing_digit_is_processed_consistently`

---

**Test Status Before Further Implementation**

RED – the new local-variable naming tests exposed missing functionality in the current naming analyzer.

Test result:

`1 failed, 33 passed`

The failing test was:

`test_invalid_variable_name_is_reported`

Expected:

`studentCount` should be reported as a local-variable violation of the snake_case naming rule.

Actual:

an empty violation list was returned.

The other three newly introduced tests passed because valid variable names did not generate false naming warnings.

---

**Evaluation**

The current implementation only inspects `ast.FunctionDef`, `ast.AsyncFunctionDef`, and `ast.ClassDef` nodes.

It does not inspect variable assignment targets.

Therefore, invalid local-variable names such as `studentCount` are not currently detected.

The failure represents missing functionality rather than a regression in the existing function or class naming behaviour.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The current naming analyzer already checks:
- function names using snake_case;
- class names using PascalCase.

Four additional tests have now been added for local-variable naming.

Current pytest result:

1 failed, 33 passed

The failing behaviour is:

def calculate():
    studentCount = 10
    return studentCount

Expected:

[
    {
        "name": "studentCount",
        "type": "variable",
        "rule": "snake_case"
    }
]

Actual:

[]

Required behaviour:
1. Local variables assigned inside functions must follow snake_case.
2. student_count is valid.
3. studentCount is a violation.
4. x is valid.
5. value2 should be accepted consistently as valid under the simplified snake_case rule already used by the project.
6. Preserve existing function and class naming behaviour.

Use Python's ast module.
Analyse source code statically and never execute it.
Implement only the minimum functionality required by these tests.
Do not implement constant naming yet.

---

**AI Response Summary**

The AI proposed extending the existing AST-based naming analyzer to inspect variable assignment targets inside functions.

For each function, the implementation traverses its AST and identifies `ast.Name` nodes whose context is `ast.Store`.

These names are treated as local-variable assignment targets and checked using the same simplified snake_case validation rule already used for
function names.

Function and class naming behaviour remains unchanged, and constant analysis is intentionally excluded from this iteration.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed change directly addresses the failing local-variable test.

Using `ast.Store` allows assignment targets to be distinguished from ordinary variable references, while restricting the additional traversal to functions keeps the implementation aligned with the requirement to analyse local variables.

The existing snake_case validator already accepts the tested boundary names `x` and `value2`.

---

**Changes Made**

Modified `analyzer/naming.py`.

The implementation now:
- retains existing function snake_case analysis;
- retains existing class PascalCase analysis;
- traverses function bodies for local variable assignment targets;
- identifies assigned names through `ast.Store`;
- applies the simplified snake_case rule to local variables.

Constant naming analysis was not added in this iteration.

---

**Test Status After Implementation**

GREEN – all four local-variable and boundary naming tests passed after the naming analyzer was extended.

The complete regression test suite produced:

`34 passed in 0.09s`

The analyzer now correctly reports `studentCount` as a local-variable snake_case violation while accepting `student_count`, `x`, and `value2`.

All previously passing complexity, unused-variable, duplicate-code, function-naming, and class-naming tests continued to pass.

---

**Decision**

Accepted.

---

**Evidence**

- `20_naming_red_variable_detection.png`
- `21_naming_green_variables.png`

---

**Notes / Problems Identified**

The local-variable naming functionality now satisfies the current tests.

The implementation uses `ast.Store` nodes inside functions to identify assigned local-variable names.

No regression was detected in the existing naming behaviour.

Constant naming analysis remains to be implemented in a later iteration.


### Iteration 3 – Constants and Multiple Identifier Types

**Requirement/Test**

This iteration addresses the remaining naming cases defined in the initial Test Design.

The following behaviours are tested:

- the module-level constant `MAX_SIZE` is accepted under the UPPER_CASE convention;
- multiple identifier types can be analysed in the same source file;
- function, class, and local-variable identifiers continue to use their respective naming rules when analysed together.

For the limited scope of this project, a module-level assignment whose name already follows the UPPER_CASE convention is treated as a constant.
The specification does not define a broader method for inferring whether an arbitrary module-level assignment was intended to be a constant.

Tests:

`test_valid_upper_case_constant_has_no_violation`

`test_multiple_identifier_types_use_correct_naming_rules`

---

**Test Status Before Further Implementation**

GREEN – both newly introduced naming tests passed against the existing implementation.

The complete regression test suite produced:

`36 passed in 0.10s`

No production-code modification was required for these tests.

---

**Evaluation**

The mixed-identifier test confirmed that the existing implementation can apply the function, class, and local-variable naming rules within the same source file.

However, evaluation of the constant test identified a limitation in the test design.

The test for `MAX_SIZE` passed because the current implementation does not analyse module-level assignments at all. Therefore, the absence of a violation does not demonstrate that constant naming analysis has actually been implemented.

The Software Requirements Specification states that constants should use UPPER_CASE, but it does not define how an arbitrary assignment should be classified as a constant.

Consequently, adding a test that treats an invalid-looking module-level name such as `maxSize` as definitely being a constant would introduce an assumption that is not explicitly defined by the specification.

---

**Decision**

Accepted with limitation.

No production-code modification was made solely to satisfy the current constant test.

The ambiguity in constant classification will be documented as a specification and test-design limitation rather than silently introducing a new classification rule.

---

**Changes Made**

No changes were made to `analyzer/naming.py`.

Two additional automated tests were added to `tests/test_naming.py` for the valid UPPER_CASE example and mixed identifier types.

---

**Evidence**

- `22_naming_constant_mixed_tests.png`

---

**Notes / Problems Identified**

The naming analyzer now passes all 10 tests derived from the initial naming test group.

Function, class, and local-variable naming behaviour is directly exercised by both valid and invalid examples.

Constant naming has weaker verification because the specification defines the required UPPER_CASE convention but does not define a reliable rule for determining whether an arbitrary module-level assignment represents a constant.

This limitation should be retained for discussion in the final evaluation rather than hidden by an unsupported implementation assumption.



## Major Feature 5: Code Metrics

### Iteration 1 – Function and Class Counts

**Requirement/Test**

The code-metrics component should report the number of functions and classes contained in supplied Python source code.

This iteration tests the normal function/class counting behaviours defined in the initial Test Design:

- one function produces a function count of 1;
- two functions produce a function count of 2;
- one class produces a class count of 1;
- a source containing two functions and one class reports both counts
  independently.

Tests:

`test_one_function_is_counted`

`test_two_functions_are_counted`

`test_one_class_is_counted`

`test_two_functions_and_one_class_are_counted`

---

**Test Status Before Implementation**

RED – pytest could not collect the code-metrics tests because the required `analyzer.metrics` module had not yet been implemented.

Error:

`ModuleNotFoundError: No module named 'analyzer.metrics'`

The existing 36 automated tests remained present, but collection was interrupted when pytest attempted to import the new metrics module.

This confirms that the metrics tests were created before the production implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

I have written four pytest tests for the first iteration of a code-metrics feature.

The tests import:

from analyzer.metrics import calculate_metrics

Current required behaviour:

1. Source containing one function should report:
   functions = 1
   classes = 0

2. Source containing two functions should report:
   functions = 2
   classes = 0

3. Source containing one class should report:
   functions = 0
   classes = 1

4. Source containing two functions and one class should report:
   functions = 2
   classes = 1

Requirements:
- Use Python 3.
- Parse the supplied source code statically.
- Do not execute the supplied code.
- Use Python's ast module where appropriate.
- Return the metrics in a dictionary.
- Implement only the function and class counts required by the current tests.
- Do not implement physical-line, blank-line, comment-line, or code-line metrics yet.

---

**AI Response Summary**

The AI proposed an AST-based implementation for the initial code-metrics feature.

The implementation parses the supplied Python source using `ast.parse()` and traverses the resulting syntax tree using `ast.walk()`.

Function definitions, including asynchronous functions, are counted using `ast.FunctionDef` and `ast.AsyncFunctionDef`. Class definitions are counted using `ast.ClassDef`.

The function returns the two current metrics in a dictionary.

Line-based metrics were intentionally excluded from this iteration.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation directly addresses the four current tests and uses Python's AST for static source analysis.

It does not execute the supplied source code and does not introduce functionality that belongs to later metrics iterations.

---

**Changes Made**

Created `analyzer/metrics.py`.

The implementation:
- parses source code using `ast.parse()`;
- traverses the syntax tree using `ast.walk()`;
- counts function and asynchronous-function definitions;
- counts class definitions;
- returns the function and class counts in a dictionary.

Physical-line, blank-line, comment-line, and code-line metrics were not implemented in this iteration.

No manual modification to the AI-proposed implementation was made before the initial test execution.

---

**Test Status After Implementation**

GREEN – all four initial code-metrics tests passed after the metrics implementation was added.

The complete regression test suite produced:

`40 passed in 0.09s`

The analyzer correctly counted one function, multiple functions, one class, and a combination of functions and classes.

All 36 previously passing tests continued to pass, indicating that the new metrics component introduced no detected regression.

---

**Evidence**

- `23_metrics_red_module_missing.png`
- `24_metrics_green_function_class_counts.png`

---

**Notes / Problems Identified**

No defect was identified by the initial function and class count tests.

The current implementation only provides function and class counts.
Physical-line, blank-line, comment-only-line, and code-line metrics remain to be implemented.


### Iteration 2 – Line Metrics and Boundary Cases

**Requirement/Test**

This iteration extends code metrics to physical-line, blank-line, comment-only-line, and code-line counts.

The line-counting convention used by the implementation is based on
`source.splitlines()`.

A line is classified as:

- blank when `line.strip()` is empty;
- comment-only when the stripped line begins with `#`;
- code otherwise.

The following behaviours are tested:

- empty source produces zero line counts;
- blank-line-only source contains no code lines;
- comment-only source contains no code lines;
- a one-line program is counted as one physical and one code line;
- mixed source counts code, comments, and blank lines independently.

Tests:

`test_empty_source_has_zero_line_counts`

`test_blank_line_only_source_has_zero_code_lines`

`test_comment_only_source_has_zero_code_lines`

`test_one_line_program_has_correct_line_counts`

`test_mixed_source_line_categories_are_counted_independently`

---

**Test Status Before Further Implementation**

RED – all five newly introduced line-metrics tests failed against the existing implementation.

Test result:

`5 failed, 40 passed`

Each failure raised:

`KeyError: 'physical_lines'`

The existing `calculate_metrics()` implementation only returned function and class counts. It did not yet provide physical-line, blank-line, comment-only-line, or code-line metrics.

All 40 previously implemented tests continued to pass.

---

**Evaluation**

The failures identify missing functionality rather than a regression.

The existing AST-based implementation correctly provides structural function and class counts, but line-category metrics require analysis of the original source text.

All five new tests fail at the first attempted access to `physical_lines`, confirming that the required line-metrics interface has not yet been implemented.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The current calculate_metrics(source) function already returns:

- functions
- classes

Five new pytest tests have been introduced for line metrics.

Current pytest result:

5 failed, 40 passed

All five failures currently raise:

KeyError: 'physical_lines'

Required additional metrics:

1. physical_lines
   Count all physical source lines using source.splitlines().

2. blank_lines
   A line is blank when line.strip() is empty.

3. comment_lines
   A line is comment-only when its stripped content begins with "#".

4. code_lines
   A line is a code line when it is neither blank nor comment-only.

Required examples:

- "" -> 0 physical, 0 blank, 0 comment, 0 code
- "\n\n" -> 2 physical, 2 blank, 0 comment, 0 code
- "# first comment\n# second comment" -> 2 physical, 0 blank, 2 comment, 0 code
- "x = 10" -> 1 physical, 0 blank, 0 comment, 1 code
- "x = 10\n# comment\n\ny = 20" -> 4 physical, 1 blank, 1 comment, 2 code

Requirements:
- Preserve the existing function and class metrics.
- Use Python 3.
- Do not execute the supplied source code.
- Preserve all currently passing tests.
- Implement only the required line metrics.

---

**AI Response Summary**

The AI proposed extending the existing metrics implementation with line-based analysis of the original source text.

The existing AST analysis remains responsible for counting functions and classes.

The source is additionally processed using `source.splitlines()` to determine the number of physical lines.

Each physical line is classified as exactly one of the following:

- blank, when `line.strip()` is empty;
- comment-only, when the stripped line begins with `#`;
- code, otherwise.

The resulting dictionary combines the four new line metrics with the existing function and class counts.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation directly addresses all five failing tests while preserving the existing structural metrics.

Using the original source text is appropriate for physical-line classification because blank and comment-only lines are not represented as ordinary executable nodes in the AST.

The implementation also preserves the project's static-analysis constraint and does not execute the supplied code.

---

**Changes Made**

Modified `analyzer/metrics.py`.

The implementation now:
- retains AST-based function counting;
- retains AST-based class counting;
- splits the original source into physical lines;
- counts blank lines;
- counts comment-only lines;
- counts remaining lines as code lines;
- returns all six required metrics in one dictionary.

No manual modification to the AI-proposed implementation was made before regression testing.

---

**Test Status After Implementation**

GREEN – all five line-metrics and boundary tests passed after the metrics implementation was extended.

The complete regression test suite produced:

`45 passed in 0.09s`

The analyzer correctly reports physical lines, blank lines, comment-only lines, and code lines for empty, blank-only, comment-only, one-line, and mixed source inputs.

The previously implemented function and class metrics also continued to pass, together with all complexity, unused-variable, duplicate-code, and naming tests.

---

**Decision**

Accepted.

---

**Evidence**

- `25a_metrics_red_line_metrics_missing.png`
- `25b_metrics_red_line_metrics_summary.png`
- `26_metrics_green_line_metrics.png`

---

**Notes / Problems Identified**

No new defect was identified after implementing the required line metrics.

The code-metrics component now provides all six metrics required by the current specification:

- physical lines;
- blank lines;
- comment-only lines;
- code lines;
- functions;
- classes.

The complete automated regression suite currently contains 45 passing tests.



## System Integration and Error Handling

### Iteration 1 – Syntax Validation

**Requirement/Test**

The integrated analyzer should validate supplied Python source before performing AST-dependent analysis.

Valid Python source should produce no syntax error.

Invalid Python source should be handled without allowing an uncaught `SyntaxError` to terminate the analyzer.

This iteration tests:

- valid Python source;
- an incomplete assignment;
- an incomplete function definition;
- invalid indentation.

Tests:

`test_valid_source_has_no_syntax_error`

`test_invalid_assignment_reports_syntax_error`

`test_incomplete_function_reports_syntax_error`

`test_invalid_indentation_reports_syntax_error`

---

**Test Status Before Implementation**

RED – pytest could not collect the new system-level syntax-validation tests because the required `analyzer.core` module had not yet been implemented.

Error:

`ModuleNotFoundError: No module named 'analyzer.core'`

The existing 45 automated feature tests remained present, but collection was interrupted when pytest attempted to import the new integrated analyzer module.

This confirms that the system-level tests were introduced before the production implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

I have written four pytest tests for a new integrated analyzer entry point.

The tests import:

from analyzer.core import analyze_source

Current required behaviour:

1. Valid Python source should return:
   syntax_error = None

2. Invalid assignment syntax such as:
   x =
   should return a non-None syntax_error value.

3. An incomplete function definition such as:
   def calculate(
   should return a non-None syntax_error value.

4. Invalid indentation should also return a non-None syntax_error value.

Requirements:
- Use Python 3.
- Validate syntax using ast.parse().
- Do not execute supplied source code.
- Catch syntax-related parsing errors instead of allowing them to crash the analyzer.
- Return results in a dictionary.
- Implement only syntax validation in this iteration.
- Do not call the other analysis modules yet.

---

**AI Response Summary**

The AI proposed a minimal integrated source-analysis entry point.

The implementation validates the supplied source using `ast.parse()`.

If parsing raises a syntax-related exception, the exception is caught and returned as a `syntax_error` value rather than being allowed to terminate the application.

For syntactically valid source, `syntax_error` is returned as `None`.

The other analysis components are intentionally not invoked in this iteration.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation directly addresses the four current syntax-validation tests.

It centralizes syntax checking in the future integrated analyzer entry point and prevents uncaught parsing errors from terminating the application.

The implementation also remains limited to the current TDD scope and does not prematurely integrate the five analysis components.

---

**Changes Made**

Created `analyzer/core.py`.

The new implementation:
- parses supplied source using `ast.parse()`;
- catches syntax-related parsing errors;
- returns a structured `syntax_error` result;
- returns `None` when source syntax is valid.

No other analysis functionality was added in this iteration.

---

**Test Status After Implementation**

GREEN – all four system-level syntax-validation tests passed after the integrated analyzer entry point was implemented.

The complete regression test suite produced:

`49 passed in 0.13s`

Valid Python source correctly returned no syntax error, while invalid assignment syntax, incomplete function syntax, and invalid indentation were handled without an uncaught parsing exception.

All 45 previously passing feature tests continued to pass.

---

**Decision**

Accepted.

---

**Evidence**

- `27_core_red_module_missing.png`
- `28_core_green_syntax_validation.png`

---

**Notes / Problems Identified**

The integrated analyzer now provides controlled syntax validation.

At this stage, `analyze_source()` does not yet invoke the individual complexity, unused-variable, duplicate-code, naming, or metrics components.

Those components will be integrated in the next iteration.


### Iteration 2 – Integration of Analysis Components

**Requirement/Test**

This iteration integrates the previously developed analysis components through the `analyze_source()` entry point.

For syntactically valid Python source, the integrated result should contain:

- cyclomatic complexity analysis;
- unused-variable analysis;
- duplicate-code analysis;
- naming-convention analysis;
- code metrics.

For syntactically invalid source, the analyzer should return the syntax error without proceeding to the other analysis components.

Tests:

`test_valid_source_returns_all_analysis_results`

`test_invalid_source_does_not_run_further_analysis`

---

**Test Status Before Further Implementation**

RED – the integration tests exposed missing orchestration functionality in the current `analyze_source()` implementation.

Test result:

`1 failed, 50 passed`

The failing test was:

`test_valid_source_returns_all_analysis_results`

Expected:

the result for valid Python source should contain the five analysis components:

- complexity;
- unused variables;
- duplicate code;
- naming violations;
- code metrics.

Actual:

`analyze_source()` returned only:

`{"syntax_error": None}`

The invalid-source integration test passed, confirming that invalid Python source is already rejected before further analysis is performed.

---

**Evaluation**

The current implementation successfully performs syntax validation but does not yet orchestrate the five previously developed analysis modules.

The failure represents missing integration functionality rather than a defect in the individual analysis components.

The passing invalid-source test also confirms that the existing syntax-validation guard should be preserved when integration is added.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The project already contains five independently tested analysis functions:

from analyzer.complexity import calculate_complexity
from analyzer.unused_variables import find_unused_variables
from analyzer.duplicates import find_duplicate_blocks
from analyzer.naming import find_naming_violations
from analyzer.metrics import calculate_metrics

The integrated entry point is:

from analyzer.core import analyze_source

The current implementation already validates syntax using ast.parse().

Current pytest result:

1 failed, 50 passed

For syntactically valid source, analyze_source(source) currently returns only:

{"syntax_error": None}

It must now return the results of all five analysis components using these keys:

- complexity
- unused_variables
- duplicates
- naming
- metrics

For syntactically invalid source:
- syntax_error must remain non-None;
- the five analysis components must not be executed or included in the returned result.

Requirements:
- Preserve the existing syntax-validation behaviour.
- Reuse the five existing analysis functions rather than reimplementing their algorithms.
- Do not execute supplied source code.
- Preserve all currently passing tests.
- Keep analyze_source() as the single integrated entry point.

---

**AI Response Summary**

The AI proposed integrating the five previously developed analysis components through the existing `analyze_source()` entry point.

The implementation imports and reuses the existing complexity, unused-variable, duplicate-code, naming, and metrics functions.

Syntax validation remains the first operation. If parsing fails, the function immediately returns the syntax error and does not invoke the other analysis components.

For valid source, the five component results are combined into one structured result dictionary.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation directly addresses the failing integration test without duplicating any of the previously developed analysis algorithms.

It preserves the existing syntax-validation guard and therefore prevents AST-dependent components from receiving syntactically invalid source.

The design also establishes `analyze_source()` as the single orchestration point for the complete static-analysis workflow.

---

**Changes Made**

Modified `analyzer/core.py`.

The integrated implementation now:
- validates source syntax before further analysis;
- preserves controlled syntax-error handling;
- calls the existing cyclomatic-complexity analyzer;
- calls the existing unused-variable analyzer;
- calls the existing duplicate-code analyzer;
- calls the existing naming-convention analyzer;
- calls the existing code-metrics analyzer;
- combines the component results into one dictionary.

No individual analysis algorithm was reimplemented inside `core.py`.

---

**Test Status After Implementation**

GREEN – both system-integration tests passed after the five analysis components were connected through `analyze_source()`.

The complete regression test suite produced:

`51 passed in 0.10s`

For syntactically valid source, the integrated analyzer now returns complexity, unused-variable, duplicate-code, naming, and metrics results.

For syntactically invalid source, analysis stops after syntax validation and no further component results are returned.

All previously passing tests continued to pass.

---

**Decision**

Accepted.

---

**Evidence**

- `29_core_red_analysis_integration.png`
- `30_core_green_analysis_integration.png`

---

**Notes / Problems Identified**

The five independently developed analysis components are now integrated through a single `analyze_source()` entry point.

No regression was detected in the existing component tests.

Further system-level testing is still required for empty input, combined result behaviour, result-format consistency, and source-safety behaviour.


### Iteration 3 – Empty and Non-Code Input Integration

**Requirement/Test**

The integrated analyzer should handle empty, blank-only, and comment-only Python source without crashing or producing false analysis findings.

This iteration verifies that:

- empty source produces a valid empty analysis;
- blank-only source produces no analysis findings;
- comment-only source produces no analysis findings;
- line metrics remain correct for these inputs;
- all five analysis components can safely participate in the integrated workflow for minimal source inputs.

Tests:

`test_empty_source_returns_valid_empty_analysis`

`test_blank_only_source_returns_no_findings`

`test_comment_only_source_returns_no_findings`

---

**Test Status Before Further Implementation**

GREEN – all three newly introduced empty and non-code integration tests passed against the existing implementation.

The complete regression test suite produced:

`54 passed in 0.15s`

No production-code modification was required.

---

**Evaluation**

The integrated analyzer successfully handled empty source, blank-only source, and comment-only source without raising an exception.

No false complexity, unused-variable, duplicate-code, or naming findings were produced for these inputs.

The metrics component also continued to distinguish physical, blank, comment-only, and code lines correctly when invoked through the integrated `analyze_source()` entry point.

This demonstrates that the independently developed components behave consistently when combined for minimal and non-code inputs.

---

**Decision**

Accepted without modification.

---

**Changes Made**

No production code was changed.

Three additional system-level tests were added to `tests/test_core.py` to verify empty, blank-only, and comment-only source behaviour.

---

**Evidence**

- `31_core_empty_noncode_integration.png`

---

**Notes / Problems Identified**

No new defect was identified.

The complete regression suite now contains 54 passing tests.

The integrated analyzer has been verified for valid source, invalid syntax, empty source, blank-only source, and comment-only source.


### Iteration 4 – Source Safety and Non-Execution

**Requirement/Test**

The static analyzer must inspect supplied Python source without executing that source.

A safety test was introduced using source code that would create a file if it were executed.

The test verifies that:

- the supplied source is syntactically valid;
- the integrated analyzer can process the source;
- the side-effect file is not created.

Test:

`test_analyzed_source_is_not_executed`

---

**Test Status Before Further Implementation**

GREEN – the source-safety test passed against the existing integrated implementation.

The complete regression test suite produced:

`55 passed in 0.17s`

No production-code modification was required.

---

**Evaluation**

The test supplied syntactically valid Python source that would create a temporary file if the source were executed.

After analysis, the temporary file did not exist.

This provides automated evidence that the integrated analyzer performs static analysis without executing the supplied source code.

The existing implementation therefore already satisfied the tested source-safety requirement.

---

**Decision**

Accepted without modification.

---

**Changes Made**

No production code was changed.

One additional system-level safety test was added to `tests/test_core.py`.

---

**Evidence**

- `32_core_source_not_executed.png`

---

**Notes / Problems Identified**

No new defect was identified.

The integrated analyzer has now been verified to process supplied source without executing it.

The complete automated regression suite currently contains 55 passing tests.


### Iteration 5 – Python File Input

**Requirement/Test**

The integrated analyzer should support analysis of Python source stored in a file.

A file-level entry point named `analyze_file(path)` is introduced.

The function should read the supplied Python file as text and pass its contents to the existing `analyze_source()` workflow.

This iteration tests a valid UTF-8 Python file containing one function.

Test:

`test_python_file_can_be_analyzed`

---

**Test Status Before Implementation**

RED – pytest could not collect the system-level tests because the new `analyze_file` entry point had not yet been implemented.

Error:

`ImportError: cannot import name 'analyze_file' from 'analyzer.core'`

Pytest reported:

`45 items / 1 error`

Collection of `tests/test_core.py` was interrupted at import time, so the existing core tests and the new file-input test were not collected.

This confirms that the file-input test and interface were introduced before the production implementation.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The project already provides:

analyze_source(source)

in analyzer.core.

A new pytest test now imports:

from analyzer.core import analyze_source, analyze_file

Current pytest result:

ImportError: cannot import name 'analyze_file' from 'analyzer.core'

The new function should support analysis of a valid Python source file.

Required behaviour:

1. analyze_file(path) receives a path to a Python source file.
2. It reads the file as UTF-8 text.
3. It passes the resulting source text to the existing analyze_source() function.
4. It returns the same structured analysis result produced by analyze_source().

For the current test, a file containing one function should produce:
- syntax_error = None
- metrics["functions"] = 1
- metrics["classes"] = 0

Requirements:
- Reuse analyze_source() rather than duplicating analysis logic.
- Use Python 3.
- Do not execute the supplied Python file.
- Implement only valid file reading in this iteration.
- Do not add missing-file, unsupported-extension, directory, or decoding error handling yet.

---

**AI Response Summary**

The AI proposed a minimal file-analysis entry point using `pathlib.Path`.

`analyze_file(path)` reads the supplied file as UTF-8 text and delegates all source analysis to the existing `analyze_source()` function.

No analysis logic is duplicated in the file-input layer.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed implementation directly satisfies the current valid-file test while preserving the existing integrated source-analysis workflow.

Delegating to `analyze_source()` avoids duplicating syntax validation or the five analysis algorithms.

File-related error handling is intentionally deferred to a later TDD iteration.

---

**Changes Made**

Modified `analyzer/core.py`.

The implementation now:
- imports `Path` from `pathlib`;
- provides `analyze_file(path)`;
- reads source files using UTF-8 encoding;
- delegates the file contents to `analyze_source()`.

No missing-file, unsupported-file-type, directory, or decoding error handling was added in this iteration.

---

**Test Status After Implementation**

GREEN – the valid Python file-input test passed after `analyze_file()` was implemented.

The complete regression test suite produced:

`56 passed in 0.14s`

The file-level entry point successfully read a UTF-8 Python source file and delegated its contents to the existing integrated source-analysis workflow.

All 55 previously passing tests continued to pass.

---

**Decision**

Accepted.

---

**Evidence**

- `33_core_red_file_input_missing.png`
- `34_core_green_file_input.png`

---

**Notes / Problems Identified**

The analyzer now supports both direct source-text analysis and Python file analysis.

The current `analyze_file()` implementation assumes that the supplied file exists and can be read as UTF-8 text.

File-related exceptional cases have not yet been handled.


### Iteration 6 – Missing File Error Handling

**Requirement/Test**

The file-level analyzer should handle a missing input file without allowing an uncaught `FileNotFoundError` to terminate the application.

A missing file is a file-input error rather than a Python syntax error.

The expected result therefore contains:

- a non-None `file_error`;
- `syntax_error` set to `None`.

Test:

`test_missing_file_reports_file_error`

---

**Test Status Before Further Implementation**

RED – the newly introduced missing-file test failed against the existing file-analysis implementation.

Test result:

`1 failed, 56 passed`

The failing test was:

`test_missing_file_reports_file_error`

The current `analyze_file()` implementation attempted to read the missing path directly and allowed the resulting `FileNotFoundError` to propagate.

The exception was therefore not converted into a structured analyzer result.

All 56 previously passing tests continued to pass.

---

**Evaluation**

The failure identifies a file-input error-handling defect.

The existing implementation correctly handles valid UTF-8 Python files, but assumes that the supplied path exists.

A missing file currently terminates the analysis through an uncaught `FileNotFoundError`.

This should be handled separately from Python syntax errors because no source code was successfully read or parsed.

---

**AI Prompt**

I am developing a Python Static Code Analyzer using Test-Driven Development.

The analyzer currently provides:

analyze_source(source)
analyze_file(path)

The current analyze_file implementation reads a UTF-8 file and delegates to analyze_source().

A new test has exposed the following defect:

FileNotFoundError is raised when the supplied path does not exist.

Current pytest result:

1 failed, 56 passed

Required behaviour:

1. A missing file must not cause an uncaught FileNotFoundError.
2. analyze_file(path) should return a dictionary containing:
   - file_error: a non-None error description
   - syntax_error: None
3. Valid existing files must continue to use analyze_source().
4. Preserve all currently passing tests.

Requirements:
- Catch FileNotFoundError at the file-input boundary.
- Do not classify a missing file as a Python syntax error.
- Do not modify the five individual analysis components.
- Implement only the missing-file case in this iteration.

---

**AI Response Summary**

The AI proposed handling `FileNotFoundError` directly at the file-input boundary.

`analyze_file()` now attempts to read the supplied path inside a `try` block.

If the file does not exist, the function returns a structured `file_error` result and sets `syntax_error` to `None`.

If reading succeeds, the source continues through the existing `analyze_source()` workflow.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed change directly addresses the failing test while preserving the existing separation between file-input errors and Python syntax errors.

The modification is localized to `analyze_file()` and does not alter the five analysis algorithms or the existing source-analysis workflow.

---

**Changes Made**

Modified `analyzer/core.py`.

The `analyze_file()` function now:
- catches `FileNotFoundError`;
- returns a structured `file_error` result for a missing file;
- distinguishes file errors from syntax errors;
- continues to delegate successfully read source to `analyze_source()`.

No other production code was modified.

---

**Regression Identified During Implementation**

After adding missing-file error handling, regression testing produced:

`1 failed, 56 passed`

The missing-file behaviour was handled, but the previously passing valid-file test failed:

`test_python_file_can_be_analyzed`

The failure was:

`TypeError: 'NoneType' object is not subscriptable`

This showed that `analyze_file()` returned `None` for an existing valid file instead of returning the result of `analyze_source()`.

The regression was caused by the control flow/indentation of the `return analyze_source(source)` statement after the new exception-handling logic was introduced.

This demonstrates why the complete regression suite was executed after the AI-assisted modification rather than testing only the newly added missing-file case.

---

**Decision**

Modify the implementation before acceptance.

---

**Changes Made**

Corrected `analyze_file()` so that:

- `FileNotFoundError` returns a structured file-error result;
- successful file reading continues outside the exception handler;
- successfully read source is returned through
  `analyze_source(source)`.

---

**Test Status After Implementation**

GREEN – after correcting the control flow in `analyze_file()`, the complete automated test suite passed.

Test result:

`57 passed in 0.13s`

The missing-file test passed and the previously regressed valid-file test also returned to GREEN.

All other existing tests continued to pass.

---

**Final Evaluation**

The first modification for missing-file handling introduced a regression: valid files returned `None` instead of the structured analysis result.

The complete regression suite detected this problem immediately.

After correcting the control flow, `analyze_file()` successfully handles both valid files and missing files while preserving the existing analysis behaviour.

This iteration demonstrates that AI-assisted changes still require independent evaluation and regression testing before acceptance.

---

**Final Decision**

Accepted after modification.

---

**Evidence**

- `35a_core_red_missing_file.png`
- `35b_core_red_missing_file_summary.png`
- `36_core_red_regression_after_file_error_fix.png`
- `37_core_green_missing_file_fix.png`

---

**Notes / Problems Identified**

No remaining defect was detected by the current test suite.

The complete project regression suite currently contains 57 passing automated tests.


### Iteration 7 – Invalid File Input Handling

**Requirement/Test**

Additional file-input tests were introduced based on the original requirements specification and test design.

The tests verify that:

- a file without the `.py` extension is rejected as an unsupported source-file type;
- a directory supplied instead of a Python source file is rejected with a controlled file-related error.

These tests correspond to T-FIL-03 and T-FIL-04 in the initial test design.

Tests:

`test_non_python_file_reports_unsupported_file_type`

`test_directory_path_reports_file_error`

No production-code changes were made before the new tests were executed.

---

**Test Status Before Further Implementation**

RED – both newly introduced invalid-file-input tests failed.

The complete automated test suite produced:

`2 failed, 57 passed`

The non-Python file test failed with:

`KeyError: 'file_error'`

This showed that `analyze_file()` did not reject a `.txt` file and instead returned a normal analysis result without a file-error field.

The directory-input test failed with an uncaught:

`PermissionError: [Errno 13] Permission denied`

This showed that `analyze_file()` attempted to call `read_text()` directly on a directory rather than validating that the supplied path represented a regular Python source file.

---

**Evaluation**

The existing implementation made an incorrect assumption that every supplied path could be treated directly as a readable Python source file.

It did not validate the `.py` extension before analysis and did not check whether the supplied path represented a regular file.

As a result, unsupported file types were accepted and directory input could cause an uncontrolled file-system exception.

These behaviours conflicted with the defined file-input requirements and demonstrated that the earlier implementation was incomplete.

---

**AI Prompt**

I asked the AI to improve the existing `analyze_file()` implementation while preserving the existing source-analysis behaviour.

The requested changes were:

- validate that the supplied path exists;
- validate that the path represents a regular file;
- reject files without the `.py` extension;
- return controlled file-related errors instead of allowing file-system exceptions to terminate analysis;
- preserve the existing `analyze_source()` workflow for valid Python files;
- avoid modifying the five individual analysis components.

---

**AI Response Summary**

The AI proposed adding path validation before reading the source file.

The revised implementation:

- converts the supplied path to a `Path` object;
- checks whether the path exists;
- checks whether the path represents a regular file;
- checks whether the file has a `.py` extension;
- catches file-reading and decoding errors;
- delegates successfully read Python source code to `analyze_source()`.

The intention was to keep file-input validation inside `analyze_file()` while leaving the existing static-analysis components unchanged.

---

**Initial Decision**

Modified and tested.

The proposed approach directly addressed the two newly failing tests and kept file-input validation separate from source-code analysis.

---

**Initial Changes Made**

`analyzer/core.py` was modified so that `analyze_file()` performed validation before reading the supplied path.

The implementation added:

- file-existence validation;
- regular-file validation;
- `.py` extension validation;
- controlled handling of file-reading and decoding errors.

No changes were made to the individual complexity, unused-variable, duplicate-code, naming, or metrics analyzers.

---

**Regression Identified During Implementation**

After adding path and file-type validation, regression testing produced:

`1 failed, 58 passed`

The two newly introduced invalid-input tests passed. However, the previously passing missing-file test failed:

`test_missing_file_reports_file_error`

The failure was:

`KeyError: 'syntax_error'`

The revised implementation correctly returned a `file_error` for a missing file but no longer included the previously established:

`"syntax_error": None`

field.

This represented a regression in the structured result contract rather than a failure of the new path-validation behaviour.

---

**Evaluation of Regression**

The new implementation successfully addressed the unsupported-file and directory-input defects, but it did not fully preserve the existing file-error result structure.

The complete regression suite detected this compatibility problem.

The file-error return structure therefore needed to be made consistent across missing files, directories, unsupported file types, and file-reading failures.

This demonstrated the importance of running the complete automated regression suite after an AI-assisted modification rather than testing only the newly introduced requirements.

---

**Decision After Regression**

Modified again before acceptance.

---

**Changes Made After Regression**

All file-level error results were standardized to contain:

- a non-None `file_error`;
- `syntax_error` set to `None`.

The valid-file path continued to delegate successfully read source code to `analyze_source()`.

The final file-level implementation therefore distinguished file-input errors from Python syntax errors while preserving the existing result contract.

---

**Test Status After Implementation**

GREEN – after standardizing the file-error result structure, the complete automated test suite passed.

Test result:

`59 passed in 0.20s`

The analyzer correctly rejected unsupported non-Python files and directory paths while preserving the previously implemented missing-file behaviour.

All previously passing tests also continued to pass.

---

**Final Evaluation**

The first path-validation modification solved the two newly identified invalid-input defects but introduced a regression in the existing missing-file result structure.

Regression testing detected this problem before the implementation was accepted.

After the result structure was standardized, the analyzer successfully handled:

- missing files;
- unsupported non-Python files;
- directory paths;
- valid Python source files.

No regression remained in the 59-test automated suite.

This iteration provides an example of why AI-generated or AI-assisted code must be independently evaluated and improved rather than accepted without verification.

---

**Final Decision**

Accepted after modification.

---

**Evidence**

- `38a_core_red_invalid_file_inputs.png`
- `38b_core_red_invalid_file_inputs_summary.png`
- `39_core_red_regression_missing_file_contract.png`
- `40_core_green_invalid_file_inputs.png`

---

**Notes / Problems Identified**

Two initial defects were identified:

1. unsupported non-Python files were not rejected;
2. directory input could cause an uncaught `PermissionError`.

A further regression was identified after the first modification:

3. the missing-file result no longer contained the expected `syntax_error` field.

All three issues were resolved.

T-FIL-03 and T-FIL-04 are now covered by automated tests.

The complete project regression suite currently contains:

`59 passed`


### Iteration 8 – File Decoding Error Handling

**Requirement/Test**

An additional invalid-file-input test was introduced to verify the analyzer's behaviour when a Python source file cannot be decoded using the expected UTF-8 encoding.

The test creates a `.py` file containing invalid UTF-8 byte sequences and passes the file to `analyze_file()`.

Expected behaviour:

- the analyzer must not terminate with an uncaught decoding exception;
- the result must contain a non-None `file_error`;
- `syntax_error` must remain `None`, because the failure occurs while reading the file rather than while parsing Python source code.

This test corresponds to T-FIL-05 in the initial test design.

Test:

`test_invalid_utf8_file_reports_file_error`

---

**Test Status Before Further Implementation**

GREEN – the newly introduced decoding-error test passed against the existing implementation.

The complete regression test suite produced:

`60 passed in 0.15s`

No additional production-code modification was required.

---

**Evaluation**

The existing `analyze_file()` implementation successfully handled a Python source file containing invalid UTF-8 byte sequences.

The decoding failure was converted into a controlled file-related error rather than being allowed to propagate as an uncaught exception.

The returned result also preserved the established structured error contract by providing a non-None `file_error` while keeping `syntax_error` set to `None`.

This confirms that the file-reading error handling introduced during the previous iteration also covers decoding failures.

---

**Decision**

Accepted without modification.

---

**Changes Made**

No changes were made to `analyzer/core.py`.

One additional automated test was added to `tests/test_core.py` to verify invalid UTF-8 file handling.

---

**Evidence**

- `41_core_decoding_error_test.png`

---

**Notes / Problems Identified**

No new defect was identified.

The existing file-input implementation already handled decoding errors correctly, so the new test increased boundary and invalid-input coverage without requiring further production-code changes.

The complete automated regression suite now contains 60 passing tests.



## Requirements Traceability and Regression Hardening

After completing the main implementation and reaching 60 passing automated tests, the original Software Requirements Specification and Test Design were reviewed again.

This review identified several cases that were explicitly defined in the original test plan but had not yet been directly verified by the implemented automated suite.

Additional tests are therefore being introduced as regression-hardening iterations rather than as new product features.

### Iteration 1 – Nested Function Complexity Isolation

**Requirement/Test**

During the final requirements-traceability review, an exceptional-case gap was identified in the cyclomatic-complexity test suite.

The existing tests verified that multiple sibling functions were analysed independently, but they did not verify whether a nested function's decision points could incorrectly affect the complexity of its enclosing function.

The following source was therefore introduced:

```python
def outer():
    def inner():
        if True:
            return 1

    return 0
```

Expected complexity:

`outer = 1`

`inner = 2`

The outer function contains no decision structures and should retain the base complexity of 1.

The nested inner function contains one `if` statement and should have complexity 2.

This test addresses the nested-function exceptional case defined in the initial Test Design.

Test:

`test_nested_functions_have_independent_complexity`

---

**Test Status Before Further Implementation**

RED – the newly introduced nested-function test exposed a previously undetected complexity-scope defect.

The complete automated test suite produced:

`1 failed, 60 passed`

The failing test was:

`test_nested_functions_have_independent_complexity`

Expected:

`outer = 1`

`inner = 2`

Actual:

`outer = 2`

`inner = 2`

The nested function itself received the expected complexity value, but the outer function incorrectly included the `if` statement belonging to the nested function.

---

**Evaluation**

The existing complexity implementation used `ast.walk()` when analysing each function.

Because `ast.walk()` recursively traverses all descendant nodes, analysing the outer function also entered the nested function definition.

The `if` statement inside `inner()` was therefore incorrectly counted as a decision point belonging to `outer()`.

The previous test `test_multiple_functions_have_independent_complexity` verified separate sibling functions but did not exercise nested lexical function structure.

The requirements-traceability review therefore identified both:

- a missing exceptional-case test;
- a real defect in the existing AI-assisted implementation.

This defect demonstrated that successful testing of sibling functions did not guarantee correct scope isolation for nested functions.

---

**AI Prompt**

The current cyclomatic-complexity implementation passes the existing automated tests but fails a newly introduced nested-function scope test.

Current pytest result:

`1 failed, 60 passed`

For the following source:

```python
def outer():
    def inner():
        if True:
            return 1

    return 0
```

Expected:

`outer = 1`

`inner = 2`

Actual:

`outer = 2`

`inner = 2`

The current implementation uses `ast.walk(function)` and therefore counts decision nodes inside nested functions as part of the enclosing function.

Modify the implementation so that:

- each function begins with a base complexity of 1;
- `if`, `elif`, `for`, `while`, and `except` continue to increase complexity according to the existing project rules;
- nested functions are analysed independently;
- decision points inside a nested function do not contribute to the complexity of the enclosing function;
- all existing automated tests continue to pass;
- the implementation continues to perform static analysis only;
- unrelated functionality is not rewritten.

---

**AI Response Summary**

The AI proposed replacing unrestricted recursive `ast.walk()` traversal inside each function with a controlled recursive traversal using `ast.iter_child_nodes()`.

A helper function was introduced to count decision structures belonging to the current function.

When the traversal encounters another `ast.FunctionDef` or `ast.AsyncFunctionDef`, traversal into that nested function stops.

Nested functions are still discovered independently by the outer AST walk, allowing each function to receive its own complexity result.

The existing decision types and base-complexity rule were preserved.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed modification directly addressed the scope defect identified by the failing regression-hardening test.

Stopping recursive traversal at nested function boundaries prevents decision structures from being attributed to the wrong function.

At the same time, nested functions remain independently discoverable and therefore retain their own complexity calculation.

The modification preserved the existing simplified complexity rules and did not introduce unrelated functionality.

---

**Changes Made**

Modified `analyzer/complexity.py`.

The unrestricted decision counting based on `ast.walk(function)` was replaced with a controlled recursive helper based on `ast.iter_child_nodes()`.

The helper:

- counts `ast.If`;
- counts `ast.For`;
- counts `ast.While`;
- counts `ast.ExceptHandler`;
- recursively processes ordinary child nodes;
- stops traversal when another function definition is encountered.

Each detected function still begins with a base complexity value of 1.

Nested functions continue to be analysed separately by the outer syntax tree traversal.

---

**Test Status After Implementation**

GREEN – after correcting nested-function scope handling, the complete automated regression suite passed.

Test result:

`61 passed in 0.13s`

The previously failing nested-function test now passed:

`outer = 1`

`inner = 2`

All 60 previously passing tests also continued to pass, demonstrating that the scope correction introduced no detected regression in the existing complexity, unused-variable, duplicate-code, naming, metrics, integration, file-input, or source-safety behaviour.

---

**Final Evaluation**

The requirements-traceability review successfully identified a behaviour that had not been covered by the earlier complexity tests.

Although the original implementation appeared correct for multiple independent functions, its use of unrestricted recursive AST traversal caused decision points from nested functions to be incorrectly included in the enclosing function's complexity.

The new test exposed this hidden defect.

Replacing unrestricted traversal with scope-aware traversal corrected the problem while preserving all previously verified complexity rules.

This iteration demonstrates the value of reviewing test coverage after the main implementation phase and retaining new tests as permanent regression checks.

---

**Final Decision**

Accepted after modification.

---

**Evidence**

- `42_complexity_red_nested_function_scope.png`
- `43_complexity_green_nested_function_scope_fix.png`

---

**Notes / Problems Identified**

One previously untested defect was identified and corrected:

- decision structures inside a nested function were incorrectly counted toward the enclosing function's cyclomatic complexity.

The complexity analyzer now treats nested functions independently for the tested scenario.

The complete project regression suite currently contains:

`61 passed`


### Iteration 2 – Unsupported Source Input Type

**Requirement/Test**

During the final requirements-traceability review, an invalid-input scenario defined in the Software Requirements Specification was found to be missing from the implemented automated test suite.

The source-analysis API should reject unsupported input types in a controlled manner rather than allowing an unexpected low-level exception to terminate the analyzer.

This iteration tests the behaviour of:

`analyze_source(None)`

Expected behaviour:

- the analyzer must not crash;
- a non-None `input_error` must be returned;
- `syntax_error` must remain `None`, because valid Python source text was never supplied for parsing.

Test:

`test_unsupported_source_type_reports_input_error`

No production-code changes were made before executing the new test.

---

**Test Status Before Further Implementation**

RED – the newly introduced unsupported-source-type test failed.

The complete automated test suite produced:

`1 failed, 61 passed`

The failing test was:

`test_unsupported_source_type_reports_input_error`

Calling:

`analyze_source(None)`

caused an uncaught:

`TypeError: compile() arg 1 must be a string, bytes or AST object`

The exception originated from `ast.parse(source)` before the analyzer could return a controlled result.

---

**Evaluation**

The existing `analyze_source()` implementation assumed that the supplied source value was suitable for direct AST parsing.

No explicit API-level type validation was performed before calling `ast.parse()`.

As a result, an unsupported input such as `None` caused a low-level `TypeError` to escape from the Python AST/compile machinery instead of being represented as a controlled analyzer result.

The requirements-traceability review therefore identified both:

- a missing invalid-input test;
- an incomplete input-validation behaviour in the integrated analyzer.

The appropriate correction was to validate the source value before AST parsing and return a structured `input_error`.

This error should remain distinct from `syntax_error`, because the problem is not invalid Python syntax. The problem is that the supplied API value is not supported as source text.

---

**AI Prompt**

The integrated Python Static Code Analyzer currently accepts source text through:

`analyze_source(source)`

A new requirements-traceability test has exposed an unsupported-input-type defect.

Current pytest result:

`1 failed, 61 passed`

The failing call is:

`analyze_source(None)`

Current behaviour:

an uncaught `TypeError` is raised by `ast.parse()` / `compile()`.

Expected behaviour:

- unsupported source input types must not crash the analyzer;
- the result should contain a non-None `input_error`;
- `syntax_error` should be `None`;
- valid string source behaviour must remain unchanged;
- existing syntax-error handling must remain unchanged;
- all existing tests must continue to pass.

Modify the integrated source-analysis entry point with the minimum change necessary.

Requirements:

- validate the source input before calling `ast.parse()`;
- accept Python source text as a string;
- reject unsupported source values such as `None`;
- return a structured input-error result;
- do not classify unsupported input types as syntax errors;
- do not modify the five individual analysis components;
- preserve the existing static-analysis workflow;
- do not execute supplied source code.

---

**AI Response Summary**

The AI proposed adding explicit input-type validation at the beginning of `analyze_source()`.

Before syntax parsing occurs, the function checks whether the supplied source value is a string.

If the value is not a string, the function immediately returns a structured result containing:

- a descriptive `input_error`;
- `syntax_error` set to `None`.

If the value is a string, the existing syntax-validation and integrated analysis workflow continues unchanged.

The modification was intentionally placed before `ast.parse()` so that unsupported API input is rejected at the analyzer boundary rather than being handled as a lower-level AST exception.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed modification directly addressed the failing invalid-input test.

Explicit validation at the API boundary is clearer than relying on `ast.parse()` to raise a `TypeError`, because the analyzer already knows that its source-analysis interface expects text input.

The change also preserves the distinction between:

- unsupported input type errors;
- Python syntax errors;
- file-input errors.

The five individual analysis components remain unchanged.

---

**Changes Made**

Modified `analyzer/core.py`.

A source-type validation check was added at the beginning of `analyze_source()`.

If `source` is not a string, the function now returns:

```python
{
    "input_error": "Source must be a string.",
    "syntax_error": None,
}
```

The existing syntax-validation and combined-analysis logic remains unchanged for valid string input.

No changes were made to the complexity, unused-variable, duplicate-code, naming, or metrics analyzers.

---

**Test Status After Implementation**

GREEN – after adding explicit source-type validation, the complete automated regression suite passed.

The complete test suite produced:

`62 passed in 0.13s`

The previously failing test:

`test_unsupported_source_type_reports_input_error`

now passed.

Calling:

`analyze_source(None)`

no longer allows a low-level `TypeError` to escape from `ast.parse()`.

Instead, the analyzer returns a controlled result containing a non-None `input_error` and `syntax_error` set to `None`.

All 61 previously passing tests also continued to pass.

This confirms that the new input validation introduced no detected regression in the existing complexity, unused-variable, duplicate-code, naming, metrics, integration, syntax-error, or file-input behaviour.

---

**Final Evaluation**

The requirements-traceability review successfully identified an invalid-input scenario that was not covered by the previously implemented test suite.

The earlier implementation delegated an unsupported value directly to `ast.parse()`. This exposed an implementation-level Python exception to the caller instead of providing a controlled analyzer result.

The failing test demonstrated that relying solely on the AST parser was insufficient for validating the public source-analysis interface.

Adding explicit validation at the beginning of `analyze_source()` created a clearer boundary between input validation and syntax validation.

Unsupported input types are now classified as input errors, while invalid Python source strings continue to be classified as syntax errors.

The full regression suite passing after the modification provides evidence that this change corrected the identified defect without disrupting the previously implemented analyzer behaviour.

This iteration also demonstrates the value of requirements-traceability review after the main implementation phase: a requirement that appeared conceptually simple still revealed an uncontrolled failure path when tested directly.

---

**Final Decision**

Accepted after modification.

The new automated test is retained permanently as a regression test.

---

**Evidence**

- `44a_core_red_unsupported_source_type.png`
- `44b_core_red_unsupported_source_type_summary.png`
- `45_core_green_unsupported_source_type_fix.png`

---

**Notes / Problems Identified**

One previously untested invalid-input defect was identified and corrected:

- supplying an unsupported source value such as `None` caused an uncaught `TypeError` from the Python AST/compile machinery.

The integrated source-analysis API now validates its input before syntax parsing and returns a controlled `input_error` for the tested unsupported input type.

The complete project regression suite currently contains:

`62 passed`

No additional defect was detected by the complete regression suite after the modification.


### Iteration 3 – Combined Analysis Result Verification

**Requirement/Test**

During the requirements-traceability review, the existing integration tests were found to verify only that the major result categories were present in the integrated result.

They did not directly verify that multiple analysis findings were returned correctly at the same time or that a clean program produced no false quality findings.

Two additional integration tests were therefore introduced.

The first test contains:

- one function naming violation;
- one unused local variable;
- one decision point producing complexity greater than one.

Expected behaviour:

- the function complexity is reported correctly;
- the unused variable is reported;
- the naming violation is reported;
- all findings remain available in their respective result categories.

The second test uses a small clean program.

Expected behaviour:

- syntax is valid;
- no unused-variable warnings are produced;
- no duplicate-code findings are produced;
- no naming violations are produced;
- valid complexity and metrics results are still returned.

These tests correspond to T-INT-01 and T-INT-02 in the initial Test Design.

Tests:

`test_multiple_issues_are_reported_together`

`test_clean_program_has_no_quality_findings`

No production-code changes were made before executing the new integration tests.

---

**Test Status Before Further Implementation**

GREEN – both newly introduced combined-analysis tests passed against the existing implementation.

The complete automated regression suite produced:

`64 passed in 0.22s`

No production-code modification was required.

---

**Evaluation**

The existing integrated `analyze_source()` implementation successfully combined results from the independently developed analysis components.

The multiple-issues test confirmed that complexity, unused-variable, and naming findings could all be reported from the same supplied source without one result category preventing or overwriting another.

The clean-program test confirmed that a valid program with no defined quality violations produced:

- no unused-variable warnings;
- no duplicate-code findings;
- no naming violations;

while still returning valid complexity and code-metrics information.

These results provide stronger integration evidence than the earlier test that verified only the presence of result-category keys.

The requirements-traceability review therefore identified an inadequacy in test coverage rather than a defect in the existing production implementation.

---

**Decision**

Accepted without modification.

---

**Justification**

The existing integrated implementation already satisfied the observable behaviour required by T-INT-01 and T-INT-02.

Both new tests passed without any production-code change.

Modifying the implementation when the required behaviour was already correct would have introduced unnecessary risk.

The new tests were retained because they provide permanent regression coverage for combined-analysis behaviour.

---

**Changes Made**

No changes were made to production code.

Two additional automated tests were added to `tests/test_core.py`:

- `test_multiple_issues_are_reported_together`;
- `test_clean_program_has_no_quality_findings`.

These tests strengthen system-level verification by checking actual analysis results rather than only checking that result categories exist.

---

**Test Status After Implementation**

GREEN – no additional implementation was required.

The complete automated regression suite remained:

`64 passed in 0.22s`

All previously implemented feature, integration, file-input, error handling, and source-safety behaviours continued to pass.

---

**Final Evaluation**

The traceability review showed that the earlier integration test was weaker than the behaviour described in the original Test Design.

The earlier test proved that the integrated result contained the expected categories, but did not prove that meaningful results from several analyzers could coexist correctly.

The two new tests closed this test-adequacy gap.

No production defect was discovered because the existing orchestration logic already preserved the independently generated analysis results.

This iteration demonstrates that requirements-traceability review can improve test quality even when the production implementation is already correct.

---

**Final Decision**

Accepted without modification.

The two new integration tests are retained permanently as regression tests.

---

**Evidence**

- `46_core_combined_analysis_verification.png`

---

**Notes / Problems Identified**

No production-code defect was identified.

A test-coverage weakness was identified and corrected:

- the previous integration test verified result-category presence but did not verify the correctness of combined findings.

T-INT-01 and T-INT-02 are now directly covered by automated tests.

The complete project regression suite currently contains:

`64 passed`


### Iteration 4 – Constant Naming Enforcement

**Requirement/Test**

During the requirements-traceability review, a gap was identified between the naming requirements and the implemented naming analyzer.

The Software Requirements Specification defines the following simplified constant naming rule:

- constants should use `UPPER_CASE`.

The specification provides:

`MAX_SIZE`

as a valid example and:

`maxSize`

as a naming violation.

The existing automated suite included a valid `MAX_SIZE` example.
However, evaluation showed that this test could pass even when module-level assignments were not analysed at all.

A new test was therefore introduced using:

```python
maxSize = 100
```

For the limited scope of this project, module-level assignments are treated as constant candidates and are checked against the `UPPER_CASE` rule.

Expected behaviour:

- the module-level identifier is analysed as a constant;
- `maxSize` is reported as violating `UPPER_CASE`;
- the reported identifier type is `constant`.

Test:

`test_invalid_module_level_constant_name_is_reported`

No production-code changes were made before executing the new test.

---

**Test Status Before Further Implementation**

RED – the new constant-naming test exposed missing functionality in the existing naming analyzer.

The complete automated regression suite produced:

`1 failed, 64 passed`

The failing test was:

`test_invalid_module_level_constant_name_is_reported`

Expected:

```python
{
    "name": "maxSize",
    "type": "constant",
    "rule": "UPPER_CASE",
}
```

to be present in the result.

Actual:

`[]`

The analyzer therefore produced no naming violation for the invalid module-level constant name.

---

**Evaluation**

The existing naming implementation analysed:

- function names;
- local-variable assignment names;
- class names.

It did not analyse module-level assignments.

Consequently, the earlier valid-constant test using `MAX_SIZE` was weaker than initially assumed. It passed because module-level assignments were ignored entirely, not because the analyzer had verified that `MAX_SIZE` satisfied an implemented constant-naming rule.

The requirements-traceability review therefore identified both:

- an inadequate earlier test for constant behaviour;
- missing constant-naming functionality in the production implementation.

The specification defines the required `UPPER_CASE` convention but does not provide a more advanced semantic mechanism for identifying Python constants.

For this educational analyzer, module-level assignments are therefore treated as constant candidates. This provides a simple, deterministic, and testable interpretation of the stated requirement.

---

**AI Prompt**

The current naming analyzer checks:

- functions using `snake_case`;
- local variables using `snake_case`;
- classes using `PascalCase`.

A requirements-traceability review has exposed missing constant-naming functionality.

Current pytest result:

`1 failed, 64 passed`

For the following module-level source:

```python
maxSize = 100
```

Expected result:

```python
{
    "name": "maxSize",
    "type": "constant",
    "rule": "UPPER_CASE",
}
```

The current implementation returns no violation.

Modify the existing naming analyzer so that module-level assignments are treated as constant candidates and checked using the simplified `UPPER_CASE` naming rule.

Requirements:

- preserve existing function naming behaviour;
- preserve existing local-variable naming behaviour;
- preserve existing class naming behaviour;
- accept valid constants such as `MAX_SIZE`;
- report invalid module-level constant names such as `maxSize`;
- return identifier type `constant`;
- return violated rule `UPPER_CASE`;
- use static AST analysis only;
- do not execute supplied source code;
- preserve all currently passing automated tests.

---

**AI Response Summary**

The AI proposed extending the existing AST-based naming analyzer with a module-level assignment pass.

A new `UPPER_CASE` validation helper was introduced.

Only assignments contained directly in the module AST body are treated as constant candidates. This prevents ordinary assignments inside functions from being reclassified as constants.

Module-level assignment targets are extracted and checked against the new constant-naming rule.

The existing function, local-variable, and class naming analysis remains in place.

---

**Decision**

Accepted for testing.

---

**Justification**

The proposed modification directly addressed the failing requirement while preserving the existing naming-analysis structure.

Restricting constant candidates to module-level assignments provides a simple and deterministic interpretation of the project's simplified constant requirement.

It also prevents function-local variables from being checked twice under both variable and constant naming rules.

---

**Changes Made**

Modified `analyzer/naming.py`.

The implementation now:

- retains the existing `snake_case` function rule;
- retains the existing `snake_case` local-variable rule;
- retains the existing `PascalCase` class rule;
- adds an `UPPER_CASE` validation rule;
- analyses module-level assignment targets as constant candidates;
- reports invalid constant names using identifier type `constant`;
- supports simple and unpacked module-level assignment targets.

No other analysis component was modified.

---

**Test Status After Implementation**

GREEN – after implementing module-level constant naming analysis, the complete automated regression suite passed.

The complete test suite produced:

`65 passed in 0.21s`

The previously failing test:

`test_invalid_module_level_constant_name_is_reported`

now passed.

The analyzer correctly reports:

```python
{
    "name": "maxSize",
    "type": "constant",
    "rule": "UPPER_CASE",
}
```

for the tested invalid module-level constant name.

The existing valid `MAX_SIZE` test also continued to pass.

All 64 previously passing tests remained GREEN, demonstrating that the new constant analysis introduced no detected regression in function, local-variable, class, integration, complexity, duplicate-code, metrics, file-input, or source-safety behaviour.

---

**Final Evaluation**

The requirements-traceability review identified an important weakness in the earlier constant-naming verification.

The original `MAX_SIZE` test passed even though the naming analyzer did not actually inspect module-level assignments. The absence of a warning therefore did not prove that constant naming behaviour had been implemented.

The new invalid example, `maxSize`, exposed this missing functionality.

Introducing explicit module-level constant analysis converted the previously implicit assumption into observable, testable behaviour.

The revised implementation now checks both sides of the simplified constant naming rule:

- valid `UPPER_CASE` identifiers can pass without a violation;
- invalid module-level constant names are reported.

This iteration demonstrates the value of evaluating not only whether a test passes, but whether the test actually proves the intended requirement.

---

**Final Decision**

Accepted after modification.

The new constant-naming test is retained permanently as a regression test.

---

**Evidence**

- `47_naming_red_constant_violation.png`
- `48_naming_green_constant_violation_fix.png`

---

**Notes / Problems Identified**

One production requirement gap and one test-adequacy weakness were identified and corrected:

- module-level constant naming was not previously implemented;
- the earlier valid-constant test could pass without proving that constant analysis existed.

The naming analyzer now directly verifies the tested `UPPER_CASE` constant convention.

The complete project regression suite currently contains:

`65 passed`


### Iteration 5 – Four-Line Duplicate Verification

**Requirement/Test**

During the requirements-traceability review, T-DUP-02 from the initial Test Design was identified as not having a directly corresponding automated test.

T-DUP-02 requires an identical four-line repeated code region to be detected as duplicate code.

A new test was therefore introduced using two identical four-line source regions.

Expected behaviour:

- duplicate code is detected;
- the repeated region produces at least one qualifying duplicate finding;
- the duplicate result retains source-location information.

The original Test Design requires duplicate detection for this scenario but does not require the analyzer to merge all matching lines into one maximal four-line clone.

The test therefore verifies observable duplicate detection without adding a stronger maximal-block requirement that is not defined by the specification.

Test:

`test_repeated_four_line_block_is_detected`

No production-code changes were made before executing the new test.

---

**Test Status Before Further Implementation**

GREEN – the newly introduced four-line duplicate test passed against the existing implementation.

The complete automated regression suite produced:

`66 passed in 0.15s`

No production-code modification was required.

---

**Evaluation**

The existing duplicate-code implementation successfully detected the repeated four-line source region.

The current detector uses a minimum duplicate-block size of three qualifying lines. Therefore, a repeated four-line region naturally contains qualifying repeated three-line windows and can be detected without introducing a separate four-line-specific algorithm.

The test confirmed that the repeated code produced a duplicate finding with source-location information.

The result also showed that the existing implementation already satisfied the observable behaviour required by T-DUP-02.

The test intentionally does not require the detector to merge all four matching lines into one maximal duplicate block because that stronger behaviour is not defined by the current project specification.

---

**Decision**

Accepted without modification.

---

**Justification**

The existing implementation already satisfied the four-line duplicate scenario required by the initial Test Design.

Changing the duplicate algorithm solely to produce a maximal four-line clone would introduce behaviour beyond the stated requirement.

The new automated test therefore provides direct regression coverage for T-DUP-02 while preserving the existing simplified duplicate-detection design.

---

**Changes Made**

No changes were made to `analyzer/duplicates.py`.

One additional automated test was added to `tests/test_duplicates.py`:

`test_repeated_four_line_block_is_detected`

The test verifies that an identical repeated four-line source region produces at least one qualifying duplicate finding with location information.

---

**Test Status After Implementation**

GREEN – no additional implementation was required.

The complete automated regression suite remained:

`66 passed in 0.15s`

All previously implemented complexity, unused-variable, duplicate-code, naming, metrics, integration, file-input, error-handling, and source-safety tests continued to pass.

---

**Final Evaluation**

The requirements-traceability review identified a direct test-coverage gap rather than a production-code defect.

Although the existing minimum-three-line duplicate algorithm was capable of detecting a repeated four-line region, the original automated suite did not contain a test explicitly corresponding to T-DUP-02.

The new test closed this traceability gap and confirmed that the current duplicate detector satisfies the required observable behaviour.

No unnecessary production modification was introduced.

This iteration demonstrates that requirements-traceability review can strengthen verification even when the existing implementation already supports the required case.

---

**Final Decision**

Accepted without modification.

The new four-line duplicate test is retained permanently as a regression test.

---

**Evidence**

- `49_duplicates_four_line_verification.png`

---

**Notes / Problems Identified**

No production-code defect was identified.

One requirements-to-test traceability gap was closed:

- T-DUP-02 now has a directly corresponding automated test.

The current duplicate-code implementation continues to use a minimum qualifying duplicate size of three lines.

Maximal clone merging remains outside the defined project requirements.

The complete project regression suite currently contains:

`66 passed`


### Iteration 6 – Remaining Boundary and Exceptional Cases

**Requirement/Test**

The requirements-traceability review identified several remaining boundary and exceptional cases that were explicitly described in the original Test Design or Software Requirements Specification but did not have direct automated coverage.

Four additional tests were introduced.

The first test verifies malformed nested Python syntax.

A nested `for` statement is deliberately malformed inside an `if` statement.

Expected behaviour:

- a syntax error is returned;
- the analyzer does not crash;
- syntax-dependent analysis does not continue.

This corresponds to T-SYN-09 in the initial Test Design.

The second test verifies an empty class:

```python
class Example:
    pass
```

Expected behaviour:

- the source is accepted as valid Python;
- the class count is 1;
- the valid PascalCase class name produces no naming violation.

This corresponds to T-EXC-03.

The third test verifies unused-variable analysis when a variable is used inside an expression.

Example:

```python
def calculate():
    value = 10
    return value + 5
```

Expected behaviour:

- `value` is recognised as referenced;
- no unused-variable warning is produced.

This corresponds to T-UNU-08.

The fourth test verifies that a long but syntactically valid snake_case identifier can be processed without a naming violation or analyzer failure.

This addresses the identifier-length boundary condition defined in the Software Requirements Specification.

Tests:

`test_malformed_nested_structure_reports_syntax_error`

`test_empty_class_is_counted_and_has_no_naming_violation`

`test_variable_used_inside_expression_is_not_reported`

`test_long_valid_identifier_is_processed_without_violation`

No production-code changes were made before executing the new tests.

---

**Test Status Before Further Implementation**

GREEN – all four newly introduced boundary and exceptional-case tests passed against the existing implementation.

The complete automated regression suite produced:

`70 passed in 0.18s`

No production-code modification was required.

---

**Evaluation**

The existing implementation successfully handled all four newly tested cases.

The malformed nested syntax was rejected in a controlled manner. The integrated analyzer returned a syntax error and did not continue into the syntax-dependent analysis components.

The empty class was processed correctly. The metrics component reported one class, while the valid PascalCase class name produced no naming violation.

The unused-variable analyzer correctly recognised a variable referenced inside an expression as used. No false unused-variable warning was generated.

The naming analyzer also processed a long but syntactically valid snake_case identifier without crashing or generating a false naming violation.

These results show that the requirements-traceability review identified missing test coverage rather than defects in the corresponding production implementation.

---

**Decision**

Accepted without modification.

---

**Justification**

All four required behaviours were already supported by the existing implementation.

Introducing production-code changes when the new tests were already passing would have added unnecessary implementation risk.

The new tests are retained because they provide direct regression coverage for previously unverified boundary and exceptional cases.

---

**Changes Made**

No production code was modified.

Four additional automated tests were added:

- two tests to `tests/test_core.py`;
- one test to `tests/test_unused_variables.py`;
- one test to `tests/test_naming.py`.

The new tests cover:

- malformed nested syntax;
- empty-class behaviour;
- variable use inside an expression;
- long valid identifier handling.

---

**Test Status After Implementation**

GREEN – no additional implementation was required.

The complete automated regression suite remained:

`70 passed in 0.18s`

All previously implemented complexity, unused-variable, duplicate-code, naming, metrics, integration, file-input, error-handling, source-safety, and requirements-hardening tests continued to pass.

---

**Final Evaluation**

The requirements-traceability review identified four behaviours that were present in the original testing or requirements documents but were not directly represented by the implemented automated test suite.

The new tests confirmed that the existing implementation already satisfied these behaviours.

No production defect was discovered.

This iteration therefore improved requirements-to-test traceability and regression confidence rather than changing product functionality.

The result also demonstrates that test-suite improvement does not always require implementation changes. New tests may instead provide evidence that previously implemented behaviour already satisfies the stated requirements.

---

**Final Decision**

Accepted without modification.

All four new tests are retained permanently as regression tests.

---

**Evidence**

- `50_boundary_exceptional_verification.png`

---

**Notes / Problems Identified**

No new production-code defect was identified.

The following traceability gaps were closed:

- T-SYN-09 – malformed nested syntax;
- T-EXC-03 – empty class;
- T-UNU-08 – variable used inside an expression;
- BC-07 – long valid identifier handling.

The complete project regression suite currently contains:

`70 passed`


### Iteration 7 – Multiple Findings Preservation

**Requirement/Test**

During the requirements-traceability review, the exceptional case T-EXC-05 was identified as requiring direct automated verification.

T-EXC-05 requires the analyzer to preserve unrelated findings when the same source code or identifier triggers more than one applicable analysis rule.

A new integrated test was therefore introduced using:

```python
def calculate():
    studentCount = 10
    return 5
```

The local variable `studentCount` triggers two independent findings:

- it is assigned but never referenced and should therefore be reported by unused-variable analysis;
- it violates the local-variable `snake_case` naming convention.

Expected behaviour:

- `studentCount` appears in the unused-variable result;
- a naming violation for `studentCount` is also returned;
- neither finding is silently lost;
- the source remains syntactically valid.

This test corresponds to T-EXC-05 in the initial Test Design.

Test:

`test_multiple_findings_for_same_identifier_are_preserved`

No production-code changes were made before executing the new test.

---

**Test Status Before Further Implementation**

GREEN – the newly introduced multiple-findings preservation test passed against the existing integrated implementation.

The complete automated regression suite produced:

`71 passed in 0.28s`

No production-code modification was required.

---

**Evaluation**

The integrated analyzer successfully preserved two independent findings associated with the same identifier.

The variable `studentCount` was correctly reported by the unused-variable analyzer because it was assigned but never referenced.

The same identifier was also reported by the naming analyzer because it violated the local-variable `snake_case` convention.

Both findings remained available in their respective result categories.

This confirms that one analysis category does not overwrite, suppress, or prevent an unrelated finding generated by another analysis category.

The test therefore provides direct evidence for the exceptional multiple-finding behaviour defined by T-EXC-05.

---

**Decision**

Accepted without modification.

---

**Justification**

The existing integrated analysis workflow already satisfied the required multiple-finding behaviour.

Because the new test passed without any production-code change, modifying the implementation would have introduced unnecessary risk.

The test is retained permanently because it verifies a high-value integration property that was not directly covered by the earlier test suite.

---

**Changes Made**

No production code was modified.

One additional automated integration test was added to `tests/test_core.py`:

`test_multiple_findings_for_same_identifier_are_preserved`

The test verifies that an identifier can simultaneously produce:

- an unused-variable finding;
- a naming-convention violation.

Both findings must remain present in their corresponding result categories.

---

**Test Status After Implementation**

GREEN – no additional implementation was required.

The complete automated regression suite remained:

`71 passed in 0.28s`

All previously implemented complexity, unused-variable, duplicate-code, naming, metrics, integration, file-input, error-handling, source-safety, and requirements-hardening tests continued to pass.

---

**Final Evaluation**

The requirements-traceability review identified that the existing integration suite did not directly verify the exceptional case in which the same identifier triggers multiple applicable analysis rules.

The new test closed this gap.

No production defect was discovered because the existing orchestration logic already preserves results from the separate analysis components.

The passing test demonstrates that the analyzer can retain multiple independent findings for the same source identifier without silently discarding one of them.

This iteration therefore strengthened regression confidence and requirements-to-test traceability without requiring implementation changes.

---

**Final Decision**

Accepted without modification.

The new multiple-findings test is retained permanently as a regression test.

---

**Evidence**

- `51_core_multiple_findings_preservation.png`

---

**Notes / Problems Identified**

No production-code defect was identified.

One exceptional-case traceability gap was closed:

- T-EXC-05 – multiple applicable findings for the same source line/identifier are preserved.

The complete project regression suite currently contains:

`71 passed`


### Iteration 8 – Large Input and Performance Verification

**Requirement/Test**

The final requirements-traceability review identified the large-input boundary and performance requirement as requiring direct automated verification.

The Software Requirements Specification defines BC-08: a valid Python source file approaching 1,000 lines should still be processed correctly.

NFR-03 also states that analysis of a Python source file containing up to 1,000 lines should normally complete within approximately two seconds on a standard development computer.

A 1,000-line Python source file was therefore generated for this test.

The generated source contains module-level assignments of the form:

```python
VALUE_0 = 0
VALUE_1 = 1
VALUE_2 = 2
```

continuing to 1,000 physical code lines.

The identifiers use the project's valid `UPPER_CASE` constant convention.

Expected behaviour:

- the file is read successfully;
- no file error is returned;
- no syntax error is returned;
- physical line count is 1,000;
- code line count is 1,000;
- function count is zero;
- class count is zero;
- analysis completes within the two-second performance target on the development computer used for testing.

The zero-function expectation also provides direct verification of BC-10, which requires a valid module-level-only Python file to be processed successfully with a function count of zero.

Test:

`test_large_python_file_is_processed_within_performance_target`

No production-code changes were made before executing the new test.

---

**Test Status Before Further Implementation**

GREEN – the newly introduced large-input and performance test passed against the existing implementation.

The complete automated regression suite produced:

`72 passed in 0.22s`

No production-code modification was required.

---

**Evaluation**

The integrated analyzer successfully processed a generated Python source file containing 1,000 physical code lines.

The file was read successfully and no file-related or syntax-related error was returned.

The metrics component correctly reported:

- `physical_lines = 1000`;
- `code_lines = 1000`;
- `functions = 0`;
- `classes = 0`.

The zero-function result also confirms that a valid source file containing only module-level statements can be analysed correctly without requiring any function definitions.

The test also measured the execution time of the single large-file analysis using `time.perf_counter()`.

The analysis completed within the defined two-second performance target on the development computer used for testing.

The overall pytest session also completed successfully with all 72 tests passing.

This provides direct evidence that the current implementation does not exhibit an obviously inefficient performance problem for the tested 1,000-line input size.

---

**Decision**

Accepted without modification.

---

**Justification**

The existing implementation already satisfied the large-input correctness and performance expectations defined by BC-08 and NFR-03.

The new test passed without any production-code change.

Modifying the implementation when both the functional and performance requirements were already satisfied would have introduced unnecessary risk.

The test is retained permanently because it provides regression coverage for both large-input processing and the defined performance target.

---

**Changes Made**

No production code was modified.

One additional automated test was added to `tests/test_core.py`:

`test_large_python_file_is_processed_within_performance_target`

The test generates a 1,000-line Python source file and verifies:

- successful file reading;
- successful syntax processing;
- correct physical-line count;
- correct code-line count;
- zero functions;
- zero classes;
- completion within the defined performance target.

The test uses `time.perf_counter()` to measure the execution time of the single `analyze_file()` call.

---

**Test Status After Implementation**

GREEN – no additional implementation was required.

The complete automated regression suite remained:

`72 passed in 0.22s`

All previously implemented complexity, unused-variable, duplicate-code, naming, metrics, integration, file-input, error-handling, source-safety, and requirements-hardening tests continued to pass.

---

**Final Evaluation**

The requirements-traceability review identified that the large-input and performance requirements had not previously been verified directly by the implemented automated suite.

The new test closed this gap by exercising the complete file-analysis pipeline with a 1,000-line valid Python source file.

The analyzer successfully completed all supported static analyses while maintaining correct metrics and remaining within the project's stated performance target on the development machine.

No production defect was discovered.

The result also demonstrates that the current modular implementation is capable of handling substantially larger input than the small examples used during the earlier TDD iterations.

Because the performance requirement is described as a normal development target rather than a strict real-time guarantee across all hardware, the test result should be interpreted as evidence for the tested development environment rather than as a universal timing guarantee.

---

**Final Decision**

Accepted without modification.

The large-input performance test is retained permanently as a regression test.

---

**Evidence**

- `52_large_input_performance_verification.png`

---

**Notes / Problems Identified**

No production-code defect was identified.

The following remaining traceability gaps were closed:

- BC-08 – valid Python source approaching 1,000 lines;
- BC-10 – module-level-only source with zero functions;
- NFR-03 – analysis completes within the expected performance target on the development computer used for testing.

The complete project regression suite currently contains:

`72 passed`

The main implementation and requirements-hardening phase is now complete.



## Final Regression Testing

After completion of the main AI-assisted TDD implementation and the requirements-traceability hardening phase, the complete automated test suite was executed again without any further production-code changes.

The purpose of this final regression run was to verify that all previously implemented, corrected, and hardened behaviours remained stable in the final project version.

The final automated suite includes tests covering:

- cyclomatic complexity;
- unused-variable detection;
- duplicate-code detection;
- naming-convention analysis;
- code metrics;
- syntax validation;
- combined analysis;
- source safety;
- Python file input;
- missing-file handling;
- unsupported file types;
- directory input;
- file decoding errors;
- unsupported source input types;
- empty and non-code input;
- malformed nested syntax;
- nested-function complexity isolation;
- multiple findings for the same identifier;
- four-line duplicate detection;
- long valid identifiers;
- empty classes;
- large-input behaviour;
- performance verification;
- regression tests for defects discovered during AI-assisted development.

---

**Final Regression Result**

GREEN – the complete automated regression suite passed.

Pytest collected:

`72 items`

Final result:

`72 passed in 0.20s`

No test failures, collection errors, or uncontrolled exceptions were reported.

---

**Evaluation**

The final regression run confirms that the complete project test suite remains stable after all implementation changes and requirements-hardening iterations.

Previously identified defects remained corrected, including:

- complexity from nested functions being incorrectly attributed to the enclosing function;
- unsupported source input causing an uncaught `TypeError`;
- missing constant-naming analysis;
- missing and invalid file-input handling defects;
- regressions in the file-analysis result structure.

The final regression result also confirms that later changes did not break previously verified behaviour in the five core analysis components or in the integrated source/file analysis workflow.

The result provides a final automated verification baseline for the project before coverage analysis, requirements traceability summarisation, evaluation of AI-assisted development, and final report preparation.

---

**Final Decision**

Accepted.

The current implementation and automated regression suite are treated as the final tested project baseline.

No additional production-code changes are required at this stage unless a new defect is identified during final review.

---

**Evidence**

- `53_final_regression_72_passed.png`

---

**Notes / Problems Identified**

No new defect was identified during the final regression run.

The final automated regression suite contains:

`72 passing tests`

The project is now ready to proceed to final coverage analysis and requirements-to-test traceability summarisation.



## Final Test Coverage Analysis

After the final regression suite passed, test coverage was measured for the production modules contained in the `analyzer` package.

Coverage was measured using:

`python -m pytest --cov=analyzer --cov-report=term-missing`

The purpose of this step was to determine how much of the final production implementation was exercised by the automated test suite and to identify any remaining unexecuted statements.

---

**Coverage Result**

The complete automated regression suite remained GREEN during coverage measurement.

Pytest collected:

`72 items`

Final test result:

`72 passed in 0.42s`

The coverage report produced the following results:

| Production Module | Statements | Missed | Coverage |
| --- | ---: | ---: | ---: |
| `analyzer/__init__.py` | 0 | 0 | 100% |
| `analyzer/complexity.py` | 18 | 0 | 100% |
| `analyzer/core.py` | 30 | 0 | 100% |
| `analyzer/duplicates.py` | 43 | 0 | 100% |
| `analyzer/metrics.py` | 23 | 0 | 100% |
| `analyzer/naming.py` | 42 | 4 | 90% |
| `analyzer/unused_variables.py` | 18 | 0 | 100% |

Overall production-code coverage:

`174 statements`

`4 statements missed`

`98% total coverage`

The coverage tool identified the remaining uncovered statements in `analyzer/naming.py` at:

`32-34, 52`

---

**Evaluation**

The final automated test suite achieved 98% statement coverage across the production `analyzer` package.

Five of the six functional production modules achieved 100% statement coverage:

- cyclomatic complexity;
- integrated source/file analysis;
- duplicate-code detection;
- code metrics;
- unused-variable detection.

The naming analyzer achieved 90% statement coverage, with four statements remaining unexecuted.

The uncovered statements are confined to alternative paths within the naming implementation rather than representing an observed failure of a defined project requirement.

The final requirements-traceability hardening process already introduced tests for the required naming behaviours, including:

- valid and invalid function names;
- valid and invalid local-variable names;
- valid and invalid class names;
- short valid identifiers;
- identifiers containing digits;
- long valid identifiers;
- valid `UPPER_CASE` constants;
- invalid module-level constant names;
- mixed identifier types.

Therefore, the remaining uncovered statements do not by themselves demonstrate that a required naming behaviour is missing.

---

**Coverage Interpretation**

The 98% coverage result provides strong evidence that the automated tests exercise the large majority of the production implementation.

However, statement coverage is not treated as proof that the software is defect-free.

A high coverage percentage only demonstrates that statements were executed during testing. It does not guarantee that every possible input, combination, branch, semantic condition, or interaction has been tested.

For this reason, coverage was evaluated together with:

- requirements-to-test traceability;
- normal-case tests;
- boundary tests;
- invalid-input tests;
- exceptional-case tests;
- regression tests;
- integration tests;
- source-safety testing;
- large-input and performance testing.

The combination of these verification approaches provides stronger evidence than coverage percentage alone.

---

**Decision**

Accepted.

No additional production-code modification was made solely to increase the coverage percentage from 98% to 100%.

The remaining four uncovered statements are recorded as residual test coverage rather than being hidden or artificially exercised solely to increase the reported percentage.

Adding tests only to obtain a perfect numerical coverage score would not necessarily improve verification of the defined project requirements and could introduce tests for behaviour outside the intended project scope.

The current coverage level is therefore accepted as the final project coverage baseline.

---

**Changes Made**

No production code was modified during coverage analysis.

No additional automated tests were added solely in response to the coverage percentage.

The existing 72-test regression suite was executed with coverage instrumentation using `pytest-cov`.

---

**Final Evaluation**

The final production implementation contains 174 executable statements, of which 170 were exercised by the automated suite.

This produced:

`98% statement coverage`

All production modules except `analyzer/naming.py` achieved 100% statement coverage.

The naming analyzer achieved 90%, with four statements not exercised by the final test suite.

The coverage result is considered strong for the defined coursework scope because it is supported by direct requirements-based testing and multiple categories of behavioural verification rather than relying on coverage percentage alone.

The result also demonstrates the effect of the requirements-traceability hardening phase. Tests added during that phase exercised behaviours that were not directly verified by the earlier implementation suite, including nested function isolation, unsupported source input, constant naming, four-line duplicate detection, exceptional cases, multiple findings, and large-input processing.

No new production defect was identified during coverage measurement.

---

**Final Decision**

The final test coverage is accepted.

Final coverage baseline:

`98%`

Final regression baseline:

`72 passed`

No further feature development or test expansion is required before the final evaluation and reporting stages.

---

**Evidence**

- `54_final_test_coverage.png`

---

**Notes / Problems Identified**

No new functional defect was identified.

A small residual coverage gap remains in:

`analyzer/naming.py`

Uncovered statements:

`32-34, 52`

This limitation will be retained in the final project evaluation rather than being concealed by unnecessary implementation or tests.

The final automated verification baseline is:

`72 passing tests`

`98% production statement coverage`



## Final Requirements-to-Test Traceability Summary

After completion of the implementation, requirements-hardening, regression testing, and coverage analysis, the final project was reviewed against the Software Requirements Specification and the initial Test Design.

The purpose of this review was to confirm that each defined functional requirement had corresponding automated verification and to identify any remaining implementation or documentation limitations.

The final automated baseline is:

`72 passing tests`

with:

`98% production statement coverage`

---

### Functional Requirements Traceability

| Requirement | Required Behaviour | Main Automated Verification | Final Status |
| --- | --- | --- | --- |
| FR-01 – Python Source Code Input | Accept Python source strings, `.py` files, empty source, and multi-line programs | `tests/test_core.py` source-input, empty-input, file-input, and large-file tests | PASS |
| FR-02 – Python Syntax Validation | Validate syntax before further analysis and return controlled syntax errors | Syntax-validation tests in `tests/test_core.py`, including malformed syntax, incomplete statements, indentation errors, and malformed nested structure | PASS |
| FR-03 – Cyclomatic Complexity | Base complexity 1 and count defined `if`, `elif`, `for`, `while`, and `except` decisions independently per function | `tests/test_complexity.py`, including simple, nested, multiple-function, and nested-function-scope tests | PASS |
| FR-04 – Unused Variable Detection | Report local variables assigned but not referenced; ignore intentionally unused `_` variables; preserve function scope | `tests/test_unused_variables.py`, including used, unused, reassigned, expression-use, loop, unpacking, and independent-function-scope tests | PASS |
| FR-05 – Duplicate Code Detection | Detect exact normalized duplicate blocks containing at least three qualifying lines and provide locations | `tests/test_duplicates.py`, including three-line, four-line, threshold, whitespace, comments, and repeated-occurrence cases | PASS |
| FR-06 – Naming Convention Analysis | Check functions, variables, classes, and constants using the simplified naming rules | `tests/test_naming.py`, including valid/invalid functions, variables, classes, constants, short names, digits, long identifiers, and mixed identifier types | PASS |
| FR-07 – Code Metrics | Report physical, blank, comment-only, and code lines plus function and class counts | `tests/test_metrics.py` and integrated metrics tests in `tests/test_core.py` | PASS |
| FR-08 – Combined Analysis | Run all supported analyses on the same valid source and preserve findings from different categories | Combined-analysis and multiple-findings tests in `tests/test_core.py` | PASS |
| FR-09 – Analysis Result | Return structured results that distinguish error and analysis categories | Integrated result, syntax-error, input-error, file-error, and combined-analysis tests in `tests/test_core.py` | PASS WITH DOCUMENTED LABEL DEVIATION |
| FR-10 – Source Safety | Analyse source statically without executing supplied Python code | `test_analyzed_source_is_not_executed` and the complete AST/text-based implementation | PASS |

---

### FR-09 Result-Format Note

The initial Test Design used the category label:

`naming_violations`

for integrated naming results.

The final implementation uses:

`naming`

as the integrated dictionary key.

The naming findings themselves remain structured and are clearly separated from complexity, unused-variable, duplicate-code, metrics, and error results.

The Software Requirements Specification requires a structured and consistent result that distinguishes the analysis categories but does not mandate a specific dictionary-key spelling.

This difference is therefore retained as a documented interface-label deviation rather than changing the completed and regression-tested interface solely for cosmetic consistency with the initial Test Design.

---

### Boundary Conditions Traceability

| Boundary Requirement | Final Verification | Status |
| --- | --- | --- |
| BC-01 – Empty Input | Empty-source integrated test | PASS |
| BC-02 – Whitespace-Only Input | Blank-only integrated test | PASS |
| BC-03 – Comment-Only File | Comment-only source and metrics tests | PASS |
| BC-04 – Single-Line Program | Metrics single-line test | PASS |
| BC-05 – Function With No Decisions | Base-complexity tests | PASS |
| BC-06 – Duplicate Threshold | Exactly three lines detected; two lines rejected | PASS |
| BC-07 – Identifier Length | Short and long valid identifier tests | PASS |
| BC-08 – Large Input | 1,000-line integrated file test | PASS |
| BC-09 – Nested Structures | Nested `if` and nested-loop complexity tests | PASS |
| BC-10 – File With No Functions | 1,000-line module-level-only test reports zero functions | PASS |

---

### Invalid Input Traceability

| Invalid Input Requirement | Final Verification | Status |
| --- | --- | --- |
| II-01 – Syntax Error | Controlled syntax-error tests | PASS |
| II-02 – Invalid Indentation | Invalid-indentation test | PASS |
| II-03 – Incomplete Statement | Incomplete assignment/function tests | PASS |
| II-04 – Non-Python File | Unsupported `.txt` file test | PASS |
| II-05 – Missing File | Missing-file controlled-error test | PASS |
| II-06 – Directory Instead of File | Directory-input controlled-error test | PASS |
| II-07 – Unreadable / Decoding Failure | Invalid UTF-8 file test | PASS |
| II-08 – Unsupported Input Type | `analyze_source(None)` controlled input-error test | PASS |

---

### Exceptional-Case Traceability

| Exceptional Case | Final Verification | Status |
| --- | --- | --- |
| T-EXC-01 – Nested Functions | Nested-function complexity isolation test | PASS |
| T-EXC-02 – Same Variable Name in Separate Functions | Function-scope unused-variable test | PASS |
| T-EXC-03 – Empty Class | Integrated empty-class metrics/naming test | PASS |
| T-EXC-04 – Deeply Nested Decisions | Nested decision and loop complexity tests | PASS |
| T-EXC-05 – Multiple Findings | Same identifier produces unused-variable and naming findings | PASS |

---

### File-Input Traceability

The final file-level interface is verified for:

- valid UTF-8 `.py` files;
- missing files;
- unsupported file extensions;
- directory paths;
- invalid UTF-8 source data;
- 1,000-line Python source files.

All tested file-input cases return controlled results without an uncontrolled application crash.

---

### Non-Functional Requirements Verification

**Correctness**

Correctness is supported by 72 automated tests covering normal, boundary, invalid, exceptional, integration, regression, and requirements-hardening scenarios.

**Reliability**

Invalid syntax, unsupported source types, missing files, directories, unsupported file types, and decoding failures are handled through controlled result structures rather than uncontrolled application termination.

**Performance**

A generated 1,000-line Python source file was analysed within the defined two-second development target.

The complete test suite remained GREEN during this verification.

**Maintainability**

The implementation separates the major analysis responsibilities into independent modules:

- `complexity.py`;
- `unused_variables.py`;
- `duplicates.py`;
- `naming.py`;
- `metrics.py`;
- `core.py`.

This modular structure allows individual analysis behaviours to be tested and modified independently.

**Source Safety**

The analyzer performs static AST/text analysis and automated testing confirmed that supplied Python source is not executed.

---

### Final Verification Evidence

The final regression run produced:

`72 passed in 0.20s`

The final coverage run produced:

`72 passed in 0.42s`

Production statement coverage was:

`98%`

Five functional production modules achieved 100% statement coverage.

`analyzer/naming.py` achieved 90% statement coverage, leaving four statements unexecuted.

This residual coverage gap is documented rather than hidden by tests added solely to obtain a perfect numerical score.

---

### Traceability Conclusion

The final review found automated verification for all ten functional requirements and for the defined boundary, invalid-input, exceptional, file-input, safety, and large-input scenarios.

Several gaps discovered during the requirements-hardening phase required additional tests, and some exposed real implementation defects.

The most significant improvements included:

- isolating nested-function cyclomatic complexity;
- adding controlled unsupported-source handling;
- implementing constant naming analysis;
- improving file-input validation and error handling;
- verifying combined and multiple findings;
- adding direct large-input and performance verification.

The final test suite therefore provides a substantially stronger verification baseline than the initial test design alone.

The remaining documented limitations are:

- 98% rather than 100% production statement coverage;
- four uncovered statements in `analyzer/naming.py`;
- the integrated result key `naming` differs from the initial Test Design label `naming_violations`;
- the simplified analyzer intentionally remains narrower than a professional static-analysis product.

The final implementation is accepted as satisfying the defined coursework scope.


