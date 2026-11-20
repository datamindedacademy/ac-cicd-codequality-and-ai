---
layout: section
title: Backup - Working with AI
---

# Backup: skills, context and <span class="dm-accent">prompts</span>

<!--
Backup, not part of the planned day: use it when there is time left at the end, or when the group asks about Copilot. Four slides: what the assistant actually sees, how to write a skill, what to watch out for, and prompting tips. The optional exercise is exercises/ai, with a complete example skill for the bench project. On day 1 many participants turned Copilot's suggestions off because they could not judge them; this part is about getting answers you can judge.
-->

---
layout: default
label: Backup · AI
---

# The assistant only knows its <span class="dm-accent">context</span>

<div class="split">
<div class="ctx">
<div class="cb always"><b>Always</b>system instructions, <code>.github/copilot-instructions.md</code>, the names and descriptions of skills</div>
<div class="cb now"><b>This request</b>your prompt, open or attached files, what the agent reads and runs</div>
<div class="cb hist"><b>This conversation</b>every earlier message and answer, including the wrong turns</div>
<div class="cb miss"><b>Not in it</b>your datasheet, your team's habits, what you meant: it guesses</div>
</div>
<div>

- The context has a **limited size**, and everything in it competes for attention
- Long and vague gives worse answers than short and precise
- A long chat drifts: start a new one for a new task
- What it needs every time, write down once: instructions and skills

</div>
</div>

<style>
.ctx { display: flex; flex-direction: column; gap: 8px; }
.cb { padding: 10px 14px; border-radius: 8px; background: var(--dm-surface); font-size: 14px; color: var(--dm-premium); border-left: 5px solid var(--dm-connecting); }
.cb b { display: block; font-size: 15.5px; margin-bottom: 2px; }
.cb.miss { border-left-color: var(--dm-premium); background: var(--dm-authentic); }
</style>

<!--
The model knows nothing about your project except what is in its context window for this request. Some things are always there: the system instructions of the tool, the repository instructions file, and, for skills, only their names and descriptions. Then what this request adds: the prompt, the files you attach or that are open, and everything an agent reads or runs on the way. Then the history of the chat, including the dead ends; after a long session it can get confused by its own earlier mistakes, so start a new chat for a new task. Everything else, it fills in with guesses that sound confident. The practical consequence: put the important things in the context on purpose, and keep the rest out.
-->

---
layout: default
label: Backup · AI
---

# A <span class="dm-accent">skill</span> writes a process down once

<div class="split">
<div>

```markdown
---
name: add-unit
description: Add a new pressure or temperature
  unit to the bench project, with tests from
  known values. Use when asked to support a
  new unit such as MPa or mbar.
---

# Add a unit to the bench project

## 1. Find the conversion
- Ask for the source of the factor ...
## 2. Tests first
- Add rows to test_convert_known_values ...
## 3. Change the code
## 4. Check
- uv run pytest, ruff check, ruff format --check
```

</div>
<div>

- A folder `.github/skills/add-unit/` with a `SKILL.md`
- Only **name** and **description** sit in the context all the time
- The agent loads the steps when a request matches the description
- For a process, not a calculation: that is a function

</div>
</div>

<style>
.slidev-code { font-size: 12px !important; line-height: 1.4 !important; }
</style>

<!--
A skill is a short instruction document for a process that you would otherwise explain to every new colleague. The frontmatter has a name and a description; the body has the steps. This is the key design: the description is always in the context, so it must say when to use the skill. The body is only loaded when it is needed, so a project can have many skills without filling the context. Use skills for processes with judgement in them: adding a unit the way the team agreed, preparing a test report, reviewing a pull request against a checklist. If the process is a fixed calculation, write a Python function and a test instead. The full example is in exercises/ai/example-skill. In VS Code the location is .github/skills; depending on the version, agent skills may need to be switched on in the settings.
-->

---
layout: default
label: Backup · AI
---

# What makes a <span class="dm-accent">good skill</span>

<div class="grid-2 mt-2">
<DmInfoCard icon="i-mdi-text-search" title="The description decides">

Say what it does and when to use it, with the words people will type: "new unit", "MPa", "mbar"

</DmInfoCard>
<DmInfoCard icon="i-mdi-format-list-numbered" icon-tone="navy" title="Steps a new colleague could follow">

Numbered, concrete, with file and function names. Short: every line costs context

</DmInfoCard>
<DmInfoCard icon="i-mdi-hand-back-left-outline" icon-tone="navy" title="Say when to stop and ask">

"Do not guess a conversion factor", "Do not change existing tests"

</DmInfoCard>
<DmInfoCard icon="i-mdi-check-decagram" title="End with a check">

The commands that prove it worked: tests, ruff, and a summary for the reviewer

</DmInfoCard>
</div>

<p class="note">Never put passwords, tokens or customer data in a skill: it is a file in the repository, and it goes into the context.</p>

<!--
The description is the trigger: if it is vague, the skill is never used, or used for the wrong task. Test it by asking for the task in two different ways and checking that the skill is picked up both times. The steps are read by a model with a limited context, so be short and concrete, and name files and functions instead of describing them. The stop rules matter most for the things you cannot check afterwards, such as where a number comes from. And always end with the check: the tests and the pipeline from today are what make an agent's work verifiable.
-->

---
layout: default
label: Backup · AI
---

# Prompting tips: say it like a <span class="dm-accent">specialist</span>

<DmColumns class="mt-2">
<DmColumn header="Vague" tone="plain">

<p class="prompt bad">Can you add tests for my code?</p>

- Which code, which cases?
- What counts as done?
- It will guess, and often over-build

</DmColumn>
<DmColumn header="Specific" tone="violet" divider>

<p class="prompt">Write parametrized pytest tests for classify in src/bench/readings.py: both boundaries from both sides, per its docstring. Run uv run pytest. If a test fails, tell me if the code or the test contradicts the docstring. Do not change the code yet.</p>

</DmColumn>
</DmColumns>

<div class="tips">
<span><b>Name</b> files, functions and tools</span><span><b>Scope</b> one task, and what must not change</span><span><b>Ask</b> for a plan or questions first</span><span><b>Verify</b> with tests, then read the diff</span>
</div>

<style>
.prompt { font-family: monospace; font-size: 14px; line-height: 1.55; background: var(--dm-surface); border-left: 4px solid var(--dm-connecting); border-radius: 8px; padding: 12px 14px; margin: 0 0 8px; }
.prompt.bad { border-left-color: var(--dm-premium); }
.tips { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 14px; font-size: 14px; color: var(--dm-premium); }
.tips span { padding: 8px 10px; border-radius: 8px; background: var(--dm-authentic); }
.tips b { color: var(--dm-connecting); margin-right: 4px; }
</style>

<!--
The specific prompt uses only words from today: parametrized, pytest, boundaries, docstring, uv run pytest. That vocabulary is what makes the request precise, and a precise request is also faster and cheaper: fewer rounds, less code to throw away. The four tips: name things instead of describing them; keep the scope to one task and say what must stay untouched; for anything bigger than a few lines, ask for a plan or for questions before any code; and check the result with the tests and the diff, not by reading the explanation. If an answer goes in the wrong direction, a new chat with a better prompt usually beats arguing in the old one.
-->
