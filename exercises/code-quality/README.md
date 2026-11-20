# Code quality exercises

Day 3, end of the morning: a linter, a formatter, and checks that run before every commit.

From here on, all exercises work on one small project: `bench`, helpers for the readings and logs of a (fictional) compressor test bench. You put it in your own repository on Azure DevOps first. In the afternoon you test it with pytest, and Azure DevOps checks it on every pull request.

By the end you can: fix what a linter reports on your own code, choose its rules in `pyproject.toml`, and run the same checks at commit time.

| # | Folder | Topic | Why it matters |
|---|---|---|---|
| 01 | `01-ruff` | `ruff check`, `ruff format`, rules in `pyproject.toml`, format on save | Small mistakes and style debates leave the review |
| 02 | `02-pre-commit` | Git hooks with pre-commit: ruff at every commit | Feedback in seconds, before anyone else sees the code |

## Before you start: your own repository

The trainer created an empty repository for you on Azure DevOps, called `bench-<your-name>`. Put the bench project in it. In PowerShell, from the root of the course repository (`ac-cicd-codequality-and-ai`):

```powershell
Copy-Item -Recurse exercises\bench-project $HOME\bench-project
cd $HOME\bench-project
git init -b main
git add --all
git commit -m "Add the bench project"
git remote add origin https://dev.azure.com/<organisation>/<project>/_git/bench-<your-name>
git push -u origin main
uv sync
code .
```

You know every Git command here from this morning. Check on Azure DevOps (**Repos > Files**) that the project is there.

Then make a branch for this part:

```powershell
git switch -c code-quality
```

This morning you bring each branch into `main` from the command line, as in Git exercise 05: `git switch main`, `git merge <branch>`, `git push`. This afternoon `main` gets protected, and changes go through a pull request.

From here on, work in the VS Code window of `bench-project`. Keep the course repository open in a second window to read the exercises.

## How an exercise works

- **Words to use**: the terms of that exercise.
- **Tasks**: three per exercise. Each states the result to reach, not the commands. The last one is much harder. Most people will not finish it in class.
- **No hints**: use the Background section, the slides, the [ruff documentation](https://docs.astral.sh/ruff/), the [pre-commit documentation](https://pre-commit.com) or Copilot.
- **Open question**: goes beyond today. Try it, or bring it to the trainer.

A reference solution is in `solutions/bench-project/` of the course repository: `pyproject.toml`, `.pre-commit-config.yaml` and `.vscode/settings.json`. Try first, then look.

## Using Copilot

You may use GitHub Copilot. No task needs it.

- Ask it what a rule code such as `E741` means and why it exists. `uv run ruff rule E741` tells you too.
- Let ruff fix what it can fix safely. Fix the rest yourself: those are the findings where a person has to decide.
