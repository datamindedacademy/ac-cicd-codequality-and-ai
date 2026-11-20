# 01 - ruff

**Words to use:** linter, formatter, rule, rule code, finding, autofix, `pyproject.toml`, format on save.

## Goal

Lint and format the bench project with ruff, choose its rules in `pyproject.toml`, and let VS Code apply them on every save.

## Why this matters

A linter catches small mistakes before they run: an unused import, a name that is easy to misread, a pattern that is a known bug. A formatter makes all code look the same, so a review is about what the code does and not about spaces and quotes. Both read their rules from `pyproject.toml`, so everybody on the team, and the pipeline this afternoon, uses the same ones.

## Background

- **ruff** is a linter and a formatter in one, from the makers of uv. It is a dev dependency of the bench project, so `uv run ruff` uses the version in `uv.lock`.
- `uv run ruff check .` lints every Python file under the current folder. Each **finding** has a file, a line, a **rule code** and a message:

```text
src/bench/logs.py:3:8: F401 [*] `os` imported but unused
```

- `[*]` means ruff can fix it itself: `uv run ruff check . --fix`. Findings without `[*]` need a person.
- `uv run ruff rule F401` explains a rule: what it checks, why, and how to fix it.
- `uv run ruff format .` rewrites the layout of the code. `uv run ruff format --check .` only reports which files it would change. That is the version for a check.
- ruff has a set of default rules. In `pyproject.toml` you add rule groups by their letter prefix, and settings such as the line length:

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
extend-select = ["E"]   # the defaults, plus the pycodestyle errors
```

- The VS Code extension **Ruff** (`charliermarsh.ruff`, from the setup manual) shows findings as you type, and can fix and format on save. Settings for one project go in `.vscode/settings.json` in that project, so they are committed and shared.

## Tasks

Work in `bench-project`, on the branch `code-quality`.

### Task 1: lint and format

Run the linter and the format check, and read what they report: which rule codes, in which files. Then let ruff fix and format what it can, and check that the tests still pass. Look at what ruff changed with `git diff` before you commit.

Commit the result as two commits: one for the formatting, one for the lint fixes.

Result: both commands report no findings, `uv run pytest` still passes, and `git log --oneline` shows the two commits.

### Task 2: choose the rules

Add a `[tool.ruff]` section to `pyproject.toml`: a line length of 100, and on top of the defaults the rule groups `E` (pycodestyle errors) and `B` (flake8-bugbear, likely bugs). Run the linter again.

At least one new finding cannot be fixed automatically. Find out with `uv run ruff rule <code>` why the rule exists, and fix the code by hand. The new line length changes what the formatter wants too: run the format check again.

Result: `uv run ruff check .` and `uv run ruff format --check .` both pass with your settings, and the change to `pyproject.toml` is committed together with the changes it caused.

### Task 3: format on save, for the whole team

This one is much harder.

Make VS Code format a Python file with ruff and fix what ruff can fix, every time you save, in this project only. Put the settings in the project, not in your user settings, so a colleague who clones the repository gets the same behaviour.

Prove it: in one file, swap two import lines, add an unused import and break the indentation of a dictionary. Save, and check that it was all repaired. Then merge your branch into `main` from the command line, as in Git exercise 05, and push `main`.

Result: `.vscode/settings.json` is committed, saving repairs the file, and `main` on Azure DevOps has your changes.

## Open question

The formatter changed dozens of lines in task 1, without changing what the code does. Imagine a colleague did that in the same commit as a real bug fix. Why is that a problem for the reviewer, and for anyone who runs `git blame` later?
