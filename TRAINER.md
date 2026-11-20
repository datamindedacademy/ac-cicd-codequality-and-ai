# Trainer guide: day 3

How the day runs, what to prepare in Azure DevOps, and what can go wrong. The Git block has its own guide: [`exercises/git/TRAINER.md`](exercises/git/TRAINER.md).

## The group

From the trainer of day 1:

- About 10 people, mostly wanting a Python refresher or coming from MATLAB. Two had no programming experience at all and set the pace. New people join on day 3 with a bit more experience, but still beginners.
- Day 1 ran slower than planned and **did not reach Git**. That is why day 3 opens with it.
- Copilot was allowed, but many turned the suggestions off: "we do not understand what it proposes". Keep AI as a short, concrete block at the end.
- Some used notebooks for the exercises. That is fine for exploring, but today's code must live in `.py` files: pytest, ruff and the pipeline work on modules.
- Windows workstations behind Zscaler. The tools installed smoothly with the setup manual. The Zscaler "checking this file" message appears on first downloads and usually clears within two minutes.
- By 16:30 they were exhausted. Plan the hardest thing before 15:30.

## Practical

- Start 09:00, lunch 12:00, end around 16:30. On site: report at reception, Jimmy or Jörgen picks you up.
- Participants were asked to apply the setup manual beforehand. Two people did not on day 1: it took them about 30 minutes. Pair them with a neighbour for the first Git exercise while they finish.

## Timing

| Time | Block | Material |
|---|---|---|
| 09:00 | Welcome, setup check, clone the course repo, Azure DevOps sign-in in the browser | slides part 00 |
| 09:15 | Git on Azure DevOps, break around 10:10 | slides parts 01 to 04, `exercises/git`, see its TRAINER.md |
| 11:15 | Push the bench project to `bench-<name>` together on screen, then ruff and pre-commit | slides part 05, `exercises/code-quality` |
| 12:00 | Lunch | |
| 12:45 | Why test, then pytest exercises 01 to 03 | slides parts 06, 07, `exercises/pytest` |
| 14:30 | Break | |
| 14:45 | Pull requests, branch policies and pipelines: exercises 01 and 02 | slides part 08, `exercises/pipelines` |
| 16:15 | Wrap-up | slides part 09 |
| | Backup if there is time: skills, context and prompting; ty and mocks | slides parts 10, 11, `exercises/ai` |

The morning is tight: the code-quality block has 45 minutes for the bench project setup and two exercises. Pre-commit exercise 02 may finish right after lunch. Make sure everybody has the bench project in their repository before lunch: everything in the afternoon builds on it.

**If the day runs late**, in this order:

1. Skip the last, harder task of every exercise. Nothing later depends on one.
2. Do pre-commit task 2 (hooks from GitHub) as a demo only.
3. Make pytest exercise 03 a demo, and let people copy `solutions/bench-project/tests` into their repository before the pipeline part.
4. Never drop pipelines exercises 01 and 02: a reviewed pull request, branch policies, a required pipeline, and a pull request that cannot be completed are the end goal of the day.

The AI part is backup: slides part 10 and `exercises/ai` are for when the group is ahead, or as material to take home.

## Prepare Azure DevOps

Do this together with the Git block preparation in `exercises/git/TRAINER.md`, which covers the organisation, guest access for Atlas Copco accounts, the access level, and the shared training repository per group.

### Parallel jobs: request them early

A new Azure DevOps organisation has **no free Microsoft-hosted pipeline capacity** until it is granted. Request the free grant through Microsoft's parallelism request form (linked from **Organization settings > Parallel jobs**). It takes a few business days.

The free grant runs **one job at a time**. With ten participants pushing at once, each run waits for all the runs before it, and every run takes a minute or more. Options:

- Buy a few Microsoft-hosted parallel jobs for the month of the training (Organization settings > Billing). Three to five keeps the waiting acceptable.
- Or register a self-hosted agent pool on a machine you control. More setup, and the exercises say `vmImage`, so you would change the `pool:` lines.

Check the current terms and prices on the Microsoft pricing page when you request: they changed before.

### Personal repositories, from the end of the morning

The shared training repository of the Git block keeps **no branch policy** all day: in the morning participants push to its `main` directly. Pull requests and branch policies happen in the afternoon, on each participant's own `bench-<name>` repository.

1. In the training project, create one **empty** repository per participant: `bench-<first-name>`, lowercase. Leave README and `.gitignore` off: participants push the bench project into it as their first step.
2. Participants are Contributors (see the Git guide), so they can open and review each other's repositories: in the pipeline exercises neighbours approve each other's pull requests. On their own `bench-<name>` repository, give each participant the **Edit policies** permission, so they can add the branch policies in pipelines exercise 01 (Project settings > Repositories > the repository > Security). Do not give them **Bypass policies when pushing** or **when completing pull requests**, or task 3 of that exercise will not be refused.
3. Check that Contributors can create pipelines in the project (Project settings > Pipelines settings, and the Security of **Pipelines > All pipelines**).
4. With two participant-level accounts, do the afternoon once end to end: push the bench project, create the pipeline from the YAML in pipelines exercise 01, add the reviewer and build validation policies, open a pull request with a formatting error and one with a failing test, and see **Complete** blocked until the run is green and the other account approved.

The script below creates the repositories with the Azure CLI and its `azure-devops` extension. Run it in PowerShell after `az login` and `az devops configure --defaults organization=https://dev.azure.com/<organisation> project=<project>`:

```powershell
$names = "anna", "bert", "chris"
foreach ($name in $names) { az repos create --name "bench-$name" --output none }
az repos list --query "[].name" --output tsv
```

### Your own demo repository

Prepare `bench-trainer` with the full solution (`solutions/bench-project`) and the pipeline from `solutions/bench-project/azure-pipelines.yml`, with the reviewer and build validation policies on `main`. You use it for the demos in slides part 08. Ask a colleague account to be the reviewer, or keep a second browser profile signed in as a test participant.

If you show the AI backup, try the example skill (`exercises/ai/example-skill`) once beforehand in your VS Code version: agent skills may need to be switched on in the settings, and agent mode output differs between runs.

## The bench project

`exercises/bench-project` is the starting point that every participant pushes to their own repository at the end of the morning. It was "written by a colleague in a hurry": it runs and its six tests pass, but ruff has findings and the code has four real bugs.

For the morning (ruff exercise 01):

| Task | What ruff finds | Fixed by |
|---|---|---|
| 1 | an unused `import os` and unsorted imports in `logs.py`; `typing.List`, `Dict`, `Tuple` in `readings.py` | `ruff check --fix` |
| 1 | single quotes, odd spacing and cramped operators in `units.py` | `ruff format` |
| 2 | after adding the `E` rules: a variable called `l` in `summarize` (E741) | the participant, by hand |
| 2 | after setting `line-length = 100`: the formatter re-joins the `classify` signature | `ruff format` |

The exercise version of `pyproject.toml` has no `[tool.ruff]` section on purpose: choosing the rules is task 2. Exactly which rules are on by default depends on the ruff version; the exercise texts do not depend on it.

For the afternoon (pytest exercises):

| Exercise | Bug | Found by |
|---|---|---|
| pytest 01, task 2 | `classify` uses `>` instead of `>=` for the alarm limit, so 8.5 bar is a WARNING | a boundary test from the docstring |
| pytest 01, task 3 | `parse_reading` accepts any unit, the docstring says only bar, psi and kPa | writing the test before the code |
| pytest 02, task 2 | the degF offset is `255.37`, a rounded value of 273.15 - 32 × 5/9 | a known value such as 212 degF = 100 degC |
| pytest 03, task 3 | `summarize_folder` reads every file, so `notes.txt` shows up as a log | a test with a non-CSV file in `tmp_path` |

The degF bug is not found by a round trip test: the rounded offset cancels out there and back. That is on purpose, see task 3 of pytest 02.

Pipelines exercise 02 adds one more moment: a change to the default alarm limit that the existing tests catch, where the **test** is the one to update.

`solutions/bench-project` has the ruff settings, the four fixes, the complete test suite, `.pre-commit-config.yaml`, `.vscode/settings.json`, the reference pipeline and the example skill. `tests/test_bench_project.py` in this repository checks that the solution tests fail on exactly the four bugs, that ruff flags the exercise version and passes the solution, so the exercise and the solution cannot drift apart unnoticed.

## Checking the material

From the repository root:

```powershell
uv run pytest         # the Git setup script, the bench project, the solution and the planted bugs
uv run ruff check .   # lint
```

The slide commands are in [`slides/README.md`](slides/README.md).

## Still to verify on a real Azure DevOps organisation

These are written from documentation and memory, not tested on the Academy organisation yet:

- The exact labels in the Azure DevOps web pages used in the exercises: the pipeline creation wizard, the build validation dialog, the pull request Complete dialog and its merge types.
- That a Contributor with **Edit policies** on a repository can add the reviewer and build validation policies there.
- That the pre-commit hooks from GitHub (pre-commit exercise 02, task 2) download through Zscaler on a managed laptop. The local ruff hooks need no download.
- That `curl -LsSf https://astral.sh/uv/install.sh | sh` installs uv into `$HOME/.local/bin` on the `ubuntu-latest` image.
- The open points listed in `exercises/git/TRAINER.md`.
