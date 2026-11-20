---
layout: section
---

# Clean code before the commit: <span class="dm-accent">ruff</span> and <span class="dm-accent">pre-commit</span>

<!--
The last block of the morning, right after the Git exercises. Participants first push the bench project to their own repository: that is a good recap of the Git block, so do it together on screen. Then two short rounds: ruff, then pre-commit. Everything here comes back this afternoon, when the pipeline runs the same checks.
-->

---
layout: default
label: 5 · ruff and pre-commit
---

# Your own repository: the <span class="dm-accent">bench project</span>

<div class="split">
<div>

```powershell
Copy-Item -Recurse exercises\bench-project `
  $HOME\bench-project
cd $HOME\bench-project
git init -b main
git add --all
git commit -m "Add the bench project"
git remote add origin <your bench repo URL>
git push -u origin main
uv sync
```

</div>
<div>

```text
bench-project/
├── pyproject.toml
├── uv.lock
├── src/bench/
│   ├── units.py
│   ├── readings.py
│   └── logs.py
└── tests/
    └── test_units.py
```

</div>
</div>

<p class="note">The rest of the day happens here: ruff and pre-commit now, tests and a pipeline this afternoon.</p>

<!--
Every Git command on the left is from this morning, plus uv sync from day 1. The URL is the one of their personal repository bench-<name>, created by the trainer; it is on the Clone button of the repository page. The project is a small Python package for the compressor test bench of day 1: unit conversions, single readings, and CSV logs. It was written by a colleague in a hurry: it runs, but ruff will have opinions, and this afternoon the tests will find four real bugs. Keep the structure on the right in mind: code in src, tests in tests, settings in pyproject.toml.
-->

---
layout: default
label: 5 · ruff and pre-commit
---

# A linter reads the code, a formatter <span class="dm-accent">rewrites</span> it

<DmColumns class="mt-2">
<DmColumn header="ruff check: likely mistakes" tone="navy">

```text
$ uv run ruff check .
src/bench/logs.py:3:8: F401 [*] `os` imported
  but unused
src/bench/readings.py:39:5: E741 Ambiguous
  variable name: `l`
Found 2 errors.
[*] 1 fixable with the `--fix` option.
```

`[*]`: ruff fixes it with `--fix`. The rest needs you.

</DmColumn>
<DmColumn header="ruff format: one layout for everyone" tone="violet" divider>

```python
# before
UNITS = {
    'bar' : ('pressure', 1.0, 0.0),
    'psi' : ('pressure', 1/14.5038, 0.0),
}
# after uv run ruff format .
UNITS = {
    "bar": ("pressure", 1.0, 0.0),
    "psi": ("pressure", 1 / 14.5038, 0.0),
}
```

</DmColumn>
</DmColumns>

<p class="note">The review is about what the code does, not about spaces and quotes.</p>

<!--
ruff is from the makers of uv, and it is both a linter and a formatter. The linter reports likely mistakes, each with a rule code: F401 is an unused import, E741 is a variable called l, which is easy to confuse with 1 or I. Explain a code with uv run ruff rule E741. The formatter does not report; it rewrites the layout, always the same way, so nobody argues about it in a review. ruff is a dev dependency of the bench project, so uv run ruff uses the version in uv.lock, the same as the pipeline will. The output on the slide is shortened.
-->

---
layout: default
label: 5 · ruff and pre-commit
---

# Choose the rules once, in <span class="dm-accent">pyproject.toml</span>

<DmColumns class="mt-2">
<DmColumn header="pyproject.toml: which rules" tone="navy">

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
# the defaults, plus
# E: pycodestyle errors
# B: likely bugs (bugbear)
extend-select = ["E", "B"]
```

</DmColumn>
<DmColumn header=".vscode/settings.json: on save" tone="violet" divider>

```json
"[python]": {
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": "explicit",
    "source.organizeImports.ruff": "explicit"
  }
}
```

</DmColumn>
</DmColumns>

<p class="note">Both files are committed: the laptop, the hook and the pipeline all use the same rules.</p>

<!--
ruff has sensible defaults. In pyproject.toml you add rule groups by their letter prefix. Start small and add a group when the team agrees; selecting everything on an existing project gives hundreds of findings and people stop reading them. The VS Code extension from the setup manual shows findings while you type. With the settings on the right, in the project folder, every save formats the file and applies the safe fixes. Because the file is in the repository, a colleague who clones it gets the same behaviour.
-->

---
layout: statement
---

# Exercise 01: <span class="dm-accent">ruff</span>

`exercises/code-quality/01-ruff`

<p class="words"><b>Words you can now use</b> linter · formatter · rule code · finding · autofix · pyproject.toml · format on save</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 15 minutes, including "Before you start" in exercises/code-quality/README.md: copy the bench project, push it, branch code-quality. Task 1 fixes everything automatically. Task 2 adds the E rules, which finds the variable l: that one needs a person. Task 3 is for the fast ones.
-->

---
layout: default
label: 5 · ruff and pre-commit
---

# pre-commit runs the checks <span class="dm-accent">before the commit exists</span>

<div class="split">
<div>

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uv run ruff check --fix
        language: system
        types: [python]
      - id: ruff-format
        name: ruff format
        entry: uv run ruff format
        language: system
        types: [python]
```

</div>
<div>

```text
$ git commit -m "Add MPa"
ruff check...........................Passed
ruff format..........................Failed
- files were modified by this hook
```

- A **Git hook** is a script Git runs before a commit
- `pre-commit install`: once per clone
- Failed? `git diff`, `git add`, commit again
- `git commit --no-verify` skips it: the pipeline still checks

</div>
</div>

<style>
.slidev-code { font-size: 12.5px !important; line-height: 1.45 !important; }
</style>

<!--
pre-commit is a tool from the setup manual that installs a Git hook. Before every commit it runs the hooks in this file on the staged Python files. A local hook runs a command from the project itself: uv run ruff, so the ruff version of uv.lock. When the formatter changes a file, the commit stops, so you can see what changed; add the file and commit again. Keep commit hooks fast: lint and format, not the whole test suite. Hooks can be skipped, by --no-verify or simply by never running pre-commit install. That is why this afternoon the server checks the same things on every pull request. The hooks are for fast feedback, the pipeline is the rule.
-->

---
layout: statement
---

# Exercise 02: <span class="dm-accent">pre-commit</span>

`exercises/code-quality/02-pre-commit`

<p class="words"><b>Words you can now use</b> Git hook · pre-commit · hook · stage · .pre-commit-config.yaml · local hook · --no-verify</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 14px; }
.words b { margin-right: 8px; }
</style>

<!--
About 15 minutes; it may run into the time after lunch. Task 2 downloads hooks from GitHub: through Zscaler that can need a retry after two minutes. If it keeps failing, skip it; tasks 1 and 3 use local hooks only. Before lunch, make sure everybody merged their branch into main with a pull request, even with unfinished tasks.
-->
