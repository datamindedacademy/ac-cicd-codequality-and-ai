# Training repository

Shared repository for the Git exercises of the Python Programming and Data Analysis training (day 3), hosted in Azure Repos.

## Rules

1. Never work on `main`. Make a branch: `feature/<your-name>-<topic>`.
2. Only add or change files in your own folder: `participants/<your-name>/`.
3. Get your change into `main` on the command line: update `main` with `git pull`, merge your branch, push. If the push is refused, `git pull` and push again. Never force push. Delete your branch afterwards, on your laptop and on the remote.

## Contents

| Path | What it is |
|---|---|
| `participants/` | One folder per participant. Create yours with your first name in lowercase. |
| `check_setup.py` | Small script to check that Python runs. Try: `uv run python check_setup.py` |
| `.gitignore` | Files that Git ignores (virtual environments, Python caches). |
