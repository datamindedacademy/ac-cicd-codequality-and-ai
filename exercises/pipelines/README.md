# Pipeline exercises

Day 3, last part: protect `main` with branch policies, and let Azure DevOps check every pull request.

You continue in your own `bench-project` repository. This morning ruff and pre-commit checked your code on your laptop, you merged your branches yourself, and this afternoon you wrote tests. Now changes go through a pull request: Azure DevOps runs the same checks on it, and refuses the merge until they pass and a colleague approved.

By the end you can: get a change into `main` with a reviewed pull request, protect `main` with branch policies, add a pipeline as a required check, and show that a pull request with badly formatted code, a failing test, or no approval cannot be completed.

| # | Folder | Topic | Why it matters |
|---|---|---|---|
| 01 | `01-format-check-and-policies` | A pipeline that runs ruff, a reviewer policy and a build validation policy on `main`, your first pull request | Nothing reaches `main` without a check and a second pair of eyes |
| 02 | `02-tests-required` | The tests as a second required check | A red test blocks the merge, not only a format error |

## Before you start

You need your `bench-project` repository with your tests merged into `main`. If you did not get that far, merge what you have, or copy `solutions/bench-project/tests` from the course repository.

Sit next to a neighbour: in these exercises you approve each other's pull requests. Your neighbour can open your repository on Azure DevOps, in the same project.

Start every exercise from an up-to-date `main` on a new branch:

```powershell
cd $HOME\bench-project
git switch main
git pull
git switch -c add-pipeline
```

## How an exercise works

The same as this morning: **Words to use**, **Tasks** with a result to reach, and an **Open question**. In these two exercises the YAML is given: the point is the setup in Azure DevOps and proving that it holds. The last task is much harder and optional.

A reference pipeline is in `solutions/bench-project/azure-pipelines.yml` of the course repository.

## Using Copilot

You may use GitHub Copilot. Pipelines are a place where it often writes something that looks right and is not: an old task version, a GitHub Actions keyword such as `runs-on:` in an Azure file, or a `pr:` section that Azure Repos ignores. The run log is the judge, not the YAML.

## Cheat sheet

```yaml
trigger:                      # which pushes start a run
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest      # a fresh Microsoft-hosted machine for every run

jobs:
  - job: lint                 # jobs run in parallel, each on its own machine
    displayName: Lint and format
    steps:
      - script: uv run ruff check .   # a command, as in a terminal
        displayName: ruff check       # the name you see in the run
```

- Indentation is meaning in YAML. Use two spaces, never a tab.
- A step that fails stops its job. The run is red when one job is red.
- Branch policies live in **Repos > Branches**: the **...** menu of `main`, then **Branch policies**.
