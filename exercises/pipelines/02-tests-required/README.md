# 02 - The tests as a required check

**Words to use:** job, parallel jobs, exit code, required check, test results, JUnit XML, condition.

## Goal

Add your test suite to the pipeline, so that a pull request with a failing test cannot be completed either.

## Why this matters

A format check keeps the code readable. The tests keep it correct. With both in the validation run, a pull request that breaks a calculation is stopped before it reaches `main`, also when the author forgot to run the tests, and also when part of the code came from Copilot.

## Background

- A pipeline can have several **jobs**. They run in **parallel**, each on its own fresh machine. The pull request shows the run as red when one of them is red.
- The build validation policy from exercise 01 points at the pipeline, not at a job. A new job in the same pipeline is therefore required from the next run on, without changing the policy.
- pytest returns a non-zero **exit code** when a test fails. That makes the step red, and with it the job and the run.
- The second job needs uv too: each job starts on an empty machine.

```yaml
  - job: test
    displayName: Tests
    steps:
      - script: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "##vso[task.prependpath]$HOME/.local/bin"
        displayName: Install uv

      - script: uv sync --locked
        displayName: Install Python and the packages from uv.lock

      - script: uv run pytest
        displayName: Run the tests
```

- `pytest --junitxml=test-results.xml` also writes the results to a file that the task `PublishTestResults@2` reads. It fills the **Tests** tab of the run with every test by name. `condition: succeededOrFailed()` runs that step also when the tests failed, which is exactly when you need it.

## Tasks

Start a new branch `add-tests-to-pipeline` from an up-to-date `main`.

### Task 1: a second job

Add the `test` job from the Background to `azure-pipelines.yml`, under `jobs:` and next to the `lint` job. Commit, push, and open a pull request with your neighbour as reviewer.

Result: the validation run of the pull request shows two jobs, **Lint and format** and **Tests**, both green. Complete the pull request after the approval.

### Task 2: a pull request that must wait

Make a branch `change-alarm-limit`. On it, change the default `alarm_bar` of `classify` in `readings.py` from 8.5 to 9.0, as if a colleague read a newer datasheet, but leave the tests as they are. Commit and push. If your pre-push hook from this morning stops you, that is the hook doing its job: push with `git push --no-verify` this once. Open a pull request.

Look at the pull request: which job failed, which test, and can you complete it? Then decide who is right. Suppose the datasheet is right: update the tests in a second commit on the same branch, push, and watch the pull request update itself. Complete it after the approval.

Result: the pull request shows one failed and one successful validation run, and it is completed with your neighbour's approval.

### Task 3: test results on the pull request

This one is much harder, and optional.

Make the pipeline publish the test results, also when a test fails, so that a reviewer sees which test failed without opening a log. Prove it with a pull request that breaks one test on purpose: find the failing test in the **Tests** tab of the run. Then repair it.

Also make sure that a pull request that only changes `README.md` needs no pipeline run at all. Look at the options of the build validation policy.

Result: a run whose **Tests** tab lists all tests by name, and a README-only pull request that completes without a run.

## Open question

The lint job and the test job each install uv and the packages again, and every run starts from scratch. For this small project that takes a minute. For a project with large packages, such as pandas or scikit-learn, it can take much longer. What could you do about that, and what would it cost you?
