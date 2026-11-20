# 03 - Fixtures and files

**Words to use:** fixture, `tmp_path`, test isolation, `conftest.py`, test data, setup, teardown, `yield`.

## Goal

Test code that reads files, with small test files that the tests create themselves, and share that setup between tests with a fixture.

## Why this matters

Most of your scripts read files: logs, exports, measurement series. You cannot test them with the real files: those are large, change, and do not belong in Git. A test that writes its own tiny file is fast, readable, and runs the same on every laptop and in the pipeline.

## Background

- A **fixture** is a function that prepares something a test needs. A test asks for a fixture by naming it as a parameter. pytest calls the fixture first and passes its result in.
- pytest has built-in fixtures. **`tmp_path`** gives each test its own new, empty temporary folder as a `Path`. Nothing a test writes there can disturb another test: that is **test isolation**.

```python
def test_read_pressures(tmp_path):
    path = tmp_path / "run.csv"
    path.write_text("timestamp,pressure_bar\n09:00,7.1\n")
    pressures, skipped = read_pressures(path)
    assert pressures == [7.1]
```

- Your own fixture is a function with the decorator `@pytest.fixture`. A fixture can ask for other fixtures, such as `tmp_path`:

```python
@pytest.fixture
def sample_log(tmp_path):
    path = tmp_path / "run_01.csv"
    path.write_text("...")
    return path
```

- Fixtures in a file called **`conftest.py`** in the `tests` folder are available to every test file in that folder, without an import.
- With `yield` instead of `return`, the code after the `yield` runs after the test, also when it failed. That is **teardown**: closing a connection, removing a file outside `tmp_path`.

## Tasks

The code for this exercise is `src/bench/logs.py`. Read its docstrings first.

### Task 1: a test that writes its own file

Create `tests/test_logs.py`. Write a test for `read_pressures` that writes a CSV with two good rows into `tmp_path`, reads it, and checks both the pressures and the number of skipped rows. Then write a second test for a file in which every pressure is bad: one `ERR` and one empty.

Result: both tests green. Run them twice: nothing is left behind in the `bench-project` folder.

### Task 2: your own fixture

Write a fixture `sample_log` that writes a log with three good rows and two bad rows (`ERR` and empty) to `tmp_path`, and returns its path. Use it in a test that checks the pressures and that 2 rows were skipped. Then move the fixture to `tests/conftest.py` and check that the test still passes without importing it.

Result: `tests/conftest.py` holds the fixture, and `uv run pytest -v tests/test_logs.py` shows three green tests.

### Task 3: a whole folder

This one is much harder.

Test `summarize_folder` on a folder with your `sample_log`, a second log, and a file `notes.txt` with one line of text, as an operator might leave next to the logs. Check the complete result for one log, and which logs are in the result.

Your test finds a bug. Fix it in `logs.py`. Then add a test for an empty folder. Merge `add-tests` into `main` from the command line and push `main`.

Result: all tests green, and `main` on Azure DevOps has your tests and your three fixes.

## Open question

`read_pressures` reads from a file path. Suppose it read straight from the test bench over the network instead. How would you test it then, without a test bench next to your laptop? Look up "mock" or "fake" in the context of testing.
