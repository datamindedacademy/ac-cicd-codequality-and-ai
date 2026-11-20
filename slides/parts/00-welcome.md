---
layout: intro
role: Data engineer
photo: /jasper-goris.jpg
---

# Jasper <span class="dm-accent">Goris</span>

<p class="mt-4">Your trainer today. I like automations, skiing and cooking.</p>
<!--
Introduce yourself, then ask three questions with a show of hands: who was here on day 1, who has written a test before (in any language), and who has used Git at work. Day 1 ran out of time before Git, so for most people the Git part this morning is new. Say that explicitly: nobody is behind.
-->

---
layout: default
label: Welcome
---

# Three days: <span class="dm-accent">write</span> it, <span class="dm-accent">analyse</span> with it, <span class="dm-accent">trust</span> it

<div class="days">
<div class="dcard d1"><div class="top"><div class="ico"><div class="i-mdi-code-braces" /></div><span class="num">Day 1</span></div><b>Python and Git 101</b><span class="sub">Write a script</span><ul><li>Python on your laptop, uv</li><li>The language, files, errors</li></ul></div>
<div class="conn">→</div>
<div class="dcard d2"><div class="top"><div class="ico"><div class="i-mdi-chart-line" /></div><span class="num">Day 2</span></div><b>Data analysis</b><span class="sub">Turn measurements into answers</span><ul><li>pandas and NumPy</li><li>SciPy and scikit-learn</li><li>Plots with Matplotlib</li></ul></div>
<div class="conn">→</div>
<div class="dcard d3"><div class="top"><div class="ico"><div class="i-mdi-shield-check-outline" /></div><span class="num">Day 3</span><span class="today">today</span></div><b>Code you can trust</b><span class="sub">Share it, test it, check it automatically</span><ul><li>Git on Azure DevOps</li><li>ruff and pre-commit</li><li>Unit tests with pytest</li><li>Branch policies and pipelines</li></ul></div>
</div>

<p class="bring"><b>Bring your questions.</b> A script, a test you want to write, an error: ask it today.</p>

<style>
.days { display: grid; grid-template-columns: 1fr 26px 1fr 26px 1fr; align-items: stretch; margin-top: 10px; }
.conn { display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; color: var(--dm-connecting); }
.dcard { display: flex; flex-direction: column; gap: 4px; padding: 18px 18px 14px; border-radius: 12px; background: var(--dm-surface); border-top: 5px solid var(--dm-premium); }
.dcard.d3 { border-top-color: var(--dm-connecting); box-shadow: 0 0 0 2px var(--dm-connecting); }
.dcard .top { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.dcard .ico { width: 44px; height: 44px; border-radius: 10px; background: var(--dm-premium); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 26px; }
.dcard.d3 .ico { background: var(--dm-connecting); }
.dcard .num { font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: var(--dm-premium); }
.dcard .today { margin-left: auto; font-size: 12px; font-weight: 600; color: #fff; background: var(--dm-connecting); border-radius: 999px; padding: 2px 10px; }
.dcard b { font-size: 20px; color: var(--dm-premium); }
.dcard .sub { font-size: 14.5px; color: var(--dm-premium); opacity: 0.8; }
.dcard ul { margin: 8px 0 0; padding-left: 18px; }
.dcard li { font-size: 14.5px; line-height: 1.45; margin: 3px 0; }
.bring { margin-top: 16px; padding: 10px 16px; border-left: 4px solid var(--dm-connecting); background: var(--dm-authentic); border-radius: 0 8px 8px 0; font-size: 15.5px; color: var(--dm-premium); }
</style>

<!--
The same picture as on day 1, now with day 3 highlighted. Git moved from day 1 to today: day 1 spent its time on the Python fundamentals, which was the right call. Today is one story. This morning you learn to share code with Git and a pull request on Azure DevOps, and you clean up a small project with ruff and pre-commit. After lunch you write tests for that project, and then you make Azure DevOps check every pull request, and refuse the merge when a check fails or nobody approved. Day 2 is not needed for today.
-->

---
layout: default
label: Welcome
---

# Today in a nutshell: from a <span class="dm-accent">commit</span> to a check that <span class="dm-accent">blocks the merge</span>

<DmSteps class="mt-4">
<DmStep n="1" label="Git on Azure DevOps">Commit, branch, merge and push, from the command line</DmStep>
<DmStep n="2" label="ruff and pre-commit">A linter and a formatter that run before every commit</DmStep>
<DmStep n="3" label="Unit tests with pytest">Tests that say what correct means, and find the bugs in a small project</DmStep>
<DmStep n="4" label="Pull requests, policies and pipelines">Every change goes through a pull request, and nothing reaches main without a green run and an approval</DmStep>
</DmSteps>

<div class="times">
<span><b>09:00</b> setup check</span><span><b>09:15</b> Git</span><span><b>11:15</b> ruff</span><span><b>12:00</b> lunch</span><span><b>12:45</b> pytest</span><span><b>14:45</b> pipelines</span><span><b>16:15</b> wrap-up</span>
</div>

<style>
.times { display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 26px; font-size: 15px; color: var(--dm-premium); }
.times b { color: var(--dm-connecting); margin-right: 4px; }
</style>

<!--
Four steps, and each one needs the one before. In step 4 the command line merge of step 1 becomes a pull request, and that is where the pipeline reports. The ruff checks of step 2 and the tests of step 3 are what the pipeline runs. Two breaks of 15 minutes, around 10:10 (inside the Git block) and around 14:30; we move them when an exercise is in full flow. The day ends around 16:30.
-->

---
layout: default
label: Welcome
---

# Tonight you can do <span class="dm-accent">six things</span>

<div class="grid-3 goals">
<v-clicks>
<DmInfoCard icon="i-mdi-source-pull" title="Work with Git">

Clone, commit on a branch, merge and push from the command line

</DmInfoCard>
<DmInfoCard icon="i-mdi-auto-fix" title="Keep code clean">

Fix what ruff reports, and run it at every commit with pre-commit

</DmInfoCard>
<DmInfoCard icon="i-mdi-test-tube" title="Write a unit test">

For an existing function, and run the test suite

</DmInfoCard>
<DmInfoCard icon="i-mdi-bug-check-outline" title="Let a test find a bug">

Read a failing test, and decide if the code or the test is wrong

</DmInfoCard>
<DmInfoCard icon="i-mdi-shield-lock-outline" icon-tone="navy" title="Protect main">

Every change through a pull request: a reviewer and a required pipeline keep the codebase clean

</DmInfoCard>
<DmInfoCard icon="i-mdi-pipe" icon-tone="navy" title="Check every pull request">

A pipeline that runs ruff and pytest, and blocks the merge when one fails. Keeps the standards high

</DmInfoCard>
</v-clicks>
</div>

<!--
These are the end goals of today. We tick them off in the wrap-up. They are the ones from the training proposal for day 3, minus what we move to a later moment: type checking with ty, and coding agents. Those are in the backup slides, with skills and prompting tips if there is time at the end.
-->

---
layout: default
label: Welcome
---

# Check the tools, then <span class="dm-accent">clone the repository</span>

<div class="setup">
<div>
<p class="step">1 · Verify your tools</p>

```powershell
git --version
uv --version
code --version
git config --global user.name
```

</div>
<div>
<p class="step">2 · Get the course material on your laptop</p>

```powershell
cd $HOME\Documents
git clone https://github.com/datamindedacademy/ac-cicd-codequality-and-ai
cd ac-cicd-codequality-and-ai
uv sync
code .
```

</div>
</div>

<DmBanner class="mt-4" icon="i-mdi-lifebuoy" title="Something fails?">
Call me over. If Zscaler says it is checking a file, wait two minutes and run the command again.
</DmBanner>

<style>
.slidev-code { font-size: 13px !important; line-height: 1.6 !important; }
.setup { display: grid; grid-template-columns: 270px 1fr; gap: 24px; margin-top: 8px; }
.setup > * { min-width: 0; }
.step { font-weight: 600; font-size: 15px; color: var(--dm-connecting); margin: 0 0 6px; }
</style>

<!--
New participants were asked to follow the setup manual beforehand. Those who did not need about half an hour: let them start the manual now and pair them with a neighbour for the first Git exercise. The fourth command must print a name; if it is empty, they set it in the first Git exercise. Also check that everyone can sign in to the Azure DevOps organisation in the browser: open the URL on the whiteboard. On day 1 everyone met the Zscaler message on the first download; it usually clears in one or two minutes.
-->
