# 01 - A format check and branch policies

**Words to use:** pull request, reviewer, approve, complete, branch policy, minimum number of reviewers, build validation, required check, pipeline, YAML, trigger, agent, job, step, run, status.

## Goal

Add a pipeline that runs ruff, protect `main` with a reviewer policy and a build validation policy, get your first pull request reviewed, and prove that nothing gets into `main` without a green check and an approval.

## Why this matters

This morning you merged into `main` yourself and pushed: nobody looked at the change first, and nothing stopped a broken one. Your repository has no rules yet: anyone can push anything to `main`. The pre-commit hooks help, but anyone can skip them. Branch policies are the rules the server enforces, for everyone, every time.

## Background

- A **pull request** asks to merge a branch into `main`, on the server instead of on your laptop. You create it in **Repos > Pull requests > New pull request**, with a title, a description of what and why, and a **reviewer**.
- The reviewer reads the **Files** tab, can comment on a line (hover over the line), and votes **Approve**, or **Wait for author** with a comment. A good review answers three questions: does it do what the description says, does it do anything else, and can I understand it?
- **Complete** does the merge on the server. Keep the merge type **Merge (no fast-forward)** and let Azure DevOps delete the branch. Then `git switch main` and `git pull` on your laptop.
- A **branch policy** is a rule on a branch in Azure Repos. As soon as `main` has a required policy, nobody can push to it directly: every change comes through a pull request.
- **Require a minimum number of reviewers**: the pull request needs approvals from other people. With **Allow requestors to approve their own changes** off, your own approval does not count.
- **Build validation**: the pull request runs a pipeline, and with **Required** it cannot be completed until that run is green. The run tests the result of the merge: your branch merged with the latest `main`.
- A **pipeline** is a list of commands that a machine, the **agent**, runs for you. It is described in `azure-pipelines.yml` in the repository, so it is versioned and reviewed like the code.
- This pipeline runs the same ruff checks as your pre-commit hooks, with the ruff version of `uv.lock`:

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

jobs:
  - job: lint
    displayName: Lint and format
    steps:
      - script: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "##vso[task.prependpath]$HOME/.local/bin"
        displayName: Install uv

      - script: uv sync --locked
        displayName: Install Python and the packages from uv.lock

      - script: uv run ruff check .
        displayName: ruff check

      - script: uv run ruff format --check .
        displayName: ruff format --check
```

- Line by line: `trigger` starts a run for every push to `main`. `pool` asks for a fresh Linux machine. The agent has no uv, so the first step installs it and puts it on the `PATH` for the next steps. `uv sync --locked` installs Python and exactly the packages of `uv.lock`, and stops when the lockfile is out of date. Then the two ruff checks: when one finds something, it returns an error and the job turns red.
- To create the pipeline in Azure DevOps: **Pipelines > New pipeline > Azure Repos Git**, your repository, **Existing Azure Pipelines YAML file**, then the branch and the file. **Run** starts the first run.

## Tasks

Work on the branch `add-pipeline`. See the README of this folder for how to start it.

### Task 1: the pipeline

Add `azure-pipelines.yml` from the Background to the root of `bench-project`, commit it, and push the branch. Create the pipeline in Azure DevOps from that file on your branch, and run it. Open the run and read the log of each step.

Result: a green run with the steps `Install uv`, `Install Python and the packages from uv.lock`, `ruff check` and `ruff format --check`. You can point at the step that ran each command.

### Task 2: protect main

Add two branch policies on `main` of your repository:

- a minimum of one reviewer, where your own approval does not count,
- build validation with your pipeline, triggered automatically, and required.

Then open your first pull request: from `add-pipeline` into `main`, with a title, a short description, and your neighbour as reviewer. Wait for the validation run and the approval, and complete it. Update `main` on your laptop afterwards.

In the meantime, review your neighbour's pull request: read the **Files** tab, leave at least one comment on a line, and approve.

Result: on the policy page of `main` both policies are listed, your pull request is completed with a green check and your neighbour's approval, and your neighbour's pull request has your comment and approval.

### Task 3: try to break the rules

Prove that the rules hold. Each attempt must be refused:

1. Change `README.md` on `main` on your laptop, commit, and push straight to `main`.
2. On a new branch, add a badly formatted line to a Python file. Skip your own pre-commit hook with `git commit --no-verify`, push, and open a pull request.
3. Repair the formatting on that branch and push again. Do not ask for a review yet, and try to complete the pull request.

For each attempt, write down what Azure DevOps showed. Then ask your neighbour for an approval and complete the pull request. Undo the commit on your local `main` from attempt 1.

Result: three refusals, each with a different reason, and one completed pull request.

### Task 4: a sneaky push after the approval

This one is much harder, and optional.

Your neighbour approves your pull request. Then you push one more commit to the same branch, with a change your neighbour never saw. Can you still complete the pull request? Find the setting of the reviewer policy that closes this gap, turn it on, and prove the difference with a second pull request.

Result: the same sneaky push, once accepted and once blocked until a new approval.

## Open question

The validation run checks the merge of your branch with `main` at the moment the pull request was updated. A colleague completes another pull request ten minutes later. Is your green run still valid? Look up the **Build expiration** setting of the build validation policy, and say which value you would choose and why.
