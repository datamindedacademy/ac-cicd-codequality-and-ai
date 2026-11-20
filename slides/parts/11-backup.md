---
layout: section
title: Backup - Type checking and mocks
---

# Backup: type checking and <span class="dm-accent">mocks</span>

<!--
Backup slides for questions: ty, the type checker from the proposal that we left out of the day, and fakes and mocks, the open question of pytest exercise 03.
-->

---
layout: default
label: Backup · Type checking
---

# <span class="dm-accent">ty</span> checks the type hints you already write

<div class="split">
<div>

```python
def to_bar(value: float, unit: str = "bar") -> float:
    ...

reading = "7.5"
to_bar(reading, "psi")   # a str, not a float
```

```powershell
uv add --dev ty
uv run ty check
```

</div>
<div>

- Type hints were on day 1: Python itself ignores them
- A type checker reads them and reports calls that cannot work, without running the code
- The `astral-sh.ty` extension shows the same in VS Code, as you type
- Add it as one more job in the pipeline, next to ruff and pytest

</div>
</div>

<!--
ty is a type checker from the makers of uv and ruff. It finds the class of bug where a value of the wrong type travels through the program: here a string from a CSV file that was never converted to float. Python would only fail when this line runs, maybe deep inside a long script; ty reports it immediately. Read the diagnostic like a traceback: the file and line, then what was expected and what was found. Older projects use mypy or pyright for the same job.
-->

---
layout: default
label: Backup · Testing
---

# Replace what you cannot run in a test: <span class="dm-accent">fakes and mocks</span>

<DmColumns class="mt-2">
<DmColumn header="Fake: a simple working stand-in" tone="navy">

```python
class FakeBench:
    def __init__(self, pressures):
        self.pressures = pressures

    def read_pressure(self):
        return self.pressures.pop(0)

def test_alarm_after_three_readings():
    bench = FakeBench([7.1, 8.2, 8.6])
    assert watch(bench) == "ALARM"
```

</DmColumn>
<DmColumn header="Mock: records how it was called" tone="violet" divider>

```python
from unittest.mock import Mock

def test_alarm_sends_one_mail():
    mailer = Mock()
    raise_alarm(8.6, mailer)
    mailer.send.assert_called_once()
```

</DmColumn>
</DmColumns>

<p class="note">Pass the test bench, the database or the mail server in as a parameter. Then a test can pass in a stand-in.</p>

<!--
This answers the open question of pytest exercise 03. When code talks to a test bench, a database or a mail server, the unit test should not. A fake is a small working replacement with canned data. A mock records the calls it receives, so the test can check that the code did the right thing, such as sending exactly one mail. Both only work when the code receives its dependencies as a parameter instead of creating them itself, which is called dependency injection. Code that is easy to test this way is usually better structured too. watch and raise_alarm are illustrations, not functions in the bench project.
-->
