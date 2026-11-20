# CI/CD, Code Quality and AI

[![Dataminded Academy](https://raw.githubusercontent.com/datamindedacademy/branding/main/assets/badge.svg)](https://github.com/datamindedacademy)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/datamindedacademy/ac-cicd-codequality-and-ai)

Course material for **day 3** of the Dataminded training *Python Programming and Data
Analysis* for Atlas Copco: Git on Azure DevOps, ruff and pre-commit, unit tests with pytest,
and branch policies with pipelines that check every pull request.

Day 3 assumes the Python fundamentals of day 1: functions, conditionals, loops and
imports, and a working setup with uv. You do not need day 2, and you do not need to know
Git yet. After this day you can:

- Clone a repository from Azure DevOps, commit on a branch, merge and push from the
  command line.
- Fix what a linter reports on your own code, and run the checks at commit time with pre-commit.
- Write a unit test for an existing function and run the test suite.
- Read a failing test and decide whether the code or the test is wrong.
- Get a change into `main` with a reviewed pull request, and protect `main` with branch
  policies: a reviewer, and a pipeline that runs ruff and pytest and blocks the merge when
  one fails.

You're free to use GitHub Copilot throughout. Make sure that you understand everything it
writes or proposes.

## What is in this repository

| Path | What it is |
| --- | --- |
| [`exercises/git/`](exercises/git/) | Git exercises, with a script that prepares a practice repository |
| [`exercises/bench-project/`](exercises/bench-project/) | The small Python project you clean up, test and check in a pipeline |
| [`exercises/code-quality/`](exercises/code-quality/) | ruff and pre-commit exercises on the bench project |
| [`exercises/pytest/`](exercises/pytest/) | pytest exercises on the bench project |
| [`exercises/pipelines/`](exercises/pipelines/) | Branch policy and Azure Pipelines exercises on the bench project |
| [`exercises/ai/`](exercises/ai/) | Optional: skills and prompts for Copilot |
| [`solutions/`](solutions/) | Reference solutions. Try the exercise first. |
| [`slides/`](slides/) | The slide deck |
| [`tests/`](tests/) | Tests for the course material itself |
| [`TRAINER.md`](TRAINER.md) | Timing and preparation, for the trainer |

## Getting started

You need the tools from the setup manual: Git for Windows, uv, and Visual Studio Code
with GitHub Copilot. Open **PowerShell** and run these commands one by one:

```powershell
cd $HOME\Documents
git clone https://github.com/datamindedacademy/ac-cicd-codequality-and-ai
cd ac-cicd-codequality-and-ai
uv sync
code .
```

In VS Code, accept the recommended extensions and select the interpreter in `.venv`
(`Ctrl+Shift+P`, then *Python: Select Interpreter*).

Start with [`exercises/git/`](exercises/git/) and [`exercises/code-quality/`](exercises/code-quality/)
in the morning. After lunch, continue with [`exercises/pytest/`](exercises/pytest/) and then
[`exercises/pipelines/`](exercises/pipelines/).

If your laptop setup does not work in time, use the Codespaces button at the top. It
opens the same tools in the browser, with PowerShell as the terminal.

## License

[MIT](LICENSE).
