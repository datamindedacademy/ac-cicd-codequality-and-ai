---
layout: section
---

# Unit tests with <span class="dm-accent">pytest</span>

<!--
Three rounds of a few slides and an exercise: first tests, parametrize, fixtures. Everything happens in the bench project that participants pushed to their own repository this morning.
-->

---
layout: default
label: 7 · pytest
---

# A test is a function that <span class="dm-accent">asserts</span>

<div class="split">
<div>

```python
# tests/test_readings.py
from bench.readings import classify


def test_classify_warning_boundary():
    # Arrange
    pressure = 8.0
    # Act
    level = classify(pressure)
    # Assert
    assert level == "WARNING"
```

</div>
<div>

- The file is called `test_*.py`
- The function is called `test_*`
- **Arrange**: prepare the input
- **Act**: call the function
- **Assert**: state what must be true

</div>
</div>

<p class="note">Run it with <code>uv run pytest</code>. pytest finds the tests by their names; you register nothing.</p>

<!--
This is the whole idea. A test is an ordinary Python function, and assert is an ordinary Python statement: if the expression is false, the test fails. Arrange-act-assert is a way to keep tests readable; for one-liners the three steps fit on one line: assert classify(8.0) == "WARNING". Some people call it given-when-then; it is the same thing. Point out the import: from bench.readings, the package in src. uv sync installed it into .venv, which is why the test can import it.
-->

---
layout: default
label: 7 · pytest
---

# pytest <span class="dm-accent">finds</span> the tests by their names

<div class="split">
<div>

```text
bench-project/
├── pyproject.toml
├── uv.lock
├── src/
│   └── bench/
│       ├── readings.py
│       └── units.py
└── tests/
    ├── test_readings.py
    └── test_units.py
```

</div>
<div>

```text
$ uv run pytest
=========== test session starts ===========
collected 9 items

tests/test_readings.py ...           [ 33%]
tests/test_units.py ......           [100%]

============ 9 passed in 0.03s ============
```

</div>
</div>

<p class="note">One dot per passing test, an <code>F</code> per failure. <code>-v</code> gives one line per test with its name.</p>

<!--
Code in src, tests in tests, one test file per module. pytest walks through the tests folder, collects every test_ function, runs them and prints one character per test. In VS Code the Testing view, the flask icon, shows the same tests as a tree with a play button per test; configure it once with pytest and the tests folder. Use whichever you like; the terminal is what the pipeline uses later.
-->

---
layout: default
label: 7 · pytest
---

# Read a failure from the <span class="dm-accent">bottom up</span>

```text
_______________________ test_classify_alarm_boundary ________________________

    def test_classify_alarm_boundary():
        assert classify(8.49) == "WARNING"
>       assert classify(8.5) == "ALARM"
E       AssertionError: assert 'WARNING' == 'ALARM'
E
E         - ALARM
E         + WARNING

tests/test_readings.py:22: AssertionError
========================= short test summary info ==========================
FAILED tests/test_readings.py::test_classify_alarm_boundary - AssertionError
====================== 1 failed, 8 passed in 0.04s =========================
```

<p class="note">Score, then which test, then the <code>></code> line, then the <code>E</code> lines: the code returned <code>'WARNING'</code>, the test expected <code>'ALARM'</code>.</p>

<!--
Do not spoil the bug of exercise 01 too much: this slide shows the output, not the cause in the code. The order to read is the same as for a traceback on day 1: last line first. The minus and plus lines are a small diff: minus is what the test expected, plus is what it got. Useful flags when many tests fail: -x stops at the first failure, --lf runs only the tests that failed last time, -k classify runs only tests with classify in the name.
-->

---
layout: default
label: 7 · pytest
---

# Red: is the <span class="dm-accent">code</span> wrong, or the <span class="dm-accent">test</span>?

<DmColumns class="mt-2">
<DmColumn header="The specification decides" tone="navy">

```python
def classify(pressure_bar, warning_bar=8.0,
             alarm_bar=8.5):
    """Return "OK", "WARNING" or "ALARM".

    A pressure at or above a limit counts as
    that level: 8.0 is a WARNING, 8.5 is an
    ALARM.
    """
```

</DmColumn>
<DmColumn header="Then" tone="violet" divider>

- The docstring, the datasheet or the colleague who asked for it says what is right
- Code wrong: fix the code, keep the test
- Test wrong: fix the test, and say why in the commit message
- Never change a test only to make it green

</DmColumn>
</DmColumns>

<!--
This is the most important habit of the afternoon. A red test is a question, not a verdict: one of the two is wrong. You only know which by looking outside both: the docstring, a datasheet, the person who asked for the code. In exercise 01 the docstring is the specification. In pipelines exercise 02 the datasheet changes, and then the test is the one to update. Changing a test until it is green, without asking which side is right, is the testing version of deleting the smoke detector because it beeps.
-->

---
layout: default
label: 7 · pytest
---

# Test the <span class="dm-accent">error</span> too

```python
import pytest

from bench.readings import parse_reading


def test_parse_reading_unknown_unit():
    with pytest.raises(ValueError, match="Unknown pressure unit: atm"):
        parse_reading("7.5 atm")
```

<v-clicks>

- The test passes when the code inside the `with` raises `ValueError`
- It fails when nothing is raised, or a different error
- `match` also checks the message, so a user knows what went wrong

</v-clicks>

<p class="ask"><b>Ask</b>Why would you write this test <b>before</b> you change <code>parse_reading</code>?</p>

<!--
Answer: to see it fail first. A test that never failed has proved nothing; it could be testing the wrong function, or have a typo that makes it always pass. Write the test, see it red, change the code, see it green. That is test-driven development, which participants met in day 1 exercise 05. Day 1 also covered what a ValueError is and how try/except works; pytest.raises is the test-side version of the same idea.
-->

---
layout: statement
---

# Exercise 01: <span class="dm-accent">First tests</span>

`exercises/pytest/01-first-tests`

<p class="words"><b>Words you can now use</b> unit test · assertion · test discovery · red · green · arrange-act-assert · boundary value · pytest.raises</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 25 minutes. Everybody starts from an up-to-date main of their bench-<name> repository from this morning, on a branch add-tests (see "Before you start" in exercises/pytest/README.md). Their pre-commit hooks now lint and format the test files too. Then task 1 and 2. Walk around during task 2 and ask people what the docstring of classify says before they look at the code. Task 3 is for the fast ones.
-->

---
layout: default
label: 7 · pytest
---

# Compare floats with <span class="dm-accent">pytest.approx</span>

<DmColumns class="mt-2">
<DmColumn header="Exact comparison fails" tone="plain">

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

</DmColumn>
<DmColumn header="approx compares with a tolerance" tone="violet" divider>

```python
def test_to_bar_from_psi():
    result = to_bar(14.5038, "psi")
    assert result == pytest.approx(1.0)

# near zero, give an absolute tolerance
assert x == pytest.approx(0.0, abs=1e-6)
```

</DmColumn>
</DmColumns>

<p class="note">Default tolerance: a relative difference of one in a million. That is a choice. For a sensor with 0.1 bar accuracy, you may want another.</p>

<!--
Floats are stored in binary, and 0.1 has no exact binary form, just as one third has no exact decimal form. MATLAB has the same issue; people from MATLAB may know eps. pytest.approx compares with a tolerance. Relative tolerance does not work near zero, because a relative difference of anything against zero is huge; that is why abs exists. Exercise 02 has an example where this matters.
-->

---
layout: default
label: 7 · pytest
---

# One test, many cases: <span class="dm-accent">parametrize</span>

```python
@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (7.5, "bar", "psi", 108.7785),
        (100, "degC", "degF", 212.0),
        (-40, "degC", "degF", -40.0),
        (0, "K", "degC", -273.15),
    ],
)
def test_convert_known_values(value, from_unit, to_unit, expected):
    assert convert(value, from_unit, to_unit) == pytest.approx(expected)
```

<p class="note">Four rows, four test cases, each with its own result: <code>test_convert_known_values[100-degC-degF-212.0]</code>. A new case is a new line.</p>

<!--
The decorator gives the names of the parameters, then a list of rows. pytest runs the function once per row. If one row fails, the others still run and report separately, unlike a loop inside one test that stops at the first failing value. The values in the table come from outside the code: a handbook, or values everyone knows such as boiling water. That is important, and it is the open question of exercise 02.
-->

---
layout: statement
---

# Exercise 02: <span class="dm-accent">Parametrize</span>

`exercises/pytest/02-parametrize`

<p class="words"><b>Words you can now use</b> pytest.approx · tolerance · parametrized test · test case · known value · round trip · regression test</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 20 minutes. Task 2 finds a bug in the degF conversion: the offset is rounded. People who only test a round trip will not find it, which is what task 3 makes them discover. If someone is stuck on where the bug is: ask which rows fail, and what those rows have in common.
-->

---
layout: default
label: 7 · pytest
---

# A test that needs a file gets a <span class="dm-accent">temporary folder</span>

```python
def test_read_pressures_skips_bad_rows(tmp_path):
    path = tmp_path / "run_01.csv"
    path.write_text(
        "timestamp,pressure_bar\n"
        "09:00,7.31\n"
        "09:01,ERR\n"
    )

    pressures, skipped = read_pressures(path)

    assert pressures == [7.31]
    assert skipped == 1
```

<p class="note"><code>tmp_path</code> is a <b>fixture</b>: name it as a parameter and pytest passes in a new, empty folder for this test only.</p>

<!--
The function under test reads a file. We do not test it with the real logs: they are large, they change, and they do not belong in Git. The test writes a tiny file with exactly the cases it wants to check, including the bad row. tmp_path is a fresh folder per test, so tests cannot disturb each other and nothing is left in the project. This is the boundary of a unit test: it touches the disk, but only a temporary folder, and it still runs in milliseconds.
-->

---
layout: default
label: 7 · pytest
---

# Write your own <span class="dm-accent">fixture</span> once, use it everywhere

<div class="split">
<div>

```python
# tests/conftest.py
import pytest


@pytest.fixture
def sample_log(tmp_path):
    path = tmp_path / "run_01.csv"
    path.write_text(SAMPLE_LOG)
    return path
```

</div>
<div>

```python
# tests/test_logs.py
def test_skips_bad_rows(sample_log):
    _, skipped = read_pressures(sample_log)
    assert skipped == 2


def test_summarize_folder(sample_log):
    result = summarize_folder(sample_log.parent)
    assert "run_01" in result
```

</div>
</div>

<v-clicks>

- A fixture can use other fixtures: `sample_log` asks for `tmp_path`
- Fixtures in `conftest.py` work in every test file of the folder, without an import
- `yield` instead of `return`: the code after it runs after the test, to clean up

</v-clicks>

<!--
A fixture is setup with a name. The test says what it needs by naming it, and pytest builds it. Do not overuse fixtures: if a plain helper function does the job, that is often clearer. Fixtures shine when several tests need the same prepared thing, or when there is cleanup to do. The yield form is the backup for questions: open a connection, yield it, close it after the test.
-->

---
layout: statement
---

# Exercise 03: <span class="dm-accent">Fixtures and files</span>

`exercises/pytest/03-fixtures-and-files`

<p class="words"><b>Words you can now use</b> fixture · tmp_path · test isolation · conftest.py · teardown · yield</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 25 minutes. Task 3 finds the third bug: summarize_folder reads every file, so notes.txt shows up as a log. Make sure everybody pushes add-tests and completes the pull request at the end, even with unfinished tasks: the pipeline part starts from main. Participants who are far behind can copy the tests from solutions/bench-project/tests.
-->
