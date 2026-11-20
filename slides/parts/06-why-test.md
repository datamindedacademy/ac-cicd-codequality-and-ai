---
layout: section
---

# Why <span class="dm-accent">test</span>?

<!--
Before any pytest syntax: why bother. Most participants test by running a script and looking at the output. That is testing too. A unit test keeps that look, so it happens again on every change, without you.
-->

---
layout: default
label: 6 · Why test
---

# Code nobody dares to touch becomes <span class="dm-accent">legacy</span>

<DmColumns class="mt-2">
<DmColumn header="Without tests" tone="plain">

- "It works, don't touch it"
- Every change is a risk, so changes get postponed
- Postponed changes pile up into a migration nobody wants
- You find the bug when a colleague uses the wrong number

</DmColumn>
<DmColumn header="With tests" tone="violet" divider>

- Change the code, run the tests, know in seconds
- Small changes, often, are cheap
- A bug you fix gets a test, so it cannot come back
- The tests show a colleague how to use the function

</DmColumn>
</DmColumns>

<p class="note">If it hurts, do it more often. Tests are what makes "often" cheap.</p>

<!--
The point of tests is not proving that code is correct today. It is being able to change it tomorrow. A script with tests is a script you dare to change when the datasheet changes, the log format changes, or a colleague asks for one more column. A script without tests slowly becomes the file nobody wants to open. This comes from the Dataminded skillboost on testing: teams that deploy often and recover fast are the ones with a strong automated test suite; speed and stability are not a trade-off.
-->

---
layout: default
label: 6 · Why test
---

# The earlier you find a bug, the <span class="dm-accent">cheaper</span> it is

<div class="cost">
<div class="c c1"><b>While writing</b><span>a test turns red</span><em>seconds</em></div>
<div class="c c2"><b>In the pull request</b><span>the pipeline turns red</span><em>minutes</em></div>
<div class="c c3"><b>After the merge</b><span>a colleague's script breaks</span><em>hours</em></div>
<div class="c c4"><b>In a report</b><span>a decision used a wrong number</span><em>weeks, and trust</em></div>
</div>

<p class="note">Today we move the bugs to the left: into a test on your laptop, and into the pipeline of the pull request.</p>

<style>
.cost { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 18px; }
.c { display: flex; flex-direction: column; gap: 6px; padding: 16px 14px; border-radius: 10px; background: var(--dm-surface); color: var(--dm-premium); font-size: 15px; }
.c b { font-size: 18px; }
.c em { font-style: normal; font-weight: 600; color: var(--dm-connecting); margin-top: auto; }
.c1 { border-top: 5px solid #b9b3e6; } .c2 { border-top: 5px solid #8d82e0; } .c3 { border-top: 5px solid #6a5bdc; } .c4 { border-top: 5px solid var(--dm-premium); }
</style>

<!--
Walk from left to right. On the left, the person who made the mistake finds it, still has the code in their head, and fixes it in seconds. On the right, somebody else finds it, maybe months later, after a decision was made with the wrong number. Ask the room for an example from their own work of a bug that was found late. There is always one.
-->

---
layout: default
label: 6 · Why test
---

# Most tests should be <span class="dm-accent">small and fast</span>

<div class="split">
<div class="pyr">
<div class="lvl l3"><b>End to end</b><span>the whole chain, slow, few</span></div>
<div class="lvl l2"><b>Integration</b><span>parts together: files, a database</span></div>
<div class="lvl l1"><b>Unit</b><span>one function, in memory, many</span></div>
</div>
<div>

A **unit test**:

- tests one function
- runs in milliseconds
- gives the same result every time
- needs no network, database or real data file
- fails with a message that points to the cause

</div>
</div>

<style>
.pyr { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.lvl { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 12px; border-radius: 8px; color: #fff; text-align: center; font-size: 13.5px; }
.lvl b { font-size: 17px; }
.l3 { width: 45%; background: var(--dm-premium); }
.l2 { width: 72%; background: #6a5bdc; }
.l1 { width: 100%; background: var(--dm-connecting); }
</style>

<!--
The test pyramid. At the bottom many unit tests: cheap to write, fast to run, and when one fails it points to one function. Higher up, fewer and slower tests that check that the parts work together, up to a full end-to-end run of a script on a real log folder. Many teams build the pyramid upside down: they only have a few manual end-to-end checks, which are slow and tell you that something is wrong but not where. Today is all about the bottom layer. Exercise 03 touches the second layer: a test that reads a small file in a temporary folder.
-->

---
layout: default
label: 6 · Why test
---

# What is worth a <span class="dm-accent">test</span>?

<DmColumns class="mt-2">
<DmColumn header="Test" tone="violet">

- Your calculations and conversions
- Decisions: limits, thresholds, `if` chains
- Boundary values: exactly at the limit, empty, zero, negative
- Bad input: what should happen, and does it
- Every bug you fixed

</DmColumn>
<DmColumn header="Do not test" tone="plain" divider>

- Python itself, or pandas: their makers test them
- Constants and settings on their own
- The exact wording of every message
- Private helper functions directly: test them through the function that uses them

</DmColumn>
</DmColumns>

<p class="ask"><b>Ask</b>A function returns <code>True</code> when it is a working day between 9:00 and 17:00. Which inputs would you test?</p>

<!--
Answer to the question: the boundaries. 8:59, 9:00, 16:59, 17:00 and 17:01, a Saturday and a Sunday, and Monday morning. The middle of a Tuesday afternoon is the least interesting test. This example is from the Dataminded skillboost on testing: code that looks too simple to test is often where the boundary bugs hide. The rule of thumb for the left column: test what you would check by hand if you had to sign for the result.
-->
