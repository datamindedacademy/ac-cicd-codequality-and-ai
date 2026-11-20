# Git exercises

Day 3, first block: version control with Git and Azure Repos, the Git part of Azure DevOps.

By the end you can: clone a remote repository, commit on a branch, push, merge your branch into `main` and push it, and pull.

## Overview

| # | Folder | Topic | Why it matters |
|---|---|---|---|
| 1 | `01-first-commit` | `git init`, `status`, `add`, `commit`, `log`, `diff`, `diff --staged`. The three areas. Commits that say one thing. | A commit is the unit you undo and review. |
| 2 | `02-history` | Extra exercise (ahead, or after class): `log`, `show`, find who changed a value and when, `restore`. | Find out what changed, who did it and why. |
| 3 | `03-branches` | `switch -c`, `merge` (fast-forward, merge conflict), `rebase`, `branch -d`. | Try things safely, and solve conflicts calmly. |
| 4 | `04-remote` | `clone` from Azure Repos, `remote`, `push -u` to the remote. | Your work is backed up and colleagues can get it. |
| 5 | `05-merge-and-push` | `pull` on `main`, `merge` your branch, `push`, a rejected push, delete the local and remote branch. | Your change reaches the shared `main`, and nobody's work is lost. |
| 6 | `06-git-in-vscode` | Trainer demo in class. Do it yourself afterwards. | Daily Git work, and keeping data out of history. |

Do the exercises in order. Exercise 2 is extra: do it when you are ahead, or after class. Exercise 6 is a trainer demo to repeat afterwards.

## How an exercise works

- **Words to use**: the terms of that exercise.
- **Tasks**: three per exercise (exercise 6 is a list of steps). Each states a result to reach, not the commands. The last one is much harder. Most people will not finish it in class.
- **No hints**: find the commands in the slides, in the cheat sheet below, or with `git help <command>`.
- Answers are in `solutions/git/README.md`.
- **Open question**: goes beyond this block. Most people cannot answer it yet. Try it, or bring it to the trainer.

## Using Copilot

You may use Copilot in VS Code all day. No task needs it.

- Type the Git commands yourself in this block. You need the words to ask for the right thing later.
- Read `git diff` before every commit, whoever wrote the change.
- You are the author of what you commit and push.

## Setup scripts for exercises 1 to 3

Exercises 1 to 3 start from a prepared folder. Create it with the setup script. Run this from the root of the course repository (`ac-cicd-codequality-and-ai`), in PowerShell:

```powershell
uv run python exercises/git/setup_exercise.py 1
```

Use `2` or `3` for the other exercises. The script creates `git-exercises\exercise_<n>` in your home folder, outside the course repository, and prints the two commands you need next. Add `--force` to start again, or `--target <folder>` to put it somewhere else.

## Where you edit the files

The exercise folder is outside the course repository, so its files do not show up in the VS Code window you have open now. Open the exercise folder in a second VS Code window:

```powershell
cd "$HOME\git-exercises\exercise_1"
code .
```

- **Second window** (the exercise folder): edit the files here. Open its terminal with ``Ctrl+` ``. It starts in the exercise folder, so type your Git commands there.
- **First window** (the course repository): keep it open to read the exercise text. Switch between the two with `Alt+Tab`.
- If VS Code asks "Do you trust the authors of the files in this folder?", click **Yes**. You created them.
- If `code` is not recognised, use **File > New Window**, then **File > Open Folder** and choose the exercise folder.

Do the same for the clone of the training repository in exercises 4 to 6.

Exercises 4 to 6 use your group's training repository in Azure Repos and need no setup script. The trainer gives you its URL:

```
https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
```

## If you get stuck

- Stuck in a screen with `:` or `(END)` at the bottom? You are in a pager. Press `q`.
- Stuck in a text editor after a commit or merge? Close the tab in VS Code. In vim, press `Esc`, type `:q!` and press Enter. Next time use `git commit -m "message"`.
- Not sure where you are? Run `pwd`, then `git status`.
- Raise your hand. Nothing in these exercises can destroy your work, except `git restore <file>` on uncommitted edits, and that one is marked in the text.

## Cheat sheet

All commands work in Windows PowerShell. Use `<...>` for a value you fill in.

### Set up (once per laptop)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.name@example.com"
git config user.name                  # check
```

### Start

```powershell
git init -b main                      # make a new repository in this folder
git clone <url>                       # copy a remote repository to your laptop
```

### The daily cycle

```powershell
git status                            # what is changed, staged, untracked?
git diff                              # unstaged changes
git diff --staged                     # staged changes
git add <file>                        # stage a file
git commit -m "Add ..."               # save a snapshot (always use -m)
git push                              # send commits to the remote
git pull                              # get commits from the remote
```

### Branches

```powershell
git branch                            # list local branches
git branch -a                         # also list remote branches
git switch <branch>                   # go to a branch
git switch -c <new-branch>            # create a branch and go to it
git merge <branch>                    # merge <branch> into the current branch
git rebase main                       # replay this branch on top of main (unpushed commits only)
git branch -d <branch>                # delete a merged branch
git push -u origin <branch>           # first push of a new branch
git push origin --delete <branch>     # delete a branch on the remote
git fetch --prune                     # update remote info, forget deleted remote branches
```

### History

```powershell
git log --oneline                     # one line per commit (q to quit)
git log --oneline --graph --all --decorate   # picture of all branches
git show <hash>                       # one commit in detail
git diff <hash1> <hash2>              # compare two commits
git log -S <text>                     # commits that added or removed <text>
git blame <file>                      # who last changed each line
git switch --detach <hash>            # look at an old version
git switch main                       # come back
```

### Undo

```powershell
git restore <file>                    # throw away uncommitted edits (cannot be undone)
git restore --staged <file>           # unstage, keep the edit
git merge --abort                     # leave a merge that went wrong
git rebase --abort                    # leave a rebase that went wrong
```

### The three areas

```
working tree  --git add-->  staging area  --git commit-->  repository  --git push-->  remote
                                                           repository  <--git pull--  remote
```

### The merge and share flow

```
git switch -c feature/<name>-<topic>      1. branch
(edit files)                              2. work
git add <file> ; git commit -m "..."      3. commit (in PowerShell 5.1 use ; instead of &&)
git switch main ; git pull                4. update main
git merge feature/<name>-<topic>          5. merge your branch
git push                                  6. share main (refused? git pull, then git push)
git branch -d feature/<name>-<topic>      7. delete the branch on your laptop
git push origin --delete feature/<name>-<topic>   8. and on the remote (if you pushed it)
git fetch --prune                         9. forget remote branches deleted by others
```

This afternoon a pull request takes the place of steps 4 to 6.
