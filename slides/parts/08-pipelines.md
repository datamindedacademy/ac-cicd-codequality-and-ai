---
layout: section
---

# Protect <span class="dm-accent">main</span>: pull requests, policies and pipelines

<!--
The last part of the day, and deliberately not deep. First pull requests, which replace the command line merge of this morning. Then what branch policies are. Then one small pipeline that runs the ruff checks from this morning, and how to plug it into a branch policy. In the exercises participants set it up on their own repository, prove that a bad pull request cannot be completed, and then make the tests required too.
-->

---
layout: default
label: 8 · Pull requests
---

# A <span class="dm-accent">pull request</span> asks before it merges

<DmProcess class="mt-4">
<DmPhase label="Push a branch" />
<DmPhase label="Create" />
<DmPhase label="Review" />
<DmPhase label="Approve" />
<DmPhase label="Complete" />
</DmProcess>

<DmColumns class="mt-4">
<DmColumn header="This morning" tone="plain">

```powershell
git switch main
git merge feature/x
git push
```

You merge, alone, on your laptop

</DmColumn>
<DmColumn header="From now on" tone="violet" divider>

**Repos > Pull requests > New pull request**: your branch into `main`, a neighbour as reviewer. Azure DevOps does the merge when you click **Complete**.

</DmColumn>
</DmColumns>

<!--
This morning everybody merged into main on their own laptop and pushed. That works, but nobody looked at the change before it reached the version everyone uses. A pull request is the same merge, done by the server, after someone else had a look. It is a feature of Azure DevOps, not of Git: in the race car picture it is part of the car, not the engine. The steps: push your branch as usual, create the pull request in the browser with a title and a description of what and why, a colleague reviews and approves, and you click Complete, which does the merge on the server. Afterwards you pull main as usual. Demo it once on your bench-trainer repository.
-->

---
layout: default
label: 8 · Pull requests
---

# A good review answers <span class="dm-accent">three questions</span>

<div class="grid-3 mt-2">
<DmInfoCard icon="i-mdi-text-box-check-outline" title="Does it do what it says?">

Read the title and description, then the **Files** tab: is that the change?

</DmInfoCard>
<DmInfoCard icon="i-mdi-alert-outline" icon-tone="navy" title="Does it do anything else?">

A changed test, a deleted check, a data file, a password

</DmInfoCard>
<DmInfoCard icon="i-mdi-eye-outline" title="Can I understand it?">

If you cannot follow it, ask in a comment on the line

</DmInfoCard>
</div>

<p class="note">Then vote: <b>Approve</b>, or <b>Wait for author</b> with a comment. You review the change, not the colleague.</p>

<!--
Most participants have never reviewed code. Keep it to these three questions. The second one matters most and is what tools cannot do: a test that was quietly changed to make it pass, or a file that should never be in the repository. Show on screen how to leave a comment on a line in the Files tab, and where the Approve button is. A review is not an exam: asking "what does this line do?" is a good comment. And it matters more when part of the code comes from Copilot: the author may not have read every line either.
-->

---
layout: default
label: 8 · Branch policies
---

# Three checks, from <span class="dm-accent">fast</span> to <span class="dm-accent">certain</span>

<div class="layers">
<div class="ly"><b>Your laptop</b><span>pre-commit runs ruff at every commit</span><em>seconds, but can be skipped</em></div>
<div class="arr">→</div>
<div class="ly"><b>The pipeline</b><span>Azure DevOps runs ruff and pytest on every pull request</span><em>minutes, and cannot be skipped</em></div>
<div class="arr">→</div>
<div class="ly"><b>A colleague</b><span>reviews the diff and approves</span><em>hours, and sees what tools miss</em></div>
</div>

<p class="note">A <b>branch policy</b> makes the last two mandatory: no pull request into <code>main</code> is completed without them.</p>

<style>
.layers { display: grid; grid-template-columns: 1fr 30px 1fr 30px 1fr; align-items: stretch; margin-top: 22px; }
.ly { display: flex; flex-direction: column; gap: 6px; padding: 16px; border-radius: 10px; background: var(--dm-surface); color: var(--dm-premium); font-size: 15px; border-top: 5px solid var(--dm-connecting); }
.ly b { font-size: 18px; }
.ly em { font-style: normal; font-weight: 600; color: var(--dm-connecting); margin-top: auto; }
.arr { display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; color: var(--dm-connecting); }
</style>

<!--
Back to the race car from this morning: the pipeline is the scrutineering every car passes before it may race, and the branch policies are the race rules that nobody can skip. Each layer catches different things at a different speed. The hook is fast and personal, but anyone can skip it or forget to install it. The pipeline runs on the server for every pull request, so nobody can skip it. The reviewer is slow, but sees what no tool sees: is this the right change at all? Participants now put these rules on their own repository: a reviewer from the pull request slides, and the pipeline as a second requirement.
-->

---
layout: default
label: 8 · Branch policies
---

# A <span class="dm-accent">branch policy</span> is a rule the server enforces

<DmColumns class="mt-2">
<DmColumn header="On main" tone="navy">

- **Minimum number of reviewers**: one, and your own vote does not count
- **Build validation**: a pipeline must pass, marked **Required**
- With any required policy: no direct pushes to `main`

</DmColumn>
<DmColumn header="On the pull request" tone="violet" divider>

- The validation run starts by itself on every push to the branch
- It tests the merge: your branch plus the latest `main`
- **Complete** stays blocked until all required policies pass

</DmColumn>
</DmColumns>

<p class="note">Repos, Branches, the <b>...</b> menu of <code>main</code>, Branch policies.</p>

<!--
Show the branch policy page of your own demo repository live. The reviewer policy makes the pull request and its review mandatory. Build validation: it points at a pipeline, and runs it for every pull request into main. Required means the pull request cannot be completed while the run is red or still running. As soon as main has a required policy, Azure DevOps refuses direct pushes to it, for everyone without bypass rights. The validation run tests the merge result, so it catches the case where your branch and main are fine on their own but broken together.
-->

---
layout: default
label: 8 · Branch policies
---

# The pipeline: the <span class="dm-accent">same ruff checks</span>, on a fresh machine

<div class="split">
<div>

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include: [main]

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
        displayName: Install the packages from uv.lock
      - script: uv run ruff check .
        displayName: ruff check
      - script: uv run ruff format --check .
        displayName: ruff format --check
```

</div>
<div>

- **trigger**: also run after every push to `main`
- **pool**: a fresh Linux machine, the **agent**
- **job**: a list of **steps**, top to bottom
- The agent has no uv: install it first
- `uv sync --locked`: exactly `uv.lock`, or an error
- A step that fails turns the job red

</div>
</div>

<style>
.slidev-code { font-size: 11.5px !important; line-height: 1.4 !important; }
</style>

<!--
Walk through it top to bottom. The file lives in the repository, so it is versioned and reviewed like code. trigger is for pushes to main; pull request runs come from the branch policy, not from this file. pool asks Azure for a Microsoft-hosted Linux machine that exists only for this run. The first step installs uv with the official installer, and the echo line is a logging command that puts uv on the PATH for the next steps. uv sync --locked installs Python and the exact versions in uv.lock, and refuses when the lockfile does not match pyproject.toml: on a machine that only checks, you never want it to quietly change the lockfile. Then the same two ruff commands as this morning. ruff returns an error code when it finds something, which turns the step red.
-->

---
layout: default
label: 8 · Branch policies
---

# Add it to Azure DevOps in <span class="dm-accent">three steps</span>

<DmSteps class="mt-4">
<DmStep n="1" label="Create the pipeline">Push the file on a branch. Pipelines, New pipeline, Azure Repos Git, your repository, Existing Azure Pipelines YAML file. Run it once.</DmStep>
<DmStep n="2" label="Make it a policy">Repos, Branches, the ... menu of main, Branch policies. Build validation, add your pipeline, Automatic, Required. Also: minimum number of reviewers, 1.</DmStep>
<DmStep n="3" label="Open a pull request">The validation run starts by itself. Complete is blocked until the run is green and a colleague approved.</DmStep>
</DmSteps>

<!--
Demo all three live on your bench-trainer repository, before exercise 01. Show the run page: the steps, a log, the commit it ran on. Then the policy page. Then a pull request with the validation status next to the reviewers. If the run waits in the queue, that is the parallel job limit of the organisation: say so, and look at an earlier run in the meantime.
-->

---
layout: statement
---

# Exercise 01: <span class="dm-accent">A format check and branch policies</span>

`exercises/pipelines/01-format-check-and-policies`

<p class="words"><b>Words you can now use</b> pull request · reviewer · approve · complete · branch policy · minimum number of reviewers · build validation · required check · pipeline · agent · job · step · run</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 35 minutes, much of it waiting for runs. Pair neighbours first: they approve each other's pull requests. Task 3 is the heart of the exercise: three attempts to break the rules, each refused for a different reason. Walk around and ask people to say which policy refused which attempt. Task 4 is optional.
-->

---
layout: default
label: 8 · Branch policies
---

# The tests: a <span class="dm-accent">second job</span>, required at once

<div class="split">
<div>

```yaml
jobs:
  - job: lint
    displayName: Lint and format
    steps:
      # ... as before

  - job: test
    displayName: Tests
    steps:
      # install uv, uv sync --locked, as before
      - script: uv run pytest
        displayName: Run the tests
```

</div>
<div>

- Jobs run in parallel, each on its own machine
- The policy points at the pipeline, so the new job is required from the next run on
- A failing test: pytest returns an error, the job is red, **Complete** is blocked

</div>
</div>

<!--
Adding the tests is one more job in the same file. No change to the policy is needed: the policy requires the whole pipeline to be green. Each job starts on an empty machine, so the test job needs its own uv installation; that duplication is the open question of exercise 02. In the exercise, a pull request changes the default alarm limit from 8.5 to 9.0 because of a newer datasheet. The tests go red. Ask the room: who is wrong, the code or the test? Here the datasheet is right, so the test is the one to update, in a second commit on the same pull request.
-->

---
layout: statement
---

# Exercise 02: <span class="dm-accent">The tests as a required check</span>

`exercises/pipelines/02-tests-required`

<p class="words"><b>Words you can now use</b> job · parallel jobs · exit code · required check · test results</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 25 minutes. Task 2 is the moment of the day: a pull request with a red test, and a Complete button that does not work. Task 3 is optional: publish test results, and a path filter for README-only changes.
-->
