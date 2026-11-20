# pytest exercises

Day 3, part 2: unit tests with pytest.

All exercises work on one small project: `bench`, helpers for the readings and logs of a (fictional) compressor test bench. You put it in your own repository on Azure DevOps this morning. Its tests run in a pipeline in the last part of the day.

By the end you can: write a unit test for an existing function, run the test suite, and read what a failing test tells you.

| # | Folder | Topic | Why it matters |
|---|---|---|---|
| 01 | `01-first-tests` | Test discovery, `assert`, red and green, boundaries, `pytest.raises` | A test is how you accept code, yours or not |
| 02 | `02-parametrize` | `pytest.approx`, `@pytest.mark.parametrize`, a table of known values | One test, many cases, no copy and paste |
| 03 | `03-fixtures-and-files` | `tmp_path`, your own fixture, `conftest.py` | Test code that reads files without real data |

## Before you start

You need your `bench-project` repository from the morning, with the ruff and pre-commit changes merged into `main`. If you did not get that far, follow "Before you start" in `exercises/code-quality/README.md` first, and copy `pyproject.toml` and `.pre-commit-config.yaml` from `solutions/bench-project/` of the course repository.

Start from an up-to-date `main` on a new branch for your tests. Commit after each task, and push at the end of each exercise:

```powershell
cd $HOME\bench-project
git switch main
git pull
git switch -c add-tests
```

Your pre-commit hooks run on every commit, so your test files get linted and formatted too.

## How an exercise works

- **Words to use**: the terms of that exercise. Use them with the trainer and with Copilot.
- **Tasks**: three per exercise. Each states the result to reach, not the code. The last one is much harder. Most people will not finish it in class.
- **No hints**: use the Background section, the slides, the [pytest documentation](https://docs.pytest.org) or Copilot.
- **Open question**: goes beyond today. Try it, or bring it to the trainer.

A reference solution is in `solutions/bench-project/` of the course repository. Try first, then look.

## How to run the tests

From the root of `bench-project`:

```powershell
uv run pytest                          # all tests
uv run pytest -v                       # one line per test
uv run pytest tests/test_readings.py   # one file
uv run pytest -k classify              # only tests with "classify" in the name
uv run pytest -x                       # stop at the first failure
uv run pytest --lf                     # only the tests that failed last time
```

In VS Code, the **Testing** view (the flask icon) runs the same tests with a click. The first time, choose **Configure Python Tests**, then **pytest**, then the folder `tests`.

## The one rule of today

When a test fails, find out who is wrong: the code or the test. The docstring of the function is the specification. Fix the code when the code is wrong. Never change a test only to make it green.

## Using Copilot

You may use GitHub Copilot. No task needs it.

- Write the first test of every task yourself. You need to know what you are testing before anyone writes it.
- Copilot is good at the next ten similar cases. Read every one: a generated test can check the bug instead of the specification.
- A test that never failed has not proved anything yet. Break the code on purpose once and watch the test turn red.
