# Optional: skills and prompts for Copilot

Not part of the planned day. Do this when you are ahead, or after the training. The slides are in the backup section of the deck.

## Goal

Write an agent skill for a process in your work that does not fit in a script, and use it with Copilot on the bench project.

## Why this matters

Some work is a process, not a calculation: add a unit the way the team agreed, prepare a test report, review a pull request against a checklist. You cannot write that as a Python function, but you can write it down once, so that Copilot follows the same steps every time, for everyone on the team.

## Background

- An assistant only knows what is in its **context**: your question, the files it reads, the instructions of the project, and the earlier messages of the conversation. What is not in the context, it guesses.
- The context has a limited size, and everything in it competes for attention. A long, vague context gives worse answers than a short, precise one.
- **Repository instructions** in `.github/copilot-instructions.md` are added to every request in the repository. Keep them short: the conventions everybody must follow.
- An **agent skill** is a folder with a `SKILL.md` file: a name, a description, and step-by-step instructions. Only the name and the description are in the context all the time. The agent loads the rest when a request matches the description. So the description decides when the skill is used.
- In VS Code and the Copilot CLI, the skills of a project live in `.github/skills/<skill-name>/SKILL.md`. Your VS Code version may need agent skills switched on in the settings: search for "skills".
- `example-skill/add-unit/SKILL.md` in this folder is a complete example for the bench project.

## Tasks

### Task 1: use the example skill

Copy `example-skill/add-unit` to `.github/skills/add-unit` in your `bench-project`, on a new branch. In Copilot Chat in agent mode, ask: "Add support for the pressure unit MPa." Check that Copilot follows the steps of the skill: does it ask for the source of the factor, and does it show the failing tests before it changes the code?

Result: a pull request that adds MPa, with tests, that passes the pipeline. You read the diff before you complete it.

### Task 2: your own skill

Pick a process from your own work that you explain to new colleagues more than once. Write a `SKILL.md` for it: a description that says when to use it, and numbered steps that a new colleague could follow too. Then ask Copilot for that task in two different ways, and check that it picks up the skill both times.

Result: a skill in `.github/skills/` that Copilot uses without you naming it.

## Open question

Your skill says "Do not change existing tests". Copilot changes one anyway. Where would you notice that today, without reading every line it wrote?
