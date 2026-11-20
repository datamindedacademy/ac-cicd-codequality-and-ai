# 02 - Parametrize

**Words to use:** floating point, `pytest.approx`, tolerance, parametrized test, test case, test id, known value, round trip, regression test.

## Goal

Replace copied tests with one parametrized test, and check a conversion function against a table of known values.

## Why this matters

Engineering code is full of tables: units, limits, material properties. A parametrized test is that table, and every row is checked on every run. Adding a case is adding a line, not a function.

## Background

- Floats are not exact: `0.1 + 0.2 == 0.3` is `False`. Compare floats with **`pytest.approx`**: `assert result == pytest.approx(7.6)`. By default it accepts a relative difference of one in a million. Use `abs=1e-6` for values close to zero.
- **`@pytest.mark.parametrize`** runs one test function once per row of values:

```python
@pytest.mark.parametrize(
    ("pressure", "expected"),
    [
        (7.2, "OK"),
        (8.0, "WARNING"),
        (8.5, "ALARM"),
    ],
)
def test_classify(pressure, expected):
    assert classify(pressure) == expected
```

- Each row is a separate **test case** with its own result. `uv run pytest -v` shows them as `test_classify[7.2-OK]`. Give them readable names with `ids=["ok", "warning", "alarm"]`.
- Two `parametrize` decorators on one test run every combination of both lists.
- A **known value** is a result you can check outside your code: a handbook, a calculator, a datasheet. 100 degC is 212 degF.
- A **round trip** converts there and back and expects the start value.
- A **regression test** is a test you add when you fix a bug, so that the bug cannot come back unnoticed.

## Tasks

The code for this exercise is `src/bench/units.py`, the tests are in `tests/test_units.py`.

### Task 1: four tests become one

The four `test_to_bar_...` tests in `tests/test_units.py` were copied and pasted. Replace the three that pass a unit with one parametrized test, with readable ids. Keep the test for the default unit as it is.

Result: `uv run pytest -v tests/test_units.py` shows `test_to_bar[bar]`, `test_to_bar[psi]` and `test_to_bar[kPa]`, and all tests pass.

### Task 2: a table of known values

Write one parametrized test `test_convert_known_values` for `convert`, with at least six rows that cover all six units. Find the expected values outside the code: in a handbook, on a calculator, or with a well-known value (water boils at 100 degC, 212 degF, 373.15 K; -40 is the same in degC and degF).

At least one row fails. Read the failure and find the line in `units.py` that causes it. Fix the code and keep the row: it is now a regression test.

Result: all tests green, and the fix is a separate commit.

### Task 3: every pair of units

This one is much harder.

`UNITS` in `units.py` has six units in two families. Write tests that check, without typing the pairs by hand:

- a round trip for every pair of units of the same family, for at least four values, one of them negative,
- that every pair of units of different families raises `ValueError` with the message `Cannot convert ...`.

Build the lists of pairs from `UNITS` itself, so that a seventh unit is tested automatically. Count the test cases with `uv run pytest -q tests/test_units.py`.

Then put the bug from task 2 back for a moment. Do your round trip tests catch it? Explain why or why not, and undo the bug again.

## Open question

You took the expected values in task 2 from outside the code. Why is that important? What would have happened if you had run `convert` once and pasted its output into the test as the expected value?
