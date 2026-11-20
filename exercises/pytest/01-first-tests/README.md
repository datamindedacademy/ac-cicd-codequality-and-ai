# 01 - First tests

**Words to use:** unit test, test function, assertion, test discovery, red, green, arrange-act-assert, boundary value, specification, `pytest.raises`.

## Goal

Run an existing test suite, write tests for a function from its docstring, and let a test find a bug.

## Why this matters

You already test your code: you run it and look at the output. A unit test does that look for you, every time, in a fraction of a second. It also tells a colleague, and Copilot, what "correct" means.

## Background

- A **unit test** calls one function with a known input and checks the result. It runs in memory, fast, and gives the same result every time.
- pytest **discovers** tests by name: files called `test_*.py`, and in them functions called `test_*`. You do not register them anywhere.
- An **assertion** is a statement that must be true: `assert classify(7.2) == "OK"`. When it is false, the test fails. pytest shows both sides of the comparison.
- **Red** is a failing test, **green** a passing one.
- Write each test in three steps, **arrange-act-assert**: prepare the input, call the function, check the result. For short tests the three steps fit on one line.
- **Boundary values** are where bugs live. If 8.0 is the limit, test 7.99 and 8.0, not 5 and 12.
- `pytest.raises` checks that code raises an error. The test fails when it does not:

```python
import pytest

def test_to_bar_unknown_unit():
    with pytest.raises(ValueError):
        to_bar(7.5, "atm")
```

- Add `match="..."` to `pytest.raises` to check the error message too.

## How to read a failed test

```text
>       assert parse_reading("7.5 bar") == (7.5, "bar")
E       AssertionError: assert (0.0, '') == (7.5, 'bar')
E         At index 0 diff: 0.0 != 7.5

tests/test_readings.py:7: AssertionError
========================= 1 failed, 6 passed in 0.03s ==========================
```

The `>` line is the failing assertion. The `E` lines give what the code returned versus what the test expected. The last line is the score. Read from the bottom up.

## Tasks

The code for this exercise is `src/bench/readings.py` in your `bench-project`.

### Task 1: red and green

Run the test suite of the project. Then make one of the tests in `tests/test_units.py` fail on purpose by changing an expected value, and read the failure: which line, which values. Undo the change.

Result:

```text
6 passed in 0.02s
```

### Task 2: test a function from its docstring

Create `tests/test_readings.py`. Write tests for `parse_reading` and `classify`, based only on their docstrings, not on the code:

- `parse_reading`: a normal reading, extra spaces, a decimal comma.
- `classify`: at least one value per level, and both boundaries tested from both sides. Also one call that changes a limit with a keyword argument.

One of your tests finds a bug. Decide whether the code or the test is wrong, and fix that. Commit the tests and the fix as two separate commits.

Result: all tests green, and `git log --oneline` shows the two commits.

### Task 3: bad input

This one is much harder.

The docstring of `parse_reading` says that a unit outside `PRESSURE_UNITS` raises `ValueError`. Write the test first, with `pytest.raises` and `match`, so that the message must name the unit:

```text
ValueError: Unknown pressure unit: atm
```

See it fail. Then change `parse_reading` until it passes. Add two more tests for bad input: a value that is not a number, and a reading without a unit. Find out which error Python raises for each without your help, and whether that is good enough.

Result: all tests green, and `uv run pytest -v -k parse` lists at least six tests.

## Open question

Your tests for `classify` pass now. Does that prove `classify` is correct? Think of a bug that all your tests would let through. What does that say about how many tests are enough?
