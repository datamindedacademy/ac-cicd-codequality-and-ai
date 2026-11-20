# 02 - pre-commit

**Words to use:** Git hook, pre-commit, hook, stage, `.pre-commit-config.yaml`, local hook, `--no-verify`.

## Goal

Run ruff automatically on every commit with pre-commit, add ready-made hooks, and see where hooks stop.

## Why this matters

ruff only helps when somebody runs it. A Git hook runs it for you, on exactly the files you are about to commit, before the commit exists. You get the feedback in seconds on your laptop, instead of minutes later from the pipeline, or days later from a colleague.

## Background

- A **Git hook** is a script that Git runs at a moment in its work, such as just before a commit. When the script fails, Git stops.
- **pre-commit** is a tool that manages hooks for you. It is in the setup manual (`uv tool install pre-commit`). Check it with `pre-commit --version`.
- The hooks of a project are listed in **`.pre-commit-config.yaml`** in its root. It is committed, so the whole team has the same hooks.
- A **local hook** runs a command from the project itself. This one runs the ruff of `uv.lock`, the same version as `uv run ruff` and the pipeline:

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uv run ruff check --fix
        language: system
        types: [python]
```

- `pre-commit install` connects the hooks to Git, once per clone. From then on every `git commit` runs them on the staged files.
- When a hook changes a file, the commit stops. Look at the change with `git diff`, `git add` the file and commit again.
- `pre-commit run --all-files` runs the hooks on everything, without committing.
- `git commit --no-verify` skips the hooks. That is why the pipeline still runs the same checks this afternoon.

## Tasks

Continue in `bench-project`. Start a new branch from an up-to-date `main`:

```powershell
git switch main
git pull
git switch -c pre-commit
```

### Task 1: ruff at every commit

Create `.pre-commit-config.yaml` with two local hooks: one that runs `ruff check --fix` and one that runs `ruff format`. Install the hooks. Then add a badly formatted line to a Python file and try to commit it.

Result: the first commit attempt stops with `Failed` and `files were modified by this hook`. After `git add`, the second attempt succeeds, and the committed line is formatted.

### Task 2: ready-made hooks

Add three hooks from the repository `https://github.com/pre-commit/pre-commit-hooks` (version `v6.0.0`): one that refuses files larger than 500 KB, one that makes every file end with exactly one newline, and one that removes spaces at the end of lines. Run all hooks on all files once, and commit what they changed.

Then try to commit a CSV file of 1 MB, as if you were adding a measurement export to the repository by accident.

Result: the large file is refused and not committed. Remove it again.

If pre-commit cannot download the hooks (a proxy or Zscaler message), wait two minutes and try again. If it still fails, write down the message and skip this task.

### Task 3: the tests before every push

This one is much harder.

Running all tests at every commit is too slow for a large project, but before a push it is fine. Add a hook that runs the test suite, only when you push, not when you commit. Make sure that a plain `pre-commit install` sets up both, so a colleague needs no extra command, and that the ruff hooks do not run a second time on push.

Prove it: break a test, commit (it works), and push (it is refused). Repair the test. Then merge your branch into `main` from the command line and push `main`.

Result: `git push` with a failing test is refused by the hook, the repaired version is pushed, and `main` has your `.pre-commit-config.yaml`.

## Open question

Anybody can skip the hooks with `git commit --no-verify`, or simply never run `pre-commit install`. So why bother with hooks at all, if the pipeline checks the same things anyway? And the other way round: if the hooks run on every laptop, why do you still need the pipeline?
