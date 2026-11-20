# Trainer guide: Git exercises on Azure DevOps

What to prepare in Azure DevOps before the training, how to run the Git block that opens day 3, and what can go wrong.

The Git part was planned for day 1 and did not fit. Day 3 now opens with it: 09:15 to 11:15, break included. Participants have used VS Code, PowerShell and uv for two days, but most have never used Git. Treat them as Git beginners.

## Open item: access for Atlas Copco accounts

How Atlas Copco accounts get into the Dataminded Academy organisation is **still being arranged**. The likely route is to invite them as guest users (Microsoft Entra B2B) in the tenant that the organisation is connected to. Until that is settled, check the following with the organisation owner and with Atlas Copco IT:

- Guest users are allowed in the organisation (Organization settings > Policies, the external guest access policy).
- Atlas Copco's conditional access lets their work accounts sign in to another tenant from the managed laptops.
- Each participant gets the **Basic** access level. Stakeholder access does not include Azure Repos in a private project.
- Someone has a fallback plan if a few accounts are not ready on the day (see section 3).

Do not assume this works until one Atlas Copco account has cloned and pushed from a managed laptop.

## Open item: shared repositories with the afternoon

Agree with the trainer of the pipelines part whether the afternoon reuses these training repositories. If it does, the branch policy on `main` (pull requests, reviewers, build validation) must go on only after 11:15: exercise 5 pushes directly to `main`. If the afternoon uses its own repositories, nothing changes here.

## 1. Prepare Azure DevOps (about 30 minutes, a few days before)

### Project and repositories

1. In the Dataminded Academy organisation, create a **private project** for this training (for example `atlas-copco-python`). Azure DevOps creates a repository with the project's name. You can use it for group A, or ignore it.
2. Create **one repository per group** under **Repos**, with the repository dropdown at the top and the option to create a new repository (for example `training-repo-group-a`). Keep groups to about 10 to 15 people: everyone pushes to the same `main` in exercise 5, and more people means more rejected pushes in a row.
3. When you create each repository, leave the README and `.gitignore` options off. An empty repository is easiest to seed.
4. The default branch must be `main`. New repositories use `main` unless the organisation changed the default branch name. The first push below creates it.

The pytest and Azure Pipelines part later in the day may use its own repositories. If it reuses these, agree with that trainer when the branch policy on `main` goes on: not before 11:15, because the morning pushes directly to `main`.

### Access

1. Add every participant to the organisation (Organization settings > Users > Add users) with access level **Basic**, add them to the training project, and put them in the project group **Contributors**. Contributors can read, clone, create branches, push to any branch including `main`, and delete branches they created.
2. Do not make anyone a Project Administrator. Administrators can change repository settings and permissions.
3. Ask participants to open `https://dev.azure.com/<organisation>` in the browser once before the training and accept the invitation, so you know their account works. Check in Organization settings > Users that every participant is listed with access level Basic.

Participants must be able to sign in with their invited account in the window of Git Credential Manager.

### No branch policy on `main` in the morning

The morning block has **no branch policy** on `main`. In exercise 5 participants merge their branch into `main` on the command line and push `main` directly. With a policy on, that push is refused with `TF402455` and the exercise cannot be done. Pull requests and branch policies are the afternoon's topic (pipelines part).

Under **Repos > Branches**, open the menu (**...**) next to `main`, choose **Branch policies** and check that nothing is turned on. Under Project settings > Repositories > the repository > Security, check that the group **Contributors** has **Contribute** and **Create branch** allowed, and **Force push (rewrite history, delete branches and lock branches)** not set. Without force push, nobody can rewrite `main`. Participants can still delete the branches they created themselves, which exercise 5 needs.

Test it: with a participant-level account (Contributor, not an administrator), make a branch, commit, merge it into `main` and run `git push`. It must be accepted. Then run `git push origin --delete <that branch>`: also accepted. Push a commit to `main` from a second clone first, and check that the push from the first clone is refused with `(fetch first)`.

If the afternoon reuses these repositories, the branch policy goes on after 11:15 (see the root TRAINER.md and the pipelines material).

## 2. Seed content for the training repository

The folder `exercises/git/training-repo-seed/` in this course repository holds the starting content:

| File | Purpose |
|---|---|
| `README.md` | Rules and a map of the repository. |
| `participants/.gitkeep` | Makes Git keep the empty `participants` folder. |
| `.gitignore` | Ignores `.venv/`, `__pycache__/`, `*.pyc`. |
| `check_setup.py` | Tiny script to check that Python runs in the clone. |

Push it to the empty repository. Work **outside** the course repository, so you do not nest repositories. In PowerShell, from the root of the course repository:

```powershell
Copy-Item -Recurse -Force exercises/git/training-repo-seed "$HOME\seed-upload"
cd "$HOME\seed-upload"
git init -b main
git add --all
git commit -m "Add seed content for the training repository"
git remote add origin https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
git push -u origin main
```

A sign-in window opens on the first push. Afterwards, open **Repos > Files** for that repository and check that you see `README.md`, `check_setup.py`, `.gitignore` and `participants/`.

For every other group repository, run these two commands in the same folder:

```powershell
git remote set-url origin https://dev.azure.com/<organisation>/<project>/_git/<training-repo-group-b>
git push -u origin main
```

Then check access and the absence of a branch policy (section 1) on every repository.

Finally, write down the real URL per group:

```
https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
```

Hand it to participants at the start of exercise 4, for example on the whiteboard or in the chat. The placeholders `<organisation>`, `<project>` and `<training-repo>` in all exercise texts refer to this URL. The **Clone** button on **Repos > Files** shows the same URL, sometimes with `<organisation>@` in front of `dev.azure.com`. Both forms work.

## 3. Check the laptops (end of day 2, or the first minutes of day 3)

On one managed laptop, with an Atlas Copco account, in PowerShell:

```powershell
git --version
git credential-manager --version
uv --version
git config --global --list
git clone https://dev.azure.com/<organisation>/<project>/_git/<training-repo> "$HOME\git-exercises\test-clone"
```

- Git for Windows is installed and on the PATH. Git Credential Manager comes with it.
- The sign-in window of Git Credential Manager appears and accepts the invited account. If it signs in silently with the wrong account, or conditional access blocks it, find out now (see section 5).
- The setup script runs: `uv run python exercises/git/setup_exercise.py 2`.
- `code .` opens VS Code from the terminal. Participants use it in every exercise to open the exercise folder in a second VS Code window, next to the course repository. Show the two windows once before exercise 1.
- The execution policy is `Restricted`. Nothing in these exercises needs `.ps1` files.

Fallback if some accounts cannot reach Azure DevOps on the day: exercises 1 to 3 work offline. Pair those participants with a neighbour whose account works for exercises 4 and 5: they type the commands together on the neighbour's laptop. If nobody can reach it, create a local "remote" for 4 and 5: `git init --bare $HOME\git-exercises\remote.git`, then clone it twice. Merge, push, rejected push and `git push origin --delete` all work against it; only the browser views are missing.

## 4. Running the session (09:15 to 11:15)

The block is 120 minutes: about 30 minutes of slides and demo, about 70 minutes of exercises, and a 15-minute break.

| Time | Content |
|---|---|
| 09:15 | Slides parts 1 and 2 up to the first exercise (about 12 min): why version control, the three areas, hash, branch, the remote, identity, add, commit, log, diff. |
| 09:27 | Exercise 1 (18 min). Draw the three areas on the whiteboard first. Task 2 is about staging: walk around and ask for the prediction before people run `git status`. |
| 09:45 | Slides: branch and merge, conflict, rebase (about 7 min). |
| 09:52 | Exercise 3 (18 min). The merge conflict is task 2. |
| 10:10 | Break (15 min). Write the repository URLs on the whiteboard during the break. |
| 10:25 | Slides part 3, Azure Repos (about 7 min): live clone from **Repos > Files > Clone**, the sign-in window, push. |
| 10:32 | Exercise 4 (15 min). Expect sign-in problems: see below. |
| 10:47 | Slide "Bring your branch into main and share it" (about 3 min): live `git switch main`, `git pull`, `git merge`, `git push`, and a refused push with `(fetch first)`. |
| 10:50 | Exercise 5 (19 min). Expect a wave of rejected pushes on `main`: that is the point. Pair up neighbours for task 3. |
| 11:09 | Demo of exercise 6 in VS Code (2 min, the Source Control view only), branching models (3 min), questions. |
| 11:15 | End of the Git block. The morning goes on with uv, ruff and pre-commit on the bench project (see the root TRAINER.md). |

Exercise 2 (history) is not done in class. It is for early finishers and for later. Exercises 3 to 5 do not depend on it. Exercise 6 is a demo only.

Exercises 1 to 5 have three tasks each. Each task states a result. There are no hints: participants find the commands in the slides, the cheat sheet in `exercises/git/README.md` or `git help`. The full command sequences are in `solutions/git/README.md`. Point a stuck participant to the right slide before you give a command. The last task of each exercise is much harder. The times above cover the tasks before it. Most participants will not finish the last task in class, and nothing later depends on it.

**If it runs late**, in this order:

1. Drop the branching models slides. Say one sentence: short branches merged into `main` quickly, which is what they just did, and this afternoon a pull request goes on top.
2. Do the merge conflict of exercise 3 (task 2) as a trainer demo on your screen instead of hands-on. Keep task 1 (branch, commit, fast-forward merge) as an exercise.
3. Shorten the exercise 6 demo to one commit in the Source Control view, or skip it and point to the README.
4. Never drop exercises 4 and 5: they reach the end goal (clone, branch, commit, push, merge into `main`, pull), and the pull requests of the afternoon build on them. If time is short in exercise 5, keep task 1 and do task 2 (clean up) as a demo.

If it runs very late, do not eat into the next block. Cut the last task of every exercise first.

Mention only briefly: GitFlow versus trunk-based development, cherry-pick, stash, tags. Rebase has a slide and is task 3 of exercise 3.

### Copilot and checking understanding

- Participants may use Copilot in VS Code (inline completions and chat) all day, including in the Git block. The ground rules are in `exercises/git/README.md` under "Using Copilot". No task needs Copilot.
- Ask participants to type the Git commands themselves. Copilot is for explaining messages and for changing code, which they then inspect with `git diff`.
- To check understanding, walk around, pick two or three people per exercise and ask them to say what they just did. Listen for the terms in the "Words to use" line.
- Every exercise ends with an "Open question" that goes beyond the block. Nobody has to answer it. Answers are in `solutions/git/README.md`.
- The message to repeat: an assistant can write the code, but you must know the words to ask for the right thing, read the diff to judge the result, and own what you commit.

## 5. Common problems

| Problem | Fix |
|---|---|
| Sign-in window does not appear | Run `git credential-manager --version`. Try a fresh `git clone`. Make sure the browser or the Windows sign-in dialog is not hidden behind VS Code. |
| Git Credential Manager signs in with the wrong account, without asking | Git Credential Manager can reuse the Windows work account. Remove the stored entries (next row), then clone again and pick the invited account. On some laptops `git config --global credential.msauthUseBroker false` brings back the browser sign-in. |
| `fatal: Authentication failed` after a password change or a switch of account | Windows Credential Manager (Control Panel) > Windows Credentials > remove the entries that mention `dev.azure.com`. Then clone or push again. |
| Signed in, but "You do not have access" or the wrong organisation list in the browser | Wrong tenant or directory. The guest account lives in the tenant of the Academy organisation, not in the Atlas Copco tenant. Switch directory in the profile menu of Azure DevOps, or open `https://dev.azure.com/<organisation>` directly. |
| `TF401019: The Git repository with name or identifier ... does not exist or you do not have permissions` | URL typo (check the project name and `_git`), the account is not in the project, the access level is Stakeholder instead of Basic, or Git signed in with a different account. Check Organization settings > Users. |
| `Author identity unknown` on commit | Participant did not do the `git config` step (task 1) of exercise 1. |
| Push to `main` rejected with `(fetch first)` | Expected in exercise 5: someone else pushed first. `git pull`, then `git push` again. With ten people this can take a few rounds. Never force push. |
| Push to `main` rejected with `TF402455: Pushes to this branch are not permitted` | Not expected in the morning: a branch policy is on `main`. Turn it off for the Git block (section 1), or, if the afternoon already set it up, demonstrate exercise 5 on your screen. |
| Participant committed on `main` locally | `git switch -c feature/<name>-intro` creates a branch at the current commit. Then in `main`: `git fetch` and `git reset --hard origin/main`. This is outside the exercises, so do it for them. |
| `git pull` says "divergent branches" | Run `git config --global pull.rebase false`, then `git pull` again. This keeps the merge behaviour explained in the exercises. |
| `git branch -d` says "not fully merged" | The branch is not in the current branch yet. Check `git branch --show-current` is `main` and that the merge was done. Do not use `-D` unless you know why. |
| `git push origin --delete ...` refused | The participant tries to delete a branch someone else created, or the branch name is wrong. `git branch -r` lists the exact names. |
| Merge or pull opens an editor and the participant is stuck | Close the tab in VS Code, or in vim press `Esc`, type `:wq` and press Enter. Next time `git merge --no-edit <branch>`. |
| Shared `README.md` left with a change from exercise 5, task 3 | Change it back with a normal commit on `main` and push. Do not force push. |
| Two participants have the same first name | Add the last initial: `anna-v`. |
| The setup script says the folder exists | Use `--force`. |

## 6. After the training

- Optionally keep the repositories as read-only examples: under Project settings > Repositories you can disable a repository or remove the Contribute permission of the Contributors group.
- Delete the repositories, or the whole project, when they are no longer needed. Remove the participants from the organisation, so their Basic licences are freed. Ask Atlas Copco which retention they prefer.
- Nothing in these repositories is secret, but remind participants not to commit real measurement data or credentials in any repository.

## Checking the material

From the repository root:

```powershell
uv run pytest tests/test_git_setup.py   # checks the Git setup script
uv run ruff check exercises/git tests   # lint
```
