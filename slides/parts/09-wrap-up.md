---
layout: default
label: Wrap-up
---

# You can now do <span class="dm-accent">all six things</span>

<div class="grid-3">
<DmInfoCard icon="i-mdi-check-bold" title="Work with Git">

Branch, commit, merge, push

</DmInfoCard>
<DmInfoCard icon="i-mdi-check-bold" title="Keep code clean">

ruff in pyproject.toml, pre-commit at every commit

</DmInfoCard>
<DmInfoCard icon="i-mdi-check-bold" title="Write a unit test">

assert, approx, parametrize, fixtures

</DmInfoCard>
<DmInfoCard icon="i-mdi-check-bold" title="Let a test find a bug">

Four bugs found in the bench project

</DmInfoCard>
<DmInfoCard icon="i-mdi-check-bold" icon-tone="navy" title="Protect main">

A reviewed pull request, with a required pipeline

</DmInfoCard>
<DmInfoCard icon="i-mdi-check-bold" icon-tone="navy" title="Check every pull request">

ruff and pytest in Azure Pipelines

</DmInfoCard>
</div>

<!--
Go through the list with a show of hands, as on day 1. Ask which of the four bugs in the bench project they found themselves: the alarm boundary, the unknown unit, the degF offset, and notes.txt in the log folder. Each one is a realistic bug that a quick manual run would not have shown.
-->

---
layout: default
label: Wrap-up
---

# Read this prompt <span class="dm-accent">again</span>

<p class="prompt">On a new branch, add a parametrized pytest test for classify with boundary values on both sides of each limit, and a test with tmp_path for read_pressures with one ERR row. Run uv run pytest. If a test fails, tell me whether the code or the test contradicts the docstring, and fix the code, not the test. Commit so that the pre-commit hooks run, then push and open a pull request into main; the build validation must be green and a colleague must approve before I complete it.</p>

<style>
.prompt { font-family: monospace; font-size: 17px; line-height: 1.6; background: var(--dm-surface); border-left: 4px solid var(--dm-connecting); border-radius: 8px; padding: 18px 22px; margin-top: 16px; }
</style>

<!--
Every term in this prompt is from today. Ask the room which ones they could not have explained this morning. That is the vocabulary that lets you direct an assistant, and judge what it brings back.
-->

---
layout: default
label: Wrap-up
---

# Take it <span class="dm-accent">home</span>

<DmColumns class="mt-2">
<DmColumn header="This week" tone="navy">

- Pick one script you use at work
- Move one calculation into a function
- Write three tests for it, boundaries first
- Put it in a repository with ruff, pre-commit and a pipeline

</DmColumn>
<DmColumn header="Next steps" tone="plain" divider>

- ty: type checking, as a third check
- Skills and prompting tips for Copilot
- `exercises/ai` in the course repository
- See the backup slides

</DmColumn>
<DmColumn header="Read more" tone="violet" divider>

- pytest docs (`docs.pytest.org`)
- Azure Pipelines YAML reference (`learn.microsoft.com`)
- uv docs (`docs.astral.sh/uv`)
- Pro Git book (`git-scm.com/book`)

</DmColumn>
</DmColumns>

<!--
The first column is the homework that matters: one real script, three real tests. A test suite starts with one test. The middle column is what we left out of today to keep the pace: type checking with ty, and working with Copilot through skills and specific prompts. Show the backup slides if there is time, otherwise point to them and to the optional exercise in exercises/ai. All material stays available: the course repository, the slides as PDF, and their own bench repository on Azure DevOps for as long as the organisation exists.
-->

---
layout: thanks
---

# Thank <span class="dm-accent">you</span>

<!--
Thank the group. Ask for feedback on the three days. Remind them of the homework and where to find the material.
-->
